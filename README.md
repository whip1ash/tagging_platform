# tagging-platform

A useful tagging-platform

## Requirement
- Python3.7
- Docker

## Installation
```
$ git clone https://github.com/whip1ash/tagging_platform.git

$ cd tagging_platform

$ sudo docker-compose up -d 

$ pip3 install -r requirements.txt

$ cd src

# create table structure
$ ./bin/django-migrate.sh
```

### Import Data
#### Import Data from WikipediaSpider result

```
# cd src

# <filepath> is the location of WikipediaSpider result 
# Default is ./output.json
$ ./bin/import_wiki_data.py <filepath>
```

#### Import Data from SQL execute file
```

# This step will overwrite data in normal_sentence table, please backup if it's important.
$ mysql -uroot -p<your_database_password> -P 6606 -h127.0.0.1 -D tag < ./resource/normal_sentence.sql
```