import pymongo
from Anthon.saver import ResultEntry, UserEntry, DBHandler
from furl import furl
from Anthon.common import UnsupportedSchemeException


BASE_DB = "anthon_db"
USERS_DOCUMENT = "users"
SNAPSHOTS_DOCUMENT = "snapshots"
MONGO_DEFAULT_PATH = "mongodb://localhost:27017"


class MongoHandler(DBHandler):

    def __init__(self, path):
        url = furl(path)
        if url.scheme != "mongodb":
            raise UnsupportedSchemeException(f'Only database supported is mongodb, ({url.scheme} is not supported)')

        self.host = url.host
        self.port = url.port
        self.client = pymongo.MongoClient(host=self.host, port=self.port)

        self.db            = self.client[BASE_DB]
        self.users_doc     = self.db[USERS_DOCUMENT]
        self.snapshots_doc = self.db[SNAPSHOTS_DOCUMENT]
        super().__init__()

    def save_user(self, user_entry: UserEntry):
        if self.user_id_exists(user_entry.user_id):
            print("user exists")
            return

        self.users_doc.insert_one(user_entry.to_json())

    def user_id_exists(self, user_id):
        return True if self.users_doc.find_one({'user_id': user_id}) else False

    def save_snapshot_result(self, result_entry: ResultEntry):
        if not self.snapshot_id_exists(result_entry.snapshot_id):
            print("snapshot doesn't exist")
            self.snapshots_doc.insert_one(result_entry.to_json())
            return

        self.snapshots_doc.update({'snapshot_id': result_entry.snapshot_id}, {'$set' : result_entry.result_to_json()})

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
