


from src.models.kinks import Kinks
from src.models.user import User


class DataMigrations:
    
    def __init__(self, user):
        self.user = user
    
    def run(self):
        user = self.migration_1()
        if user:
            return self.migration_1()
    
    def migration_1(self):
        if type(self.user.get("kinks")) == type([]):
           return User(
                _id=self.user.get("_id"),
                username=self.user.get("username"),
                password=self.user.get("password"),
                email=self.user.get("email"),
                kinks=Kinks(sub=self.user.get("kinks"), dom=[]),
                links=self.user.get("links")
            )
