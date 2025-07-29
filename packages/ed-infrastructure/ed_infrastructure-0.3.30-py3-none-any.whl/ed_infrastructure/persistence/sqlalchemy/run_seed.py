from ed_infrastructure.persistence.sqlalchemy.demo import get_config
from ed_infrastructure.persistence.sqlalchemy.seed.main import async_seed
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


async def main():
    config = get_config()
    uow = UnitOfWork(config)

    await async_seed(uow)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
