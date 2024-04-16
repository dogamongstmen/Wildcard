from enum import Enum
from typing import Dict
from db.db import Database

# We could store the data for the web page, scripts, and other assets in memory if there aren't too many.
# It's also faster than reading from the disk every request.
class PageType(Enum):
    Home = 0
    Favicon = 1
    # ???


class ApplicationState:

    card_data_db: Database

    page_data: Dict[str, str]

    def __init__(self, db: Database) -> None:
        self.card_data_db = db
