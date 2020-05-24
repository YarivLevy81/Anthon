docker exec -it integ_test_mongodb_1 sh -c "mongo --quiet --eval 'db.getMongo().getDBNames().forEach(function(i){db.getSiblingDB(i).dropDatabase()})'"
