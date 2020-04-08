import json


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
