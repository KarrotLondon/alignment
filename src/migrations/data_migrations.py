


from src.models.kinks import Kinks
from src.models.user import User


class DataMigrations:
    
    def __init__(self, user):
        self.user = user
    
    def run(self):
        self.user = self.migration_1()
        self.user = self.migration_2()
        
        return self.user
    
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
        return self.user
    
    def migration_2(self):
        if not self.user.get("links"):
            return User(
                _id=self.user.get("_id"),
                username=self.user.get("username"),
                password=self.user.get("password"),
                email=self.user.get("email"),
                kinks=self.user.get("kinks"),
                links=[]
            )
        return self.user
