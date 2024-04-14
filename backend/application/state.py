from pymongo import MongoClient


class ApplicationState:

    db_client: MongoClient

    def __init__(self, client: MongoClient) -> None:
        self.db_client = client
