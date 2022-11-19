from typing import Any, Dict, List, Optional, cast

from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pymongo.collection import Collection

from src.migrations.data_migrations import DataMigrations
from src.models.enums import Roles
from src.models.id import PyObjectId
from src.models.kink import Kink
from src.models.kinks import Kinks
from src.models.link import Link
from src.models.user import User


class MongoWrapper:
    def __init__(self, uri: str) -> None:
        client: MongoClient = MongoClient(uri)
        self._db = client.alignment

    @property
    def _users_table(self) -> Collection:
        return self._db.users

    def check_username_in_use(self, username: Optional[str]) -> bool:
        usernames = self._find_user(username)
        return usernames is not None

    def _find_user(self, username: Optional[str]) -> Optional[Dict[str, Any]]:
        return self._users_table.find_one({"username": username})

    def get_user_by_username(self, username: Optional[str]) -> Optional[User]:
        user = self._find_user(username)
        if user:
            return self._create_user(user)
        return None

    def _create_user(self, user: Dict[str, Any]) -> User:
        try:
            return User(
                _id=user.get("_id"),
                username=user.get("username"),
                password=user.get("password"),
                email=user.get("email"),
                kinks=Kinks(
                    sub=cast(Dict[str, List[Kink]], user.get("kinks")).get("sub"),
                    dom=cast(Dict[str, List[Kink]], user.get("kinks")).get("dom"),
                ),
                links=user.get("links"),
            )
        except Exception as e:
            migration_checker = DataMigrations(user)
            user_update = migration_checker.run()
            if user_update:
                self.update_user(user_update)
                return user_update
            raise e

    def update_user(self, user: User) -> None:
        self._users_table.update_one({"_id": str(user.id)}, {"$set": jsonable_encoder(user)})

    def get_user_by_id(self, id: Optional[str]) -> Optional[User]:
        user = self._users_table.find_one({"_id": id})
        if user:
            return self._create_user(user)
        return None

    def add_user(self, user: User) -> None:
        self._users_table.insert_one(jsonable_encoder(user))

    def update_kinks(self, user_id: PyObjectId, kinks: List[Kink], role: Roles) -> None:
        self._users_table.update_one(
            {"_id": str(user_id)},
            {"$set": {f"kinks.{role.value}": jsonable_encoder(kinks)}},
        )

    def update_links(self, user_id: PyObjectId, link: Link) -> None:
        self._users_table.update_one({"_id": str(user_id)}, {"$push": {"links": jsonable_encoder(link)}})

    def approve_link(self, user_id: PyObjectId, link_id: Optional[str]) -> None:
        self._users_table.update_one(
            {"_id": str(user_id)},
            {"$set": {"links.$[updateLink].pending": False}},
            array_filters=[{"updateLink.user_id": link_id}],
        )
        self._users_table.update_one(
            {"_id": link_id},
            {"$set": {"links.$[updateLink].pending": False}},
            array_filters=[{"updateLink.user_id": str(user_id)}],
        )

    def no_link_requests(self, user_id: PyObjectId) -> int:
        user = cast(User, self.get_user_by_id(str(user_id)))
        return len([i for i in user.links if i.pending and i.requested])
