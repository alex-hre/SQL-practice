from fastapi import APIRouter, Query

#####
from flask import Flask

from dbs_assignment.SQL_Z2 import GET_POST_USERS_QUERY, GET_FRIENDS_USERS_QUERY, GET_PERCENTAGE_TAGS_QUERY, \
    GET_POST_DURATION_WITH_LIMIT_QUERY, GET_POST_ON_KEYWORD_WITH_LIMIT_QUERY
from dbs_assignment.database_connect import get_postgres_version, execute_query

##app = Flask(__name__)
####

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





@router.get('/v2/posts/{post_id}/users')     ### /v2/posts/1819157/users
async def get_post_users(post_id: int):
    users = await execute_query(GET_POST_USERS_QUERY, post_id)

    formatted_users = []
    for user in users:
        formatted_user = {
            "id": user["id"],
            "reputation": user["reputation"],
            "creationdate": str(user["creationdate"]),
            "displayname": user["displayname"],
            "lastaccessdate": str(user["lastaccessdate"]),
            "websiteurl": user["websiteurl"],
            "location": user["location"],
            "aboutme": user["aboutme"],
            "views": user["views"],
            "upvotes": user["upvotes"],
            "downvotes": user["downvotes"],
            "profileimageurl": user["profileimageurl"],
            "age": user["age"],
            "accountid": user["accountid"]
        }
        formatted_users.append(formatted_user)

    response_data = {"items": formatted_users}

    return response_data

@router.get('/v2/friends/{users_id}/users')     ### /v2/friends/1076348/users
async def get_friends_users(users_id: int):
    users = await execute_query(GET_FRIENDS_USERS_QUERY, users_id)

    formatted_users = []
    for user in users:
        formatted_user = {
            "id": user["id"],
            "reputation": user["reputation"],
            "creationdate": str(user["creationdate"]),
            "displayname": user["displayname"],
            "lastaccessdate": str(user["lastaccessdate"]),
            "websiteurl": user["websiteurl"],
            "location": user["location"],
            "aboutme": user["aboutme"],
            "views": user["views"],
            "upvotes": user["upvotes"],
            "downvotes": user["downvotes"],
            "profileimageurl": user["profileimageurl"],
            "age": user["age"],
            "accountid": user["accountid"]
        }
        formatted_users.append(formatted_user)

    response_data = {"items": formatted_users}

    return response_data



@router.get('/v2/tags/{tagname}/stats')     ### /v2/tags/linux/stats
async def get_percentage_tags(tagname: str):
    statistics = await execute_query(GET_PERCENTAGE_TAGS_QUERY, tagname)

    day_of_week_names = {
        0: "sunday",
        1: "monday",
        2: "tuesday",
        3: "wednesday",
        4: "thursday",
        5: "friday",
        6: "saturday"
    }

    formatted_percentage = {}
    for row in statistics:
        day_of_week = row[0]
        percent_linux = row[1]

        day = day_of_week_names.get(day_of_week)

        formatted_percentage[day] = percent_linux

    sunday_value = formatted_percentage.pop("sunday")
    formatted_percentage["sunday"] = sunday_value

    response_data = {"result": formatted_percentage}

    return response_data





@router.get('/v2/posts/') ### /v2/posts/?duration=5&limit=2
async def get_posts_on_duration(duration: int = Query(...), limit: int = Query(...)):
    posts = await execute_query(GET_POST_DURATION_WITH_LIMIT_QUERY, duration, limit)

    formatted_posts = []
    for post in posts:
        formatted_user = {
            "id": post["id"],
            "creationdate": str(post["creationdate"]),
            "viewcount": post["viewcount"],
            "lasteditdate": str(post["lasteditdate"]),
            "lastactivitydate": str(post["lastactivitydate"]),
            "title": str(post["title"]),
            "closeddate": str(post["closeddate"]),
            "duration": post["duration"]
        }
        formatted_posts.append(formatted_user)

    response_data = {"items": formatted_posts}

    return response_data






@router.get('/v2/posts') ### /v2/posts?limit=1&query=linux
async def get_posts_on_keyword(limit: int = Query(...), query: str = Query(...)):
    posts = await execute_query(GET_POST_ON_KEYWORD_WITH_LIMIT_QUERY,limit, query)

    formatted_posts = []
    for post in posts:
        formatted_user = {
            "id": post["id"],
            "creationdate": str(post["creationdate"]),
            "viewcount": post["viewcount"],
            "lasteditdate": str(post["lasteditdate"]),
            "lastactivitydate": str(post["lastactivitydate"]),
            "title": str(post["title"]),
            "body": str(post["body"]),
            "answercount": post["answercount"],
            "closeddate": str(post["closeddate"]),
            "tags": str(post["tags_list"]),
        }
        formatted_posts.append(formatted_user)

    response_data = {"items": formatted_posts}

    return response_data

