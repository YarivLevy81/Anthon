import pathlib


USERS_DATA_DIRECTORY = "/users_data"


class Session:

    def __init__(self, user_id, timestamp):
        self.user_id = user_id
        self.timestamp = timestamp

    def save(self, filename, data):
        new_path = pathlib.Path(f'{USERS_DATA_DIRECTORY}/{self.user_id}/{self.timestamp}')
        new_path.mkdir(parents=True, exist_ok=True)
        new_file = new_path / filename
        new_file.write_bytes(data)
        return new_file.absolute()

    def new_path(self, filename):
        new_path = pathlib.Path(f'{USERS_DATA_DIRECTORY}/{self.user_id}/{self.timestamp}')
        new_path = new_path / filename
        return new_path.absolute()