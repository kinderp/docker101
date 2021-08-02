# docker101 docker-compse example


Running `docker-compose` you'll get a `flask` application (port 5000) hosted on port 80 by `nginx`, a `mysql` and a `phpmyadmin` (port 8080) instances.

If you prefer, you can submit your SQL queries throughth `phpmyadmin`, but not all SQL syntax is covered by  the dockerized phpmyadmin SQL parser (e.g. CTE query). In that case, just use mysql client cli.

`docker exec -it $(docker ps | grep mysql:8.0.19 | awk '{ print $1 }') mysql -p`


## Setup


* Cd into example dir: 
 
  ```cd compse```

* Create a `.env` file with the following values:

   ```bash
   DB_USER=root
   DB_PASSWORD=db-78n9n
   DB_NAME=example
   DB_HOST=db
   MYSQL_DATABASE=example 
   MYSQL_ROOT_PASSWORD=db-78n9n
   ```
   
* Build and run: 

  ```docker-compose up```

* Load data: 

  ```sudo chmod u+x ./setup.sh && ./setup.sh```
  
## Tests

* Get all childrens of `node_id` 5, in english.

```bash
curl 'http://localhost/fetch?node_id=5&language=english' | python3 -m json.tool
```

```json
{
    "nodes": [
        {
            "node_id": 1,
            "name": "Marketing",
            "children_count": 0
        },
        {
            "node_id": 2,
            "name": "Helpdesk",
            "children_count": 0
        },
        {
            "node_id": 3,
            "name": "Managers",
            "children_count": 0
        },
        {
            "node_id": 4,
            "name": "Customer Account",
            "children_count": 0
        },
        {
            "node_id": 6,
            "name": "Accounting",
            "children_count": 0
        },
        {
            "node_id": 7,
            "name": "Sales",
            "children_count": 3
        },
        {
            "node_id": 10,
            "name": "Developers",
            "children_count": 0
        },
        {
            "node_id": 12,
            "name": "Quality Assurance",
            "children_count": 0
        }
    ],
    "error": ""
}
```

* Get all childrens of `node_id` = 7, in italian

```bash
curl 'http://localhost/fetch?node_id=7&language=italian' | python3 -m json.tool
```

```json
{
    "nodes": [
        {
            "node_id": 8,
            "name": "Italia",
            "children_count": 0
        },
        {
            "node_id": 9,
            "name": "Europa",
            "children_count": 0
        },
        {
            "node_id": 11,
            "name": "Nord America",
            "children_count": 0
        }
    ],
    "error": ""
}
```

* Get all childrens of `node_id` = 5 in italian whose `node_name` contains `Supporto`

```bash
curl 'http://localhost/fetch?node_id=5&language=italian&search_keyword=Supporto'|python3 -m json.tool
```

```json
{
    "nodes": [
        {
            "node_id": 2,
            "name": "Supporto tecnico",
            "children_count": 0
        },
        {
            "node_id": 7,
            "name": "Supporto Vendite",
            "children_count": 3
        }
    ],
    "error": ""
}
```
