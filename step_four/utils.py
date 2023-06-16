import json
from redis import Redis
import time
import random

def check_user_credentials(username, stockname, quantity, api_version=1):

    user_state_result = 1
    if api_version == 2:
        user_state_result = verify_user(username)
    print(user_state_result, '------------------------------')
    if user_state_result:
        redis_client = Redis(host='127.0.0.1', port='6379', db='0')
        user_account = redis_client.get(username)

        user_data = json.loads(user_account)

        stock = redis_client.get(stockname)

        stock_data = json.loads(stock)

        last_stock_price = 0

        price_list = [x for x in stock_data['price'] if x != ""]
        last_stock_price = price_list[-1]
        print(last_stock_price)
        
        final_price_for_user = last_stock_price * quantity

        if user_data['credit'] >= final_price_for_user:
            user_data['credit'] -= final_price_for_user
        else:
            return False
        
        updated_user_data = json.dumps(user_data)
        redis_client.set(username, updated_user_data)

        return True
    else:
        return False


def verify_user(user_id):

    wait_number = random.randint(1, 100)

    if wait_number <= 5:
        time.sleep(wait_number)
        return 1
    
    return 0