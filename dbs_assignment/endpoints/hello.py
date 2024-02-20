from fastapi import APIRouter

from dbs_assignment.database_connect import get_postgres_version

router = APIRouter()


@router.get("/v1/hello")
async def hello():
    return {
        'hello': "ggez" #settings.NAME
    }

@router.get("/v1/status")
async def postgres_version():
    version = await get_postgres_version()
    return {"version": version}
