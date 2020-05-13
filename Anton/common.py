USER_ID_FIELD = 'user_id'
SNAPSHOT_PATH_FIELD = 'snapshot_path'
SNAPSHOT_ID_FIELD = 'snapshot_id'
TIMESTAMP_FIELD = 'timestamp'
TYPE_FIELD = 'type'
USERNAME_FIELD = 'username'
BIRTHDATE_FIELD = 'birthdate'
GENDER_FIELD = 'gender'
RESULT_DATA_FIELD = 'result_data'
DATA_FIELD = 'data'
IMAGE_PATH_FIELD = "image_path"

USER_TYPE = 'user'


class UnsupportedSchemeException(Exception):
    def __init__(self, scheme):
        self.scheme = scheme


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
