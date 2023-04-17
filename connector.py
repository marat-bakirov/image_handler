import psycopg2
import redis

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
)

db_connector = psycopg2.connect(
    host="localhost",
    database="image_registrator",
    user="root",
    password="root",
    port=5432
)

db_session = db_connector.cursor()
