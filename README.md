# priceWatch
An open source utility to watch ammunition prices.

This software is designed to be run by a cron job. It will cleanly place the information into  database where other applications can access it.

## Usage
All options and configuration details are stored in the settings yaml file.

All MariaDB style databases are supported.

In order to read the database you can use the included `sql.py` file. This file includes the relevant SQLAlchemy database mappings.

## Site Support
Each site is encompassed in a site module. Presently only the following sights have appropriate modules.

0. [BulkAmmo.com](bulkammo.com)

## Requirements

- pip

### Pip Packages
0. virtualenv
1. sqlalchemy
2. pyyaml
3. pymysql
4. beautifulsoup4
