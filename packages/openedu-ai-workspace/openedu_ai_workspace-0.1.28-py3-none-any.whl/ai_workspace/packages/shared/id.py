from snowflake import SnowflakeGenerator


class IDGenerator(SnowflakeGenerator):
    """
    IDGenerator is a wrapper around SnowflakeGenerator to generate unique IDs.
    It inherits from SnowflakeGenerator and can be extended with additional functionality if needed.
    """

    def __init__(self, instance: int = 25):
        """
        Initialize the IDGenerator with a specific instance ID.

        :param instance: The instance ID for the Snowflake generator.
        """
        super().__init__(instance=instance)
