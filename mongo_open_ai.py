from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.collection import Collection

from openai import Model, api_key
from typing import List

import yaml

from grand_index import GrandIndex
from qa_record import QARecord

class MongoOpenAI:
    def __init__(self, mongodb_uri: str, openai_api_key: str, chat_name: str):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client["openai"]
        self.chat_name = chat_name
        self.collection_name = f"{self.chat_name}_qa"
        self.collection = self.db[self.collection_name]
        self.GrandIndex = GrandIndex()
        self.model = Model("text-davinci-002", api_key=openai_api_key)

    def insert_one(self, question: str, answers: List[str], extra: dict):
        record = QARecord(self.chat_name, question, answers, extra)
        self.collection.insert_one(record.__dict__)
        self.GrandIndex[record.id] = record
        
    def update_one(self, question: str, answers: List[str], extra: dict):
        record = QARecord(self.chat_name, question, answers, extra)
        self.collection.update_one({"id": record.id}, {"$set": record.__dict__})
        self.GrandIndex[record.id] = record

    def process_yaml(self, yaml_file_name: str):
        with open(yaml_file_name, 'r') as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                for dialog in yaml_data["dialogs"]:
                    if dialog["import"] == "yes":
                        for qa in dialog["script"]:
                            self.insert_one(qa["question"], qa["answers"], {})
            except yaml.YAMLError as exc:
                print(exc)

