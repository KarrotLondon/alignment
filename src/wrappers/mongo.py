from typing import Any, Optional
import pymongo
from src.models.link import Link
from src.models.user import User  
from src.models.kink import Kink
from fastapi.encoders import jsonable_encoder 
from typing import Any, List
from bson import ObjectId

class Mongo:
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.alignment
    
    @property
    def users_table(self):
        return self.db.users
    
    def check_username_in_use(self, username) -> bool:
        usernames = self.find_user(username)
        return usernames is not None

    def find_user(self, username) -> dict[str, Any]:
        return self.users_table.find_one({"username": username})
    
    def get_user_by_username(self, username) -> Optional[User]:
        user = self.find_user(username)
        if user:
            return User(_id=user.get("_id"), username=user.get("username"), password=user.get("password"), email=user.get("email"), kinks=user.get("kinks"), links=user.get("links"))
    
    def get_user_by_id(self, id) -> Optional[User]:
        user = self.users_table.find_one({"_id": id})
        if user:
            return User(_id=user.get("_id"), username=user.get("username"), password=user.get("password"), email=user.get("email"), kinks=user.get("kinks"), links=user.get("links"))

    def add_kink(self, user_id: str, kink: Kink):
        self.users_table.find_one_and_update(
            {'_id': user_id},
            {'$push': {'kinks': jsonable_encoder(kink)}}
        )
    
    def add_user(self, user: User) -> User:
        return self.users_table.insert_one(jsonable_encoder(user))
    
    def update_kinks(self, user_id: str, kinks: List[Kink]):
        self.users_table.update_one(
            {'_id': str(user_id)},
            {'$set': {"kinks": jsonable_encoder(kinks)}}
        )
    
    def update_links(self, user_id: str, link: Link):
        self.users_table.update_one(
            {'_id': str(user_id)},
            {'$push': {"links": jsonable_encoder(link)}}
        )
    
    def approve_link(self, user_id: str, link_id: str):
        self.users_table.update_one(
            {"_id": str(user_id)},
            {"$set": {
                "links.$[updateLink].pending": False
            }},
            array_filters=[
                    {"updateLink.user_id": link_id}
            ]
        )
        self.users_table.update_one(
            {"_id": link_id},
            {"$set": {
                "links.$[updateLink].pending": False
            }},
            array_filters=[
                    {"updateLink.user_id": str(user_id)}
                ]
        )
    
    def no_link_requests(self, user_id: str) -> int:
        user = self.get_user_by_id(str(user_id))
        return len([i for i in user.links if i.pending and not i.requested])


