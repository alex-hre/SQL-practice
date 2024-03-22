from typing import Optional

from fastapi import APIRouter, Query

from dbs_assignment.SQL_Z2 import GET_POST_USERS_QUERY, GET_FRIENDS_USERS_QUERY, GET_PERCENTAGE_TAGS_QUERY, \
    GET_POST_DURATION_WITH_LIMIT_QUERY, GET_POST_ON_KEYWORD_WITH_LIMIT_QUERY, GET_BADGE_POSTS_HISTORY_WITH_LIMIT_QUERY, \
    GET_K_COMMENT_TO_POSTS_BY_TAGS_WITH_LIMIT_QUERY, GET_POSTS_AND_PARENT_POSTS_BY_POSTID_WITH_LIMIT_QUERY, \
    GET_COMMENTS_BY_TAGS_MORE_THAN_COUNT_QUERY
from dbs_assignment.database_connect import get_postgres_version, execute_query


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

@router.get('/v2/users/{users_id}/friends')     ### /v2/users/1076348/friends
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




"""
@router.get('/v2/posts/') ### /v2/posts/?duration=5&limit=2
async def get_posts_on_duration(duration: int, limit: int):
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
async def get_posts_on_keyword(limit: int, query: str):
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

"""

@router.get('/v2/posts')
async def get_posts(limit: int, duration: Optional[int] = None, query: Optional[str] = None):
    if duration is not None:
        posts = await execute_query(GET_POST_DURATION_WITH_LIMIT_QUERY, duration, limit)

        formatted_posts = []
        for post in posts:

            formatted_post = {
                "id": post["id"],
                "creationdate": str(post["creationdate"]),
                "viewcount": post["viewcount"],
                "lasteditdate": str(post["lasteditdate"]),
                "lastactivitydate": str(post["lastactivitydate"]),
                "title": str(post["title"]),
                "closeddate": str(post["closeddate"]),
                "duration": post["duration"]
            }
            formatted_posts.append(formatted_post)
        response_data = {"items": formatted_posts}
        return response_data
    elif query is not None:

        posts = await execute_query(GET_POST_ON_KEYWORD_WITH_LIMIT_QUERY, limit, query)

        formatted_posts = []
        for post in posts:

            formatted_post = {
                "id": post["id"],
                "creationdate": str(post["creationdate"]),
                "viewcount": post["viewcount"],
                "lasteditdate": str(post["lasteditdate"]),
                "lastactivitydate": str(post["lastactivitydate"]),
                "title": str(post["title"]),
                "body": str(post["body"]),
                "answercount": post["answercount"],
                "closeddate": str(post["closeddate"]),
                "tags": [str(post["tags_list"])]
            }
            formatted_posts.append(formatted_post)
        response_data = {"items": formatted_posts}
        return response_data

############################### Z3


@router.get('/v3/users/{user_id}/badge history')     ### /v3/users/120/badge history
async def get_posts_and_badges(user_id: int):
    posts_and_badges = await execute_query(GET_BADGE_POSTS_HISTORY_WITH_LIMIT_QUERY, user_id)

    formatted_posts_and_badges = []
    for post_and_badge in posts_and_badges:


        post_and_badge = {
            "id": post_and_badge["id"],
            "title": str(post_and_badge["title"]),
            "type": str(post_and_badge["type"]),
            "created_at": str(post_and_badge["created_at"]),
            "position": post_and_badge["position"],
        }
        formatted_posts_and_badges.append(post_and_badge)


    response_data = {"result": formatted_posts_and_badges}

    return response_data



@router.get('/v3/tags/{tag}/comments')     ### /v3/tags/networking/comments?count=40
async def get_comments_more_than_count(tag: str, count: int):
    comments_more_than_count = await execute_query(GET_COMMENTS_BY_TAGS_MORE_THAN_COUNT_QUERY, tag, count)

    formatted_comments_more_than_count = []
    for comment in comments_more_than_count:

        comment = {
            "post_id": comment["post_id"],
            "title": str(comment["title"]),
            "displayname": str(comment["displayname"]),
            "text": str(comment["text"]),
            "created_at": str(comment["created_at"]),
            "diff": str(comment["diff"]),
            "avg": str(comment["avg"])
        }
        formatted_comments_more_than_count.append(comment)

    response_data = {"result": formatted_comments_more_than_count}

    return response_data




@router.get('/v3/tags/{tagname}/comments/{position}')   ### /v3/tags/linux/comments/2?limit=1
async def get_comments(tagname: str, position: int, limit: int ):

    comments = await execute_query(GET_K_COMMENT_TO_POSTS_BY_TAGS_WITH_LIMIT_QUERY, tagname, position, limit)

    formatted_comments = []
    for comment in comments:

        formatted_comment = {
            "id": comment["id"],
            "displayname": str(comment["displayname"]),
            "body": str(comment["body"]),
            "text": str(comment["text"]),
            "score": comment["score"],
            "position": comment["position"]
        }
        formatted_comments.append(formatted_comment)
    response_data = {"items": formatted_comments}
    return response_data






@router.get('/v3/posts/{post_id}')   ### /v3/posts/2154?limit=2
async def get_posts_tree(post_id: int, limit: int):

    posts_tree = await execute_query(GET_POSTS_AND_PARENT_POSTS_BY_POSTID_WITH_LIMIT_QUERY, post_id, limit)

    formatted_posts_tree = []
    for post in posts_tree:

        formatted_comment = {
            "displayname": str(post["displayname"]),
            "body": str(post["body"]),
            "created_at": str(post["created_at"])
        }
        formatted_posts_tree.append(formatted_comment)
    response_data = {"items": formatted_posts_tree}
    return response_data








