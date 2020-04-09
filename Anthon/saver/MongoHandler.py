import pymongo
from Anthon.saver import ResultEntry, UserEntry, DBHandler
from furl import furl
from Anthon.common import UnsupportedSchemeException
import Anthon.common as Common


BASE_DB = "anthon_db"
USERS_COL = "users"
SNAPSHOTS_COL = "snapshots"
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
        self.users_col     = self.db[USERS_COL]
        self.snapshots_col = self.db[SNAPSHOTS_COL]
        super().__init__()

    def save_user(self, user_entry: UserEntry):
        if self.user_id_exists(user_entry.user_id):
            print("user exists")
            return

        self.users_col.insert_one(user_entry.to_json())

    def user_id_exists(self, user_id):
        return True if self.get_user(user_id) else False

    def save_snapshot_result(self, result_entry: ResultEntry):
        if not self.snapshot_id_exists(result_entry.snapshot_id):
            print("snapshot doesn't exist")
            self.snapshots_col.insert_one(result_entry.to_json())
            return

        self.snapshots_col.update({'snapshot_id': result_entry.snapshot_id}, {'$set' : result_entry.result_to_json()})

    def snapshot_id_exists(self, snapshot_id):
        return True if self.snapshots_col.find_one({'snapshot_id': snapshot_id}) else False

    def get_all_users(self):
        users_json_list = []
        for user_doc in self.users_col.find():
            user_json = dict()
            user_json[Common.USER_ID_FIELD]  = user_doc[Common.USER_ID_FIELD]
            user_json[Common.USERNAME_FIELD] = user_doc[Common.USERNAME_FIELD]

            users_json_list.append(user_json)

        return users_json_list

    def get_user(self, user_id):
        user_doc = self.users_col.find_one({Common.USER_ID_FIELD: user_id})
        if user_doc is not None:
            user_doc.pop('_id')

        return user_doc

    def get_user_snapshots(self, user_id):
        snapshots_json_list = []

        for snapshot_doc in self.snapshots_col.find({Common.USER_ID_FIELD: user_id}):
            snapshot_json = dict()
            snapshot_json[Common.SNAPSHOT_ID_FIELD] = snapshot_doc[Common.SNAPSHOT_ID_FIELD]
            snapshot_json[Common.TIMESTAMP_FIELD]   = snapshot_doc[Common.TIMESTAMP_FIELD]

            snapshots_json_list.append(snapshot_json)

        return snapshots_json_list

    def get_snapshot(self, snapshot_id):
        snapshot_doc = self.snapshots_col.find({Common.SNAPSHOT_ID_FIELD: snapshot_id})
        if snapshot_doc is not None:
            snapshot_doc.pop('_id')
            snapshot_doc.pop(Common.SNAPSHOT_PATH_FIELD)
            snapshot_doc.pop(Common.USER_ID_FIELD)

        return snapshot_doc

    def get_snapshot_result(self, snapshot_id, topic):
        snapshot_doc = self.get_snapshot(snapshot_id)
        if snapshot_doc is not None:
            if topic in snapshot_doc:
                return snapshot_doc[topic]

        return None
