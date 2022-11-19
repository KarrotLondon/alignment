from typing import Any, Dict, List, cast

from src.models.kink import Kink
from src.models.kinks import Kinks
from src.models.user import User


class DataMigrations:
    def __init__(self, user: Dict[str, Any]) -> None:
        self.user = user

    def run(self) -> User:
        self.migration_1()
        self.migration_2()

        return User(
            _id=self.user.get("_id"),
            username=self.user.get("username"),
            password=self.user.get("password"),
            email=self.user.get("email"),
            kinks=Kinks(
                sub=cast(Dict[str, List[Kink]], self.user.get("kinks")).get("sub"),
                dom=cast(Dict[str, List[Kink]], self.user.get("kinks")).get("dom"),
            ),
            links=self.user.get("links"),
        )

    def migration_1(self) -> None:
        if isinstance(self.user.get("kinks"), list):
            self.user["kinks"] = {"sub": self.user.get("kinks"), "dom": []}

    def migration_2(self) -> None:
        if not self.user.get("links"):
            self.user["links"] = []
