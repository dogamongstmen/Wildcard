from typing import Final
from pymongo import MongoClient
from application.routes.api.endpoints.cardsets.cardsets import (
    api_create_card_set_handler,
    api_get_card_set_handler,
)
from application.routes.api.endpoints.singlecardset.members import (
    api_create_card_handler,
    api_get_card_set_members_handler,
)
from application.routes.api.endpoints.singlecardset.root import (
    api_delete_single_card_set_handler,
    api_get_single_card_set_handler,
    api_update_single_card_set_handler,
)
from application.routes.pages.home import page_home_handler
from application.routes.pages.singlecardset import page_get_card_set_handler
from application.state import ApplicationState
from db.credentials import get_db_credentials
from db.databases import DB_FLASHCARD_DATA
from server.routing.route import Route
from server.server import Server

from pymongo.database import Database

PORT: Final[int] = 5000


def main() -> None:

    credentials: str = get_db_credentials()
    db_client: MongoClient = MongoClient(credentials)
    card_data_db: Database = db_client.get_database(DB_FLASHCARD_DATA)

    app_state: ApplicationState = ApplicationState(card_data_db)
    app: Server[ApplicationState] = Server(app_state)

    # Viewable pages.
    page_home_route: Route = Route("/").get(page_home_handler)
    page_card_set_route: Route = Route("/collections/:set_id").get(
        page_get_card_set_handler
    )

    # API

    api_card_collections_route: Route = (
        Route("/api/card_sets")
        .get(api_get_card_set_handler)
        .post(api_create_card_set_handler)
    )

    api_card_set_route: Route = (
        Route("/api/card_sets/:set_id")
        .get(api_get_single_card_set_handler)
        .patch(api_update_single_card_set_handler)
        .delete(api_delete_single_card_set_handler)
    )

    api_card_set_members_route: Route = (
        Route("/api/card_sets/:set_id/cards")
        .get(api_get_card_set_members_handler)
        .post(api_create_card_handler)
    )

    api_card_set_single_card_route: Route = Route(
        "/api/card_sets/:set_id/cards/:card_id"
    )

    # Set up routes.
    app.route(page_home_route).route(page_card_set_route)

    app.route(api_card_collections_route).route(api_card_set_route).route(
        api_card_set_members_route
    )

    # Start server.
    socket = app.listen("", PORT)
    print(f"Listening on port {PORT}")
    input("Press ENTER to shut down the server: \n")
    app.shutdown()

    db_client.close()


main()
