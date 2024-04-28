# True Tech Hack 2024

...

## Architecture

![arch](https://www.plantuml.com/plantuml/svg/XP5DRi8m48NtFiM8RPKR80HjXLG9K2XqqLKriISeQcAd_g7qzXtRM91DkqZiUU-Rv8szT1wj3qClK7fZuSsH1NGGU1L2eSS67S5psSpdjN7-PEcmtomMaLID4D8Cez6aFJoY_2Ijc5kZywlw1Gvapvsa33Tit-DhQxJF_ExKwGiym2jnaaotqOsuzjRqSEm6iam-iPm1oRlxpytg7YL1ZPRZpnXTTMRed9o663_614mwruG-s7zxsrjlRu82df3HxV40c-vyPGRlflOxQaKNsEAOWPzK2_4LA13CTlGDARYBlzr7CNF95oBU1LIBSXnfWOg5V9hndSfq4socuZPasKKvPUFdBqGraxgaQ8ishwghraxRIfHfJm7Ar7b9Ih75ahGAG_yB)

## Database Schema

![database](https://www.plantuml.com/plantuml/svg/jLFHQi8m57tlLrny7FZWQn5HcS8sqO7ErvAPMmsqCUGc7QBxzwKQR5PBXSdwT7DExkqv9ycG3DF6vXbmPjWd8umYb4QO0tG-27K76865OmJkUmB1On3Iu1QrHyn1OGpbrfMhF6ZTKhBS4MIqa5iFAqRqjTSysJ7QrJczLwYDG8hXTRcOZps-qSWCyeIP69vTjHBvzI-AtrBVbVxtZ6tmR42r66ZGoP4sMYWZzhB6CCur4bNeenedXQlE6h55eogT904E_VxqRJ3uYuNpWJUBHSdhn0C6RGwTgUkp6jSiivUJI8khpT5wz38RZMUJ67eUcYzMIG1tUq5KVfOVqn8MPNORUgu7LByXuLpb1z_FFBrqtTzGbDvZ29EukG2X1AmaOCdzluIbo4N6TFLSoB-NzX1SqfV69jwDZnISJjtkwUXIZTAmBXeNc5OT6640fqrRIFsgXoYvpRCV)

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
