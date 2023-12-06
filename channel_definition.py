import toml
from typing import Optional, Dict

class ChannelDefinition:
    def __init__(self, name: str, domain: str, prompt: str):
        """
        Initialize a ChannelDefinition instance with all attributes set to None.
        The attributes are intended to be set using the read method.
        """
        self.name: Optional[str] = name
        self.domain: Optional[str] = domain
        self.prompt: Optional[str] = prompt

        #definitions = ChannelDefinition.read_all(file_path = "general.toml")


    def read(self, file_path: str):
        """
        Read the channel definition from a TOML file.

        Args:
        file_path (str): The path to the TOML file containing channel definitions.

        Sets the object's attributes based on the data found in the file.
        """
        try:
            with open(file_path, 'rb') as file:
                data = toml.load(file)

            channel_data = data.get("abc")
            if channel_data:
                self.domain = channel_data.get('abc')

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")


    @staticmethod
    def read_all1(file_path: str) -> Dict[str, 'ChannelDefinition']:
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

