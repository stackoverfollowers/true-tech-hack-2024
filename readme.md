# True Tech Hack 2024

...

## Architecture

```plantuml
@startuml architecture

actor User as user

database Database <<PostgreSQL>> as db

component Backend <<FastAPI Service>> as back

component Frontend <<Nginx + React>> as front

control Timer <<Cron>> as cron

component "Place Parser" <<Aiomisc Service>> as p_parser

component "Feature Parser" <<Aiomisc Service>> as f_parser

cloud API <<MTS Live>> as mts

cloud API <<Yandex Map>> as yandex

queue "New Places" <<Queue>> as queue

user -> front

front --> back

back --> db

cron --> p_parser

p_parser --> mts
mts --> p_parser

p_parser --> db
p_parser --> queue

f_parser <-- queue
f_parser --> db

back --> queue

f_parser --> yandex
yandex --> f_parser

@enduml
```

## Database Schema

```plantuml
@startuml database

entity "User" as u {
    * id: integer
    * type: UserType
    * username: string
    * password_hash: string
    * properties: JSONB
    * created_at: DateTime
    * updated_at: DateTime
}

entity "Place" as p {
    * id: integer
    * name: string
    * description: string
    * address: string
    * created_at: DateTime
    * updated_at: DateTime
}

entity "Event" as e {
    * id: integer
    * place_id: integer <<FK>>
    * name: string
    * description: string
    * started_at: DateTime
    * ended_at: DateTime
    * created_at: DateTime
    * updated_at: DateTime
}

enum "FeatureValue" as fv {
    * AVAILABLE: 1
    * NOT_AVAILABLE: -1
}

entity "Feature" as f {
    * id: integer
    * slug: string
    * name: string
}

entity "PlaceFeature" as pf {
    * place_id: integer <<FK>>
    * feature_id: integer <<FK>>
    * feature_value: FeatureValue
}

entity "EventFeature" as ef {
    * event_id: integer <<FK>>
    * feature_id: integer <<FK>>
    * feature_value: FeatureValue
}

entity "SimilarPlace" as sp {
   * place_id: integer <<FK>>
   * similar_id: integer <<FK>>
}


p ||--|{ pf
f ||--|{ pf
fv ||--|{ pf
fv ||--|{ ef
p ||--|{ e
e ||--|{ ef
f ||--|{ ef
p ||--|{ sp
p ||--|{ sp
@enduml
```

## Stack

### Python libs

- [Aiomisc](https://aiomisc.readthedocs.io/en/latest/) for DI and service organization
- [FastAPI](https://aiomisc.readthedocs.io/en/latest/) with uvicorn for REST backend with Swagger (can be replaced with aiohttp)
- [SqlAlchemy](https://www.sqlalchemy.org/) with [Alembic](https://alembic.sqlalchemy.org) for database
- [Poetry](https://python-poetry.org/) for requirements management and project config

### JS stack

- ...

## Deployment


## Expluatation

After starting project via `docker-compose.yaml` you can open docs on:

- [Swagger](http://127.0.0.1/docs/swagger)
- [Redoc](http://127.0.0.1/docs/redoc)
- [OpenAPI JSON](http://127.0.0.1/docs/openapi.json)
