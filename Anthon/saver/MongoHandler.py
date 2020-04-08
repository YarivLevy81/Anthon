import pymongo
from Anthon.saver import ResultEntry, UserEntry


BASE_DB = "anthon_db"
USERS_DOCUMENT = "users"
SNAPSHOTS_DOCUMENT = "snapshots"
MONGO_DEFAULT_PATH = "mongodb://localhost:27017"


class MongoHandler:

    def __init__(self, path=MONGO_DEFAULT_PATH):
        self.path = path
        self.client = pymongo.MongoClient(self.path)

        self.db            = self.client[BASE_DB]
        self.users_doc     = self.db[USERS_DOCUMENT]
        self.snapshots_doc = self.db[SNAPSHOTS_DOCUMENT]

    def save_user(self, user_entry: UserEntry):
        if self.user_id_exists(user_entry.user_id):
            return

        self.users_doc.insert_one(user_entry.to_json())

    def user_id_exists(self, user_id):
        return True if self.users_doc.find_one({'user_id': user_id}) else False

    def save_snapshot_result(self, result_entry: ResultEntry):
        if not self.snapshot_id_exists(result_entry.snapshot_id):
            self.snapshots_doc.insert_one(result_entry.to_json())
            return

        self.snapshots_doc.update({'snapshot_id': result_entry.snapshot_id}, {'$set' : {result_entry.result_to_json()}})

    def snapshot_id_exists(self, snapshot_id):
        return True if self.snapshots_doc.find_one({'snapshot_id': snapshot_id}) else False

    def get_user(self):
        pass

    def get_snapshot(self):
        pass

    def get_user_snapshots(self):
        pass

    def get_snapshot_result(self):
        pass
