FROM python:3.11

WORKDIR /usr/src/app/

RUN apt-get update && \
    apt-get -y install python3-dev

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 

WORKDIR tfmkt_scraper/tfmkt_scraper/

ENTRYPOINT ["python3", "crawl.py"]
