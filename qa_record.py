import random
import hashlib
from typing import Any, Dict, List, Optional, Tuple

class QARecord:
    def __init__(self, question: str, answers: List[str], extra: Dict[str, List[str]] = None):
        self.id = self.get_id(question)
        self.question = question
        self.answers = answers
        self.used_indexes = set()
        self.extra = extra or {}

    @staticmethod
    def get_id(question: str) -> str:
        """
        Compute the unique ID for the QA record based on the question text.
        """
        hash_object = hashlib.sha256(question.encode())
        return hash_object.hexdigest()

    def pick_an_answer(self) -> Optional[Tuple[int, str]]:
        """
        Pick an answer randomly from the set of unused answers.
        """
        unused_indexes = self.get_unused_indexes()
        if not unused_indexes:
            return None
        index = random.choice(unused_indexes)
        self.used_indexes.add(index)
        return index, self.answers[index]

    def get_unused_indexes(self) -> List[int]:
        """
        Get a list of all answer indexes that have not been used yet.
        """
        return [i for i in range(len(self.answers)) if i not in self.used_indexes]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the QA record to a dictionary for saving to a database.
        """
        return {
            "id": self.id,
            "question": self.question,
            "answers": self.answers,
            "extra": self.extra
        }

    @staticmethod
    def from_dict(qa_dict: Dict[str, Any]) -> "QARecord":
        """
        Create a QARecord object from a dictionary retrieved from a database.
        """
        return QARecord(
            question=qa_dict["question"],
            answers=qa_dict["answers"],
            extra=qa_dict.get("extra")
        )
