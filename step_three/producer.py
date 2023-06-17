from confluent_kafka import Producer, Consumer
import json
import logging
import csv
from redis import Redis

logging.basicConfig(format='%(asctime)s %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='producer.log',
                            filemode='w')


logger = logging.getLogger()
logger.setLevel(logging.INFO)


p = Producer({'bootstrap.servers': '127.0.0.1:9092'})
print('kafka producer has been initiated ...')


def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)





def read_csv_file(file_path: str):
    with open(file_path, 'r') as file:
        
        csv_reader = csv.reader(file)
        next(csv_reader) # Skip headers

        data = list(csv_reader)  # Read all rows into a list

    return data


def config_redis_for_start_line(number, edit_mode=False):
    redis_client = Redis(host='127.0.0.1', port='6379', db=0)
    start_line = redis_client.get('start_line')

    if start_line is None or edit_mode:
        redis_client.set('start_line', number)
    
    return int(redis_client.get('start_line'))


def main():
    start_line = config_redis_for_start_line(0)
    try:
        csv_data = read_csv_file('price_data.csv')
        for line in range(start_line, len(csv_data)):
            record = csv_data[line]
            data = {
                'stock-name': record[1],
                'time': f'{record[0][:2]}:{record[0][2:4]}:{record[0][4:]}',
                'price': record[2]
            }

            m = json.dumps(data)
            p.poll(1)
            p.produce('main_topic', m.encode('utf-8'), callback=receipt)
            p.flush()
            start_line = line + 1
    
    except KeyboardInterrupt:
        config_redis_for_start_line(start_line, True)
        print('Keyboard Interrupted ...')

    except Exception as e:
        config_redis_for_start_line(start_line, True)
        print(start_line)


if __name__ == '__main__':
    main()