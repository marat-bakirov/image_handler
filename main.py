import time

from pathlib import Path
from threading import Thread

from connector import redis_client as redis, db_session, db_connector

ROOT_DIR = Path(__file__).parent
IMAGES_DIR = ROOT_DIR / 'images'

redis_pubsub = redis.pubsub()


def put_images_to_queue():
    """Read image from images folder and put it to redis queue"""
    images = IMAGES_DIR.glob("*")
    for image in images:
        print(f'Size of image file: {image.stat().st_size} bytes')
        with open(image, 'rb') as file:
            redis.publish('queue_images', file.read())


def handle_images():
    """Read images from redis queue, proccess it and put image size to database"""
    time.sleep(1)
    try:
        first_message = True
        while True:
            image = redis_pubsub.get_message(ignore_subscribe_messages=True, timeout=5)
            if not image:
                if first_message == True:
                    first_message = False
                    continue
                else:
                    break
            db_session.execute('INSERT INTO images (image_size) VALUES (%s)', (len(image['data']),))
    finally:
        redis_pubsub.unsubscribe('queue_images')


if __name__ == '__main__':
    """Main function, it start thread, and wait it"""
    print("Start processing images...")
    redis_pubsub.subscribe('queue_images')

    try:
        db_session.execute('CREATE TABLE images '
                           '(id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY, '
                           'image_size INTEGER NOT NULL, '
                           'time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
    except Exception as ex:
        if "already exists" in str(ex):
            print("Table 'images' already exists")
            db_connector.commit()

    handle_images_thread = Thread(target=put_images_to_queue)
    put_images_to_queue_thread = Thread(target=handle_images)
    handle_images_thread.start()
    put_images_to_queue_thread.start()
    handle_images_thread.join()
    put_images_to_queue_thread.join()

    db_connector.commit()

    db_connector.close()
    db_session.close()

    print("Stop processing images!")
