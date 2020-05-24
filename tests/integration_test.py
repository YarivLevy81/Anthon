import os
import time
from Anton.common import bcolors
import requests
from Anton.client import upload_sample


def main():
    try:
        # Environment up
        print(f'\n{bcolors.OKBLUE}Integration-Test: Setting up environment with docker-compose (this takes around a minute)..{bcolors.ENDC}\n')
        ret = os.system("docker-compose -f ./docker/docker-compose.yaml -p integ_test up -d")
        if ret != 0:
            raise Exception("docker-compose up failed")

        # Environment set
        print(f'\n{bcolors.OKBLUE}Integration-Test: Waiting for environment to be ready..{bcolors.ENDC}\n')
        time.sleep(15)  # Need to wait for RabbitMQ to set

        # Client upload samples
        print(f'\n{bcolors.OKBLUE}Integration-Test: Simulating client uploads..{bcolors.ENDC}\n')
        os.system("python3 -m Anton.client upload-sample ./tests/mock_data/3_sample.mind.gzip")
        time.sleep(5)

        # Testing results
        r = requests.get("http://0.0.0.0:5000/users")
        _json = r.json()
        if len(_json) != 1 or _json[0]['user_id'] != 42:
            raise Exception("Users json not correct")
        print(f'\n{bcolors.OKBLUE}Integration-Test: Users entry looks fine..{bcolors.ENDC}\n')

        r = requests.get("http://0.0.0.0:5000/users/42")
        _json = r.json()
        if not _json or _json['birthdate'] != 699746400:
            raise Exception("User 42 json not correct")
        print(f'\n{bcolors.OKBLUE}Integration-Test: User 42 entry looks fine..{bcolors.ENDC}\n')

        r = requests.get("http://0.0.0.0:5000/users/42/snapshots")
        _json = r.json()
        if not _json or len(_json) != 3:
            raise Exception("User 42 snapshots json not correct")
        print(f'\n{bcolors.OKBLUE}Integration-Test: User 42 snapshots entry looks fine..{bcolors.ENDC}\n')

        snapshots = [res['snapshot_id'] for res in _json]
        for snapshot in snapshots:
            r = requests.get("http://0.0.0.0:5000/users/42/snapshots/" + snapshot)
            _json = r.json()
            if not _json or 'pose' not in _json or 'feelings' not in _json or 'depth_image' not in _json or 'color_image' not in _json:
                raise Exception("User 42 snapshot data json not correct")
        print(f'\n{bcolors.OKBLUE}Integration-Test: Snapshots entries look fine..{bcolors.ENDC}\n')

        # Environemnt down
        print(f'\n{bcolors.OKBLUE}Integration-Test: Shutting down services and cleaning..{bcolors.ENDC}\n')

        for snapshot in snapshots:
            os.system("rm ./docker/snapshots/" + snapshot + ".raw")
            os.system("rm ./docker/snapshots/" + snapshot + ".snp")
            os.system("rm -rf ./docker/users_data/42/" + snapshot)
        print(f'\n{bcolors.OKBLUE}Integration-Test: Cleaning complete..{bcolors.ENDC}\n')

    except Exception as e:
        print(f'{bcolors.FAIL}<<<<< Integration test has failed >>>>>{bcolors.ENDC}')
        print(f'{bcolors.FAIL}ERROR: {e}{bcolors.ENDC}')

    finally:
        os.system("./scripts/clean_integration_mongo.sh")

        ret = os.system("docker-compose -f ./docker/docker-compose.yaml -p integ_test down")
        if ret != 0:
            raise Exception("docker-compose down failed")
        print(f'\n{bcolors.OKBLUE}Integration-Test: Env shutdown complete..{bcolors.ENDC}\n')

    print(f'\n{bcolors.OKGREEN}Integration-Test: Integration test passed with no exceptions!{bcolors.ENDC}\n')


if __name__ == '__main__':
    main()
