from redis import Redis
import multiprocessing
import time
import json


def save_data_to_redis(csv_row, current_time_str):
    
    redis_client = Redis(host='127.0.0.1', port='6379', db=0)
    DATA_KEYS = ['stock1', 'stock2', 'stock3']
    process = None
    
    if current_time_str == csv_row[0]:
        message = f"An update relevant to the current time was found - updated stock name: {csv_row[1]}."
        print(message)
        for stock in DATA_KEYS:
            if stock == csv_row[1]:
                current_value = redis_client.get(csv_row[1])
                data = json.loads(current_value)
                new_time = csv_row[0][:2] + ':' + csv_row[0][2:4] + ':' + csv_row[0][4:]
                if data['time'][-1] != new_time:
                    data['time'].append(new_time)
                    data['price'].append(csv_row[2])
                    print(f'Added new price and time for stock! | stock-name: {stock}')
                else:
                    print(f'The price of an old time was updated ! | stock-name: {stock}')
                    data['price'][-1] = csv_row[2]

                process = multiprocessing.Process(target=calculate_performance, args=(stock,))
                process.start()
                updated_value = json.dumps(data)

                redis_client.set(csv_row[1], updated_value)
                
            else:
                current_value = redis_client.get(stock)
                data = json.loads(current_value)
                new_time = csv_row[0][:2] + ':' + csv_row[0][2:4] + ':' + csv_row[0][4:]
                if data['time'][-1] != new_time:
                    data['time'].append(new_time)
                    data['price'].append('')

                updated_value = json.dumps(data)
                redis_client.set(stock, updated_value)

    else:
        updated_time = current_time_str[:2] + ':' + current_time_str[2:4] + ':' + current_time_str[4:]
        print(f"There are no updates for the current time  ...")
        for stock in DATA_KEYS:
            current_value = redis_client.get(stock)
            data = json.loads(current_value)
            data['price'].append('')
            data['time'].append(updated_time)
            updated_value = json.dumps(data)    
            redis_client.set(stock, updated_value)
    
    return process

def calculate_performance(stock_price):
	time.sleep(3)
	return 0  
