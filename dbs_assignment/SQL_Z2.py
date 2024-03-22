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
    (SELECT comments.userid AS user_id
    FROM posts
    JOIN comments ON posts.id = comments.postid
    WHERE comments.userid = $1

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
	WHERE (unaccent(posts.body) ILIKE '%' || unaccent($2) || '%' OR posts.title ILIKE '%' || unaccent($2) || '%')+
	GROUP BY posts.id, posts.creationdate, posts.viewcount, posts.lasteditdate, posts.title, posts.body, posts.answercount, posts.closeddate, posts.lastactivitydate
	ORDER BY posts.creationdate DESC
	LIMIT $1
"""





################# Z3

GET_BADGE_POSTS_HISTORY_WITH_LIMIT_QUERY = """
SELECT id, title, type, created_at, CEIL(ROW_NUMBER() OVER (ORDER BY created_at) / 2.0) AS position
FROM(
    SELECT *, LAG(type) OVER (ORDER BY created_at) AS previous_type, LEAD(type) OVER (ORDER BY created_at) AS next_type
    FROM(
	    SELECT posts.id AS id,
            posts.title AS title,
            'post' AS type,
            TO_CHAR(posts.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS created_at
	    FROM posts
	    JOIN users ON posts.owneruserid = users.id
	    WHERE users.id = $1

	    UNION

	    SELECT badges.id AS id,
            badges.name AS title,
            'badge' AS type,
            TO_CHAR(badges.date AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS created_at
	    FROM badges
	    JOIN users ON badges.userid = users.id
	    WHERE users.id = $1
        ORDER BY type, title
    ) as final
) as finality
WHERE (previous_type = 'post' AND type = 'badge') OR (next_type = 'badge' AND type = 'post')
ORDER BY created_at
"""



GET_COMMENTS_BY_TAGS_MORE_THAN_COUNT_QUERY = """
SELECT post_id, title, displayname, text, TO_CHAR(created_at AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS created_at, (created_at - previous_time) AS diff, AVG(created_at - previous_time) OVER (PARTITION BY post_id ORDER BY created_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS avg
FROM(
	SELECT users.displayname AS displayname, posts.id AS post_id, posts.title AS title, comments.text AS text, comments.creationdate AS created_at, posts.creationdate, LAG(comments.creationdate, 1, posts.creationdate) OVER (PARTITION BY posts.id ORDER BY comments.creationdate) AS previous_time
	FROM post_tags
		JOIN posts ON post_tags.post_id = posts.id
		JOIN tags ON tags.id = post_tags.tag_id
		JOIN comments ON posts.id = comments.postid
		LEFT JOIN users ON comments.userid = users.id

	WHERE tags.tagname = $1 AND posts.commentcount > $2
	ORDER BY comments.creationdate
) AS main
"""


GET_K_COMMENT_TO_POSTS_BY_TAGS_WITH_LIMIT_QUERY = """
    SELECT comments.id, users.displayname, base.body, comments.text, comments.score, ARRAY_POSITION(base.comment_ids, comments.id) AS position
    FROM comments
    LEFT JOIN users ON comments.userid = users.id
    JOIN(
        SELECT posts.id as post_id, posts.body,  ARRAY_AGG(comments.id ORDER BY comments.creationdate) AS comment_ids
        FROM tags
            JOIN post_tags ON tags.id = post_tags.tag_id
            JOIN posts ON post_tags.post_id = posts.id
            JOIN comments ON posts.id = comments.postid
        WHERE tags.tagname = $1
        GROUP BY posts.id, posts.body, posts.creationdate
        HAVING COUNT(*) >= $2
        ORDER BY posts.creationdate
        LIMIT $3
    ) base ON comments.id = base.comment_ids[$2]
"""



GET_POSTS_AND_PARENT_POSTS_BY_POSTID_WITH_LIMIT_QUERY = """
SELECT users.displayname, posts.body, TO_CHAR(posts.creationdate AT TIME ZONE 'UTC+0', 'YYYY-MM-DD"T"HH24:MI:SS.US+00:00') AS created_at
FROM posts
JOIN users ON posts.owneruserid = users.id
WHERE posts.id = $1 OR posts.parentid = $1
ORDER BY posts.creationdate
LIMIT $2
"""


