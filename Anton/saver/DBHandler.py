from abc import ABC, abstractmethod


class ResultEntry:
    def __init__(self, user_id, snapshot_id, snapshot_path, timestamp, result_type, result_data):
        self.user_id       = user_id
        self.snapshot_id   = snapshot_id
        self.snapshot_path = snapshot_path
        self.timestamp     = timestamp
        self.result_type   = result_type
        self.result_data   = result_data

    def to_json(self):
        result_dict = dict(
            user_id       = self.user_id,
            snapshot_id   = self.snapshot_id,
            snapshot_path = self.snapshot_path,
            timestamp     = self.timestamp,
        )
        result_dict[self.result_type] = self.result_data
        return result_dict

    def result_to_json(self):
        return {self.result_type: self.result_data}


class UserEntry:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id    = user_id
        self.username   = username
        self.birthdate  = birthdate
        self.gender     = gender

    def to_json(self):
        result_dict = dict(
            user_id   = self.user_id,
            username  = self.username,
            birthdate = self.birthdate,
            gender    = self.gender,
        )
        return result_dict


class DBHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save_user(self, user_entry: UserEntry):
        pass

    @abstractmethod
    def user_id_exists(self, user_id) -> bool:
        pass

    @abstractmethod
    def save_snapshot_result(self, result_entry: ResultEntry):
        pass

    @abstractmethod
    def snapshot_id_exists(self, snapshot_id) -> bool:
        pass

    @abstractmethod
    def get_all_users(self) -> list:
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def get_user_snapshots(self, user_id) -> list:
        pass

    @abstractmethod
    def get_snapshot(self, user_id, snapshot_id):
        pass

    @abstractmethod
    def get_snapshot_result(self, user_id, snapshot_id, topic):
        pass
