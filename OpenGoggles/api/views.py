from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
import os


def get_db_connection():
    
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    return psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)


def select(query):
    conn = None
    try:
        conn = get_db_connection()
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



@api_view(['GET'])
def test(request):

    data = select('''
        SELECT *
        FROM movies
        LIMIT 5
    ''')
    return Response(data)