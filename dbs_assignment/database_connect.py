import asyncpg

from dotenv import load_dotenv

from dbs_assignment.config import settings

load_dotenv()


async def get_postgres_version():
    conn = await asyncpg.connect(
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    version = await conn.fetchval("SELECT version();")
    await conn.close()
    return version


################# Z2

async def connect_to_database():
    conn = await asyncpg.connect(
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    return conn


async def execute_query(query, *args):
    conn = await connect_to_database()
    try:
        result = await conn.fetch(query, *args)
        return result
    finally:
        await conn.close()
