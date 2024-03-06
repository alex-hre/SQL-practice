GET_POST_USERS_QUERY = """
    SELECT users.id, users.reputation,
           TO_CHAR(users.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS creationdate,
           users.displayname,
           TO_CHAR(users.lastaccessdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lastaccessdate,
           users.websiteurl, users.location, users.aboutme, users.views, users.upvotes, users.downvotes, users.profileimageurl, users.age, users.accountid
        FROM users
    JOIN comments ON users.id = comments.userid
    WHERE comments.postid = $1
    ORDER BY comments.creationdate DESC;
"""

GET_FRIENDS_USERS_QUERY = """
    SELECT users.id, users.reputation,
           TO_CHAR(users.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS creationdate,
           users.displayname,
           TO_CHAR(users.lastaccessdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lastaccessdate,
           users.websiteurl, users.location, users.aboutme, users.views, users.upvotes, users.downvotes, users.profileimageurl, users.age, users.accountid
    FROM
    (SELECT posts.owneruserid AS user_id
    FROM posts
    JOIN comments ON posts.id = comments.postid
    WHERE posts.owneruserid = $1

    UNION

    SELECT comments.userid AS user_id
    FROM comments
    JOIN posts ON comments.postid = posts.id
    WHERE posts.owneruserid = $1
    ) AS user_ids
JOIN users ON users.id = user_ids.user_id ORDER BY users.creationdate;
"""

GET_PERCENTAGE_TAGS_QUERY = """
    SELECT EXTRACT(DOW FROM posts.creationdate) AS day_of_week,
	ROUND((COUNT(CASE WHEN tags.tagname = $1 THEN 1 END) * 100.0 / COUNT(DISTINCT posts.id)), 2) AS percent_linux

	FROM tags
	JOIN post_tags ON tags.id = post_tags.tag_id
	JOIN posts ON post_tags.post_id = posts.id

	GROUP BY day_of_week
	ORDER BY day_of_week ASC
"""

GET_POST_DURATION_WITH_LIMIT_QUERY = """
    SELECT posts.id, TO_CHAR(posts.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS creationdate, posts.viewcount, TO_CHAR(posts.lasteditdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lasteditdate, TO_CHAR(posts.lastactivitydate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lastactivitydate, posts.title, TO_CHAR(posts.closeddate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS closeddate, ROUND((EXTRACT(EPOCH FROM (closeddate::timestamp - creationdate::timestamp)) / 60), 2) AS duration

	FROM posts
	WHERE closeddate IS NOT NULL AND EXTRACT(EPOCH FROM (closeddate::timestamp - creationdate::timestamp)) / 60 < $1

	ORDER BY creationdate DESC
	LIMIT $2
"""

GET_POST_ON_KEYWORD_WITH_LIMIT_QUERY = """
SELECT posts.id, TO_CHAR(posts.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS creationdate, posts.viewcount, TO_CHAR(posts.lasteditdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lasteditdate, TO_CHAR(posts.lastactivitydate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS lastactivitydate, posts.title, posts.body, posts.answercount, TO_CHAR(posts.closeddate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS closeddate, STRING_AGG(tags.tagname, ', ') AS tags_list
	FROM posts
	JOIN post_tags ON posts.id = post_tags.post_id JOIN tags ON post_tags.tag_id = tags.id
	WHERE (posts.body ILIKE '%' || $2 || '%' OR posts.title ILIKE '%' || $2 || '%')
	GROUP BY posts.id, posts.body, posts.title, posts.answercount
	ORDER BY posts.creationdate DESC
	LIMIT $1
"""
