from ed_infrastructure.persistence.sqlalchemy.demo import get_config
from ed_infrastructure.persistence.sqlalchemy.seed.main import \
    seed_delivery_job
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


async def main():
    config = get_config()
    uow = UnitOfWork(config)

    await seed_delivery_job(uow)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
