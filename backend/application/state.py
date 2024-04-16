from db.db import Database


class ApplicationState:

    card_data_db: Database

    def __init__(self, db: Database) -> None:
        self.card_data_db = db
