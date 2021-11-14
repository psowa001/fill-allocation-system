## **Fill allocation system**
Application is build with four main services. 
First one is generating transactions and pushing them to controller.
Second one is generating transaction account's splits and pushing them to controller.
Third one is spliting transaction between accounts and pushing them to position server.
Fourth is printing all positions for all accounts.

#### Fibonacci numbers generator developed with:
- FastAPI
- Asyncio
- Docker
- Docker-compose

#### To start services run:
```
docker-compose up -d 
```

#### To stop services and remove containers run:
```
docker-compose stop
docker-compose rm -f
```