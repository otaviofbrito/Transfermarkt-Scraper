# :soccer: Soccer transfers scraper
![Neo4j|Scrapy](./img/project_logo.png)

An application that uses [Scrapy](https://scrapy.org/) framework to collect data from [Transfermarkt](https://www.transfermarkt.com/) website.

The main focus of this project is to collect and store data from every transfer available in the website.

To keep things related, we also collect data from players, clubs and leagues.
All the data collected is cleaned and exported in several formats:
  - File formats:
    - [JSON-lines](https://jsonlines.org/)
    - CSV
  - Databases:
    - [Neo4j](https://neo4j.com) graph database
    - [MySql](https://www.mysql.com/) relational database

---
## Neo4j
Neo4j graph data modelling
```mermaid
flowchart 
    CT((Country))
    P((Player))
    L((League))
    C((Club))
    C2((Club))
    T((Transfer))

    L-- PART_OF --> CT
    C-- COMPETED_IN --> L
    C-- COMPETED_IN_{YEAR} --> L
    T-- OF_PLAYER --> P
    T-- LEFT --> C
    T-- JOINED --> C2
    P-- HAS_CITIZENSHIP -->CT


```
---
## MySql
Relational data modelling
```mermaid
erDiagram 
    League }o--o{ Club_League : includes
    League {
        VARCHAR id PK
        VARCHAR url
        VARCHAR name
        VARCHAR country
        BIGINT current_mv
    }
    Club }o--o{ Club_League : competes
    Club {
        BIGINT id PK
        VARCHAR url
        VARCHAR name
        VARCHAR current_league
        BIGINT current_mv
    }
    Club_League {
        BIGINT club_id PK
        VARCHAR league_id PK
        INT season PK
        INT squad
        BIGINT market_value
    }
    Transfer }o--|{ Club : involves

    Transfer }o--|| Player : involves
    Transfer {
        BIGINT player_id PK
        INT year PK
        BIGINT left_club_id PK
        BIGINT joined_club_id PK
        BIGINT transfer_fee
        TINYINT transfer_type
    }
    Player {
        BIGINT id PK
        VARCHAR url
        VARCHAR name
        VARCHAR full_name
        DATE birthdate
        DATE deathdate
        INT height
        VARCHAR citizenship_1
        VARCHAR citizenship_2
        VARCHAR foot
        VARCHAR agent
        BIGINT current_club_id
        VARCHAR outfitter
        VARCHAR main_position
        BIGINT current_mv
    }
```

---

### Docker

This project can be easily run via [Docker](https://www.docker.com/).

```console
##The scraper will automatically run using all five spiders.
docker compose up
```


If you don't want to collect data from all spiders, you can choose which one to run.

```console
## First start mysql database container
docker compose up -d mysql_db
```
Next select which spider you'd like to run
```console
## If arguments are omitted, it will run every spider.
docker compose run scrapy
```

There are 5 different spiders:

1. clubs
2. leagues
3. club_league
4. transfers
5. players

You can choose which spider will run by providing its name as an argument:

```console
##It will run only the transfers and clubs spiders.
docker compose run scrapy transfers clubs
```

### Get the scraped data
The scraped data is stored in a volume on the Docker host, and you can retrieve it using the following command:
```console
docker cp CONTAINER:/usr/src/app/tfmkt_scraper/tfmkt_scraper/data/ /destination/path/
```