from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
import os


def get_db_connection(user = None):
    
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER'] if user is None else user   # Use the user passed in if it's None, otherwise use default (postgres: Root access)
    db_password = os.environ['DB_PASSWORD'] if user is None else '12345'
    return psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)


def select(query, user):
    conn = None
    try:
        conn = get_db_connection(user)
        cursor = conn.cursor()
        cursor.execute(query)        
        columns = [i[0] for i in cursor.description]    # Get column names
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]   # Fetch data
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        return {'Error:', str(error)}
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def insert(query, user):
    conn = None
    try:
        conn = get_db_connection(user)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)        
        conn.commit()
        return {'Status': 'Success'}

    except (Exception, psycopg2.DatabaseError) as error:
        return {'Error:', str(error)}
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


@api_view(['GET'])
def genre_popularity(request):

    user = request.META.get('HTTP_USER')
    data = select('''
        -- Select most popular genres among users (rented or purchased)
        WITH u_m AS (
            -- Query total rented and purchased movies as (user_id, movie_id) unioned
            SELECT users.id AS user_id, purchases.movie_id
            FROM users
                INNER JOIN purchases ON purchases.user_id = users.id
                INNER JOIN movies ON movies.id = purchases.movie_id
            UNION ALL
            SELECT users.id AS user_id, rents.movie_id
            FROM users
                INNER JOIN rents ON rents.user_id = users.id
                INNER JOIN movies ON movies.id = rents.movie_id
        ),
        m_g AS (
            -- Query all the movies and their corresponding genres (a movie can have multiple genres, therefor can be repeated multiple times)
            SELECT movies.id AS movie_id, genre
            FROM movies
                INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
                INNER JOIN genres ON genres.id = movies_genres.genre_id
        ),
        report AS (
            SELECT genre, COUNT(user_id) AS popularity
            FROM u_m
                INNER JOIN m_g USING(movie_id)
            GROUP BY genre
        )
        SELECT genre, popularity, DENSE_RANK() OVER (ORDER BY popularity DESC) AS rank
        FROM (
            SELECT genre, COUNT(user_id) AS popularity
            FROM u_m
                INNER JOIN m_g USING(movie_id)
            GROUP BY genre
        ) AS report
        ORDER BY popularity DESC
    ''',
    user = user)

    return Response(data)


@api_view(['GET'])
def actors_rollup_genres(request):

    user = request.META.get('HTTP_USER')
    data = select(f'''
        WITH m_c AS (
        SELECT movie_id, CONCAT(first_name, ' ', last_name) AS full_name
        FROM casts
            INNER JOIN people ON people.id = casts.people_id
    ),
    m_g AS (
        SELECT movies.id AS movie_id, genre
        FROM movies
            INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
            INNER JOIN genres ON genres.id = movies_genres.genre_id
    ),
    total AS (
        SELECT full_name, genre, COUNT(genre) AS count
        FROM m_c
            INNER JOIN m_g USING(movie_id)
        GROUP BY full_name, genre
    )
    SELECT full_name, genre, SUM(count)
    FROM total
    GROUP BY ROLLUP(full_name, genre)
    ORDER BY full_name, genre
    ''',
    user = user)
    return Response(data)


@api_view(['GET'])
def actors_crosstab_genres(request):

    user = request.META.get('HTTP_USER')
    data = select(f'''
        -- Query the box-office for each movie cross-tabed by date
        SELECT *
        FROM CROSSTAB('
            WITH m_c AS (
                SELECT movie_id, CONCAT(first_name, '' '', last_name) AS full_name
                FROM casts
                    INNER JOIN people ON people.id = casts.people_id
            ),
            m_g AS (
                SELECT movies.id AS movie_id, genre
                FROM movies
                    INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
                    INNER JOIN genres ON genres.id = movies_genres.genre_id
            )
            SELECT full_name, genre, COUNT(genre)
            FROM m_c
                INNER JOIN m_g USING(movie_id)
            GROUP BY full_name, genre
            ',
            'SELECT genre FROM genres'
        ) AS report(
            "full_name" VARCHAR,
            "Animation" VARCHAR,
            "Shi-Fi" VARCHAR,
            "Mystry" VARCHAR,
            "Sport" VARCHAR,
            "Family" VARCHAR,
            "Film-Noir" VARCHAR,
            "Game-Show" VARCHAR,
            "Westerb" VARCHAR,
            "Romance" VARCHAR,
            "Music" VARCHAR,
            "War" VARCHAR,
            "Horror" VARCHAR,
            "Action" VARCHAR,
            "Fantacy" VARCHAR,
            "Biography" VARCHAR,
            "Adventure" VARCHAR,
            "Comedy" VARCHAR,
            "Musical" VARCHAR,
            "Thriller" VARCHAR,
            "Crime" VARCHAR,
            "Drama" VARCHAR,
            "History" VARCHAR
        )
    ''',
    user = user)
    return Response(data)


@api_view(['GET'])
def select_movies(request):

    title_cond = None
    type_cond = None
    writer_cond = None
    released_cond = None
    rated_cond = None
    language_cond = None
    country_cond = None

    if request.query_params.get('title'):
        title_cond = f"title = '{request.query_params.get('title')}'"
    if request.query_params.get('type'):
        type_cond = f"type = '{request.query_params.get('type')}'"
    if request.query_params.get('writer'):
        writer_cond = f"writer = '{request.query_params.get('writer')}'"
    if request.query_params.get('released'):
        released_cond = f"released = '{request.query_params.get('released')}'"
    if request.query_params.get('rated'):
        rated_cond = f"rated = '{request.query_params.get('rated')}'"
    if request.query_params.get('language'):
        language_cond = f"language = '{request.query_params.get('language')}'"
    if request.query_params.get('country'):
        country_cond = f"country = '{request.query_params.get('country')}'"
    
    conds = ' AND '.join([cond for cond in [title_cond, type_cond, writer_cond, released_cond, rated_cond, language_cond, country_cond] if cond is not None])

    if conds != '':
        conds = f'WHERE {conds}'

    user = request.META.get('HTTP_USER')
    data = select(f'''
        SELECT *
        FROM movies
        {conds}
    ''',
    user = user)
    return Response(data)


@api_view(['GET'])
def awards_per_actors(request):

    threshold = request.query_params.get('threshold')

    if threshold is None:
        return Response({'Error:': 'Please specify a threshold'})

    user = request.META.get('HTTP_USER')
    data = select(f'''
        SELECT * FROM awards_per_actors({threshold})
    ''',
    user = user)
    return Response(data)


@api_view(['GET'])
def movies_by_actor(request):

    first_name = request.query_params.get('first_name')
    last_name = request.query_params.get('last_name')

    if first_name is None or last_name is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = select(f'''
        SELECT * FROM movies_by_actor('{first_name}', '{last_name}')
    ''',
    user = user)
    return Response(data)


@api_view(['GET'])
def rents_between(request):

    rented_date = request.query_params.get('rented_date')
    returned_date = request.query_params.get('returned_date')

    if rented_date is None or returned_date is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = select(f'''
        SELECT * FROM rents_between('{rented_date}', '{returned_date}')
    ''',
    user = user)
    return Response(data)


@api_view(['POST'])
def add_purchase(request):

    user_id = int(request.POST.get('user_id'))
    movie_id = int(request.POST.get('movie_id'))

    if user_id is None or movie_id is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = insert(f'''
        call purchase({user_id}, {movie_id})
    ''',
    user = user)
    return Response(data)


@api_view(['POST'])
def add_rent(request):

    user_id = int(request.POST.get('user_id'))
    movie_id = int(request.POST.get('movie_id'))

    if user_id is None or movie_id is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = insert(f'''
        call rent({user_id}, {movie_id})
    ''',
    user = user)
    return Response(data)


@api_view(['POST'])
def add_movie(request):

    id = request.POST.get('id')
    title = request.POST.get('title')
    runtime = request.POST.get('runtime')

    if id is None or title is None or runtime is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = select(f'''
        INSERT INTO movies (id, title, runtime) VALUES ({id}, '{title}', {runtime})
    ''',
    user = user)
    return Response(data)


@api_view(['POST'])
def send_gift(request):

    user_id = request.POST.get('user_id')
    friend_id = request.POST.get('friend_id')
    movie_id = request.POST.get('movie_id')

    if id is None or user_id is None or friend_id is None or movie_id is None:
        return Response({'Error': 'Missing parameters'})

    user = request.META.get('HTTP_USER')
    data = insert(f'''
        CALL gift ({user_id}, {friend_id}, {movie_id})
    ''',
    user = user)
    return Response(data)


@api_view(['POST'])
def send_money(request):

    user_id = request.POST.get('user_id')
    friend_id = request.POST.get('friend_id')
    amount = request.POST.get('amount')

    if id is None or user_id is None or friend_id is None or amount is None:
        return Response({'Error': 'Missing parameters'})
    
    user = request.META.get('HTTP_USER')
    data = insert(f'''
        CALL send_money({user_id}, {friend_id}, {amount})
    ''',
    user = user)
    return Response(data)