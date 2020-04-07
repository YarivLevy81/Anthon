import pymongo


BASE_DB = "anthon_db"
USERS_DOCUMENT = "users"
SNAPSHOTS_DOCUMENT = "snapshots"
MONGO_DEFAULT_PATH = "mongodb://localhost:27017"


class MongoHandler:

    def __init__(self, path=MONGO_DEFAULT_PATH):
        self.path = path
        self.client = pymongo.MongoClient(self.path)

        self.db = self.client[BASE_DB]
        self.users_doc = self.db[USERS_DOCUMENT]
        self.snapshots_dob = self.db[SNAPSHOTS_DOCUMENT]

    def insert_user(self):
        pass

    def insert_snapshot(self):
        pass

    def get_user(self):
        pass

    def get_snapshot(self):
        pass

    def get_user_snapshots(self):
        pass

    def get_snapshot_result(self):
        pass

    def set_(self):
        pass