# vendor

### Setup

> docker-compose.yml up -d

By executing above command, project will be ready to be consumed.
If you want to use virtualenv, please follow instructions of Dockerfile and docker-compose.

#### Admin Account (use this to login on swagger. /swagger)

```
username='admin'
password='Vending!123'
```

#### Buyer Account

```
username='buyer'
password='Vending!123'
```

#### Seller Account

```
username='seller',
password='Vending!123'
```


### Docs
Multiple options to check:
- see swagger.yaml on project files
- go to path **/swagger** -> make sure to do Django Login with admin account
- go to path **/redoc**  -> make sure to do Django Login with admin account