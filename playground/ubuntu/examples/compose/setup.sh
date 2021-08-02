input=".env"
while IFS= read -r line
do
  export "$line"
done < "$input"

docker exec `docker ps|grep mysql:8.0.19|awk '{ print $1 }'` mysql --password=$DB_PASSWORD -Bse "drop database $DB_NAME;" 2>/dev/null
echo "1. Creating Database $DB_NAME"
docker exec `docker ps|grep mysql:8.0.19|awk '{ print $1 }'` mysql --password=$DB_PASSWORD -Bse "create database $DB_NAME;" 2>/dev/null
echo "2. Loading Schema"
docker exec -i `docker ps|grep mysql:8.0.19|awk '{ print $1 }'` sh -c 'exec mysql --password="$DB_PASSWORD" $DB_NAME' < data/tables.sql 2>/dev/null
echo "3. Loading Data"
docker exec -i `docker ps|grep mysql:8.0.19|awk '{ print $1 }'` sh -c 'exec mysql --password="$DB_PASSWORD" $DB_NAME' < data/data.sql 2>/dev/null
