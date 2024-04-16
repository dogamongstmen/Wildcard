# Appease the type-checker by all measns necessary.
# We use these types so that we don't need to import from pymongo.*.* (which is very annoying)


from typing import Any, TypeVar
from pymongo import MongoClient, database
from pymongo import results

from pymongo.collection import Collection
from pymongo.cursor import Cursor

from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern


InsertOneResult = results.InsertOneResult

CurT = TypeVar("CurT")


class DbCursor(Cursor[CurT]): ...


ColT = TypeVar("ColT")


class DbCollection(Collection[ColT]):
    def find(self, *args: Any, **kwargs: Any) -> DbCursor[ColT]:
        return super().find(*args, **kwargs)


class Database(database.Database):
    def get_collection(
        self,
        name: str,
        codec_options: database.CodecOptions[Any] | None = None,
        read_preference: database._ServerMode | None = None,
        write_concern: WriteConcern | None = None,
        read_concern: ReadConcern | None = None,
    ) -> DbCollection[ColT]:
        return super().get_collection(
            name, codec_options, read_preference, write_concern, read_concern
        )


class DatabaseClient(MongoClient):
    def get_database(
        self,
        name: str | None = None,
        codec_options: database.CodecOptions[Any] | None = None,
        read_preference: database._ServerMode | None = None,
        write_concern: WriteConcern | None = None,
        read_concern: ReadConcern | None = None,
    ) -> Database:
        return super().get_database(
            name, codec_options, read_preference, write_concern, read_concern
        )

    # I probably won't use these dunder methods.
    # def __enter__(self) -> MongoClient:
    #     return super().__enter__()

    # def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
    #     self.close()
    #     return super().__exit__(exc_type, exc_val, exc_tb)
