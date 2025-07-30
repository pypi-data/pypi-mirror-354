from dotenv import load_dotenv
from ai_workspace import Workspace
from ai_workspace import WorkspaceSchema, DocumentSchema
import pytest
from ai_workspace.database import MongoDB, Qdrant
from ai_workspace.packages.shared import IDGenerator
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()


@pytest.fixture
def workspace_schema() -> WorkspaceSchema:
    """Create a test workspace schema."""
    return WorkspaceSchema(
        workspace_id="test_workspace",
        title="Test Workspace",
        description="A test workspace for testing",
        chat_sessions=[],
        instructions="Test instructions",
        user_id="fsd23",
    )


@pytest.fixture
def workspace() -> Workspace:
    """Create a test workspace instance."""
    TEST_MONGODB_URL = "mongodb://localhost:27017/aicore"
    TEST_QDRANT_URL = "http://localhost:6333"
    mongodb = MongoDB(uri=TEST_MONGODB_URL)
    qdrant = Qdrant(uri=TEST_QDRANT_URL)
    embedding = AzureOpenAIEmbeddings(
        azure_deployment="embedding",
    )
    return Workspace(mongodb=mongodb, qdrant=qdrant, embedding=embedding)


@pytest.fixture
def test_workspace_data():
    """Create test workspace data."""
    workspace_id = IDGenerator.generate()
    return WorkspaceSchema(
        description="A test workspace",
        instructions="Test instructions",
        chat_sessions=["123das", "jnvsjaj3"],
        user_id="12sdgffdgbhd3",
        title="test_title",
        workspace_id=workspace_id,
    )


# def test_upload_documnet(document, document_schema):
#     """Test adding a new document."""
#     document_id = document.upload_document(document_schema)
#     assert document_id is not None
#     assert isinstance(document_id, str)


def test_create(workspace, test_workspace_data):
    """Test adding a new workspace."""
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Verify the workspace was created
    created_workspace = workspace.find_workspace_by_id(workspace_id)
    assert created_workspace is not None
    assert created_workspace.workspace_id == workspace_id
    assert created_workspace.title == test_workspace_data.title

    # Verify the workspace on Qdrant
    qdrant_collection_exists = workspace.qdrant_client.collection_exists(workspace_id)
    assert qdrant_collection_exists is True

    # clean up
    workspace.delete_workspace(workspace_id)


def test_add_session(workspace, test_workspace_data):
    """Test adding a session to a workspace."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)
    # Then add a session
    session_id = "test_session_123"
    result = workspace.add_session(workspace_id, session_id)
    assert result is True
    # Verify the session was added
    updated_workspace = workspace.find_workspace_by_id(workspace_id)
    assert updated_workspace is not None
    assert session_id in updated_workspace.chat_sessions
    assert isinstance(updated_workspace.chat_sessions, list)
    assert len(updated_workspace.chat_sessions) > 0
    assert any(
        session == session_id for session in updated_workspace.chat_sessions
    ), "Session should be in the workspace's chat sessions"
    # Clean up
    workspace.delete_workspace(workspace_id)


def test_get_instructions(workspace, test_workspace_data):
    """Test getting instructions from a workspace."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Then get instructions
    instructions = workspace.get_instructions(workspace_id)
    assert instructions == test_workspace_data.instructions

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_delete_workspace(workspace, test_workspace_data):
    """Test deleting a workspace."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Then delete the workspace
    result = workspace.delete_workspace(workspace_id)
    assert result is True

    # Verify the workspace is deleted
    with pytest.raises(Exception):
        workspace.get_instructions(workspace_id)  # Should raise an error


def test_update_instructions(workspace, test_workspace_data):
    """Test updating instructions in a workspace."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Then update instructions
    new_instructions = "Updated test instructions"
    result = workspace.update_instructions(workspace_id, new_instructions)
    assert result is True

    # Verify the instructions are updated
    updated_instructions = workspace.get_instructions(workspace_id)
    assert updated_instructions == new_instructions

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_get_workspace(workspace, test_workspace_data):
    """Test getting a workspace by ID."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Then get the workspace
    retrieved_workspace = workspace.find_workspace_by_id(workspace_id)
    assert retrieved_workspace is not None
    assert retrieved_workspace.workspace_id == workspace_id
    assert retrieved_workspace.title == test_workspace_data.title

    # Clean up
    workspace.delete_workspace(workspace_id)


def test_get_workspace_by_user(workspace, test_workspace_data):
    """Test getting workspaces by user ID."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Then get workspaces by user ID
    retrieved_workspaces = workspace.find_workspace_by_user_id(
        test_workspace_data.user_id
    )
    assert retrieved_workspaces is not None
    assert isinstance(retrieved_workspaces, list)
    assert len(retrieved_workspaces) > 0
    # assert contains the created workspace
    assert any(
        ws.workspace_id == workspace_id for ws in retrieved_workspaces
    ), "Created workspace should be in the list of retrieved workspaces"

    # Clean up
    workspace.delete_workspace(workspace_id)  # Clean up the test workspace


def test_add_knowledge(workspace, test_workspace_data):
    """Test uploading a document to a workspace."""
    # First add a workspace
    workspace_id = workspace.create(test_workspace_data)
    assert workspace_id is not None
    assert isinstance(workspace_id, str)

    # Create a test document schema
    document_schema = DocumentSchema(
        workspace_id=workspace_id,
        file_name="test_file.txt",
        file_mime="text/plain",
        file_suffix=".txt",
    )

    document_id = workspace.add_knowledge(
        document=document_schema,
        to_workspace=True,
        raw_texts=["This is a test document.", "It contains some test data."],
        metadata={"source": "test_file.txt"},
    )
    assert document_id is not None
    assert isinstance(document_id, str)

    # Verify the document was added
    found_document = workspace.document_client.get_document(document_id)
    assert found_document is not None
    assert found_document.workspace_id == workspace_id
    assert found_document.file_name == document_schema.file_name
    assert found_document.file_mime == document_schema.file_mime
    assert found_document.file_suffix == document_schema.file_suffix

    # Clean up
    workspace.delete_workspace(workspace_id)
