import toml
from typing import Optional, Dict

class ChannelDefinition:
    def __init__(self):
        """
        Initialize a ChannelDefinition instance with all attributes set to None.
        The attributes are intended to be set using the read method.
        """
        self.name: Optional[str] = None
        self.domain: Optional[str] = None
        self.prompt: Optional[str] = None

    def read(self, file_path: str, channel_name: str, default_prompt: str):
        """
        Read the channel definition from a TOML file.

        Args:
        file_path (str): The path to the TOML file containing channel definitions.
        channel_name (str): The name of the channel to search for in the TOML file.
        default_prompt (str): The default prompt to use if the prompt is not defined in the file.

        Sets the object's attributes based on the data found in the file.
        """
        self.name = channel_name
        self.domain = None  # Default value, indicating no specific domain
        self.prompt = default_prompt

        try:
            with open(file_path, 'rb') as file:
                data = toml.load(file)

            channel_data = data.get(channel_name)
            if channel_data:
                self.domain = channel_data.get('domain')
                self.prompt = channel_data.get('prompt', default_prompt)

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    @staticmethod
    def read_all(file_path: str) -> Dict[str, 'ChannelDefinition']:
        """
        Read all channel definitions from a TOML file and return a dictionary mapping
        each channel name to a ChannelDefinition object.

        Args:
        file_path (str): The path to the TOML file containing channel definitions.
        default_prompt (str): The default prompt to use for each channel.

        Returns:
        Dict[str, ChannelDefinition]: A dictionary mapping channel names to their definitions.
        """
        channel_map = {}

        try:
            with open(file_path, 'r') as file:
                data = toml.load(file)

            for channel_name, attributes in data.items():
                channel_def = ChannelDefinition()
                channel_def.name = channel_name
                channel_def.domain = attributes.get('domain')
                channel_def.prompt = attributes.get('prompt', "Error")
                channel_map[channel_name] = channel_def

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

        return channel_map

