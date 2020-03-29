# Echo Tools Committee Dashboard Backend
Committee Dashboard Backend provides api methods for getting information about committee members activity

## Config
For running `local` version of Committee Dashboard Backend, define some environment variables:

**Parameter name** | **Description**
--- | ---
DATABASE_NAME | Name of influxdb database
DATABASE_USER_NAME | Name of database user
DATABASE_USER_PASSWORD | Password of database user
DATABASE_PORT | Port on which db layer should be locally running
REDIS_PORT | Port on which redis layer should be locally running
REDIS_DATABASE | Integer value that specify, which database should be used for store temporary data
CELERY_REDIS_DATABASE | Integer value that specify, which database shuld be used for store Celery data
COINMARKETCAP_API_KEY | Api Key for CoinMarketCap API
ECHO_URL | Websocket url for Echo node connection
SERVICE_PORT | Port on which service should be running

**Example:** export <ENV_VARIABLE>=VALUE

## Run service
**`Run:`**

	$ docker-compose -f docker-compose-dev.yml pull
	$ docker-compose -f docker-compose-dev.yml build --no-cache
	$ docker-compose -f docker-compose-dev.yml up -d

**`Stop:`**

	$ docker-compose -f docker-compose-dev.yml down -v

Swagger for this service placed by `<URL>/api/` url.