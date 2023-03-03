from typing import Dict, List, Tuple
import openai
from qa_record import QARecord

class GrandIndex:
    def __init__(self):
        """
        The constructor initializes the dictionary that will hold the records.
        """
        self.records: Dict[str, QARecord] = {}

    def add_qa(self, question: str, answers: List[str], model):
        """
        Adds a QA record to the index.
        """
        # Create a QA record with the question and answers
        record = QARecord(question=question, answers=answers)

        # Generate the ID for the record
        record_id = record.get_id()

        # Add the record to the index
        self.records[record_id] = record

        # Get the vector representation of the question using the OpenAI model
        question_vec = model.get_vector(question)

        # Set the vector for the record to the vector representation of the question
        self.records[record_id].vector = question_vec

    def get_best_record(self, question: str, model: openai) -> Tuple[QARecord, float]:
        """
        Gets the best record that matches the question.
        """
        # Get the vector representation of the question using the OpenAI model
        question_vec = model.get_vector(question)

        # Initialize the best record and score to None
        best_record = None
        best_score = None

        # Iterate over all records in the index
        for record_id, record in self.records.items():
            # Skip records that have no unused answers
            if not record.unused_answers:
                continue

            # Calculate the similarity score between the question vector and the record vector
            record_vec = record.vector
            score = model.compute_similarity(question_vec, record_vec)

            # If this is the first record checked or if the score is better than the previous best score
            if best_score is None or score > best_score:
                # Update the best record and score
                best_record = record
                best_score = score

        # Return the best record and score
        return (best_record, best_score)

