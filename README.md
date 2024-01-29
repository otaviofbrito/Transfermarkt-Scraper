# :soccer: Soccer transfers scraper

An application that uses [scrapy](https://scrapy.org/) framework to collect data from [Transfermarkt](https://www.transfermarkt.com/) website.

The main focus of this project is to collect and store data from every transfer available in the website.
 - To keep things related, we also collect data from players, clubs and leagues. 
 - All the data collected is cleaned and exported in two formats ([json-lines](https://jsonlines.org/) and csv) and also stored into a [mySql](https://www.mysql.com/) database.
 

------
```mermaid
classDiagram
direction LR
    League <-- Club
    Transfer --> Player
    Transfer -- Club
    Club_League --> Club
    Club_League --> League
    class League{
      id
      url
      name
      country
      current_mv
    }
    class Club{
      id
      url
      name
      current_league
      current_mv

    }
    class Club_League{
      club_id
      league_id
      season
      squad_number
      market_value
    }
    class Player{
      id
      url
      name
      ...
    }
     class Transfer{
      player_id
      year
      left_club_id
      joined_club_id
      transfer_fee
      transfer_type
    }
```
------

## Installation

The project can be runned either locally or via [docker](https://www.docker.com/) container.

To run locally install the dependencies listed in [requirements.txt](/requirements.txt). You must  have a mysql-server instance running at default port: `3306`. 

```console
pip3 install requirements.txt
```

> :warning: **This project uses [ScrapeOps](https://scrapeops.io) fake headers**: In order to run the application you must provide an api key that can be generated [here](https://scrapeops.io/app/headers). 
 >>Inside [docker_compose.yaml](/docker-compose.yaml) set the environment variable `API_KEY` to your actual key.\
 >>If running locally, go directly to [settings.py](/tfmkt_scraper/tfmkt_scraper/settings.py) and set your scrape ops api key.


### Docker
```console
docker compose up
```

Be sure that all containers are up and run the next command to attach a shell from the scrapy application container:
```console
docker exec -ti <container-id> bash
```

Once everything is set up go to the [main directory](/tfmkt_scraper//tfmkt_scraper/) to be able to run scrapy commands 

```console
cd tfmkt_scraper/tfmkt_scraper/

```
Spiders crawl independently, collects the data and sends through the [item pipelines](/tfmkt_scraper//tfmkt_scraper//pipelines/) where the data is properly treated.

There are 5 different spiders which can be seen by running the scrapy command `scrapy list` :
  1. transferspider
  2. playerspider
  3. clubspider
  4. leaguespider
  5. club_leaguespider

You can start scraping by typing the command:
```console
scrapy crawl <spidername>

```