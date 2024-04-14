from typing import Final
from pymongo import MongoClient

from application.endpoints.api.cards import (
    api_get_card_handler,
    api_remove_card_handler,
    api_update_card_handler,
)
from application.endpoints.api.cardsets import (
    api_create_card_set_handler,
    api_get_card_set_handler,
)
from application.endpoints.api.singlecardset import (
    api_add_single_card_set_handler,
    api_delete_single_card_set_handler,
    api_get_single_card_set_handler,
)
from application.endpoints.pages.home import page_home_handler
from application.endpoints.pages.singlecardset import page_get_card_set_handler
from application.state import ApplicationState
from db.credentials import get_db_credentials
from server.routing.route import Route
from server.server import Server

PORT: Final[int] = 5000


def main() -> None:

    credentials: str = get_db_credentials()
    db_client: MongoClient = MongoClient(credentials)

    app_state: ApplicationState = ApplicationState(db_client)

    app: Server[ApplicationState] = Server(app_state)

    # Viewable pages.
    page_home_route: Route = Route("/").get(page_home_handler)
    page_card_set_route: Route = Route("/collections/:set_id").get(
        page_get_card_set_handler
    )

    # API
    api_card_route: Route = (
        Route("/api/cards/:card_id")
        .get(api_get_card_handler)
        .patch(api_update_card_handler)
        .delete(api_remove_card_handler)
    )

    api_card_sets_route: Route = (
        Route("/api/sets")
        .get(api_get_card_set_handler)
        .post(api_create_card_set_handler)
    )

    api_single_card_set_route: Route = (
        Route("/api/sets/:set_id")
        .get(api_get_single_card_set_handler)
        .post(api_add_single_card_set_handler)
        .delete(api_delete_single_card_set_handler)
    )

    # Set up routes.
    app.route(page_home_route).route(page_card_set_route).route(api_card_route).route(
        api_card_sets_route
    ).route(api_single_card_set_route)

    socket = app.listen("", PORT)
    print(f"Listening on port {PORT}")
    input("Press ENTER to shut down the server: \n")
    app.shutdown()

    # db: Database = db_client.get_database(DB_FLASHCARD_DATA)
    # col: Collection[CardSet] = db.get_collection(COLLECTION_CARD_SETS)

    # card_sets: Cursor[CardSet] = col.find()
    # for card_col in card_sets:

    #     id_bin: bytes = card_col["_id"].binary

    #     print(id_bin[0:4].hex())
    #     print(id_bin[4:9].hex())
    #     print(id_bin[9:12].hex(), "\n")

    #     print(id_bin.hex())

    # db_client.close()


main()
