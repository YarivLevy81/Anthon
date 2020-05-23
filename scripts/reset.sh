docker exec -it docker_mongodb_1 sh -c "mongo --quiet --eval 'db.getMongo().getDBNames().forEach(function(i){db.getSiblingDB(i).dropDatabase()})'"
rm -rf ./docker/snapshots/*
rm -rf ./docker/users_data/*