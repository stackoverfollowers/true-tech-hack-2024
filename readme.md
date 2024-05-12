# True Tech Hack 2024

Project of Team "Не грози Южному централу попивая сок у себя на Go"

## Architecture

![arch](https://www.plantuml.com/plantuml/png/VP3FRi8m3CRlUGgBwzGtG0Ys2Ga9KFcpmqvJchfTj2PXYSFs-7DIAiXbXpRnvv-Tpru6afwY6K1wzQa95KMFGaX5piDRG0yoGEHJY5QIR6H0U9qkytdj0lKUJuVjOf78jX52ENDn5Yt1irHVQ5lcrZBGgjx02VrLAnpXXjEF-DexIoE_xxNzXISu8ZiPwIvb4sx9km7Esg1dyeNb4L1yUsmtgmUf46hfsVwCqPLsHWTLchXyN39GL6wCx94VLwwtchIpZ-NlRd1bZ-xUOt2n1PwK-Ttv15jzlJ66WX3V4IF2R8y_aCq5E2GbTJ_Afj6qEunq1eL8YuTgCSsU3wXO65UN_ZdCQ-Ta3kuJJRSaPmFy_OUqJH5FBhf9crVLJUlAiibAKLC-BSGIRHlDy0S0)

## Database Schema

![database](https://www.plantuml.com/plantuml/png/jLB1QW8n5BplLpmy5ZnuNKHKgj1Mj53hTNarRpMm6qFoiaMq_zwi1WshA5IwfybCydPcahvbDEpA0WGoVg6b9275ahVG-hHaMe0M7EmIyDyJI962L4mhCe7XhQOKwgrpZmBf_59XwGNBHgfLe3LQ-xqn8bkZNJSriz5aM99DuVLZDXq6Vca8cKI6dCApHtDPdlwYnQNqS_R_Nk2I3W7qZG1NV0goIoCrourgA2Y48MiZza6FeygZWqUwuL7NIRA8Xsvt_DRh_IN2uSAlcoKb6i8Z0Lq9hJ4XEqCBBDpn9lBg57Em6BnC1iF9A8LEeAQpUHRHxKvKLPWLnjmeonPk5MTk5jHy8V5S7GRVxpm_dhg_eQgpfn0rSVa0OWjqja2rzdyMDEptxVP-vrCdUOohgmlApoSeeOZE8vpqIGbN5hy0)

## Stack

### Python libs

- [Aiomisc](https://aiomisc.readthedocs.io/en/latest/) for DI and service organization
- [FastAPI](https://aiomisc.readthedocs.io/en/latest/) with uvicorn for REST backend with Swagger (can be replaced with aiohttp)
- [SqlAlchemy](https://www.sqlalchemy.org/) with [Alembic](https://alembic.sqlalchemy.org) for database
- [Poetry](https://python-poetry.org/) for requirements management and project config
- [YoloV8 Ultralytics](https://github.com/ultralytics/ultralytics) for recognizing ramps and stairs

### JS stack

- ...

## Deployment

For deployment project you should:

1. Create `.env` file
2. Run `docker compose`
3. Apply database migrations

### Required Envs for Docker Compose

- `POSTGRES_USER` - user for postgresql
- `POSTGRES_PASSWORD` - password for postgresql
- `POSTGRES_DB` - database name for postgresql
- `RABBITMQ_USER` - rabbitmq user
- `RABBITMQ_PASSWORD` - rabbitmq password
- `APP_SECURITY_SECRET` - secret string for passwords
- `APP_SECURITY_PRIVATE_KEY` - base64 encoded RSA private key for JWT
- `APP_YOLO_MODEL_URL` - URL for downloading YOLO model (need for building)

### Start services

After creating `.env` file you can start project with command:

```bash
docker compose up -d --build
```

### Migrations

You need run command for applying migrations to database

```bash
make docker-alembic-upgrade-head
```

## Expluatation

After starting project via `docker-compose.yaml` you can open docs on:

- [Swagger](http://127.0.0.1/docs/swagger)
- [Redoc](http://127.0.0.1/docs/redoc)
- [OpenAPI JSON](http://127.0.0.1/docs/openapi.json)
