import datetime
from csv_handler import read_csv_file
from redis_handler import save_data_to_redis




def main():
    csv_data = read_csv_file('price_data.csv')

    start_time = datetime.datetime.strptime("09:00:00", "%H:%M:%S")
    end_time = datetime.datetime.strptime("09:59:47", "%H:%M:%S")

    current_time = start_time
    current_time_str = current_time.strftime("%H%M%S")
    counter = 0
    processes = []
    while current_time <= end_time:

        try:
            performance_process = save_data_to_redis(csv_data[counter], current_time_str)
            if performance_process is not None:
                processes.append(performance_process)
            if current_time_str == csv_data[counter][0]:
                counter += 1
            if current_time_str < csv_data[counter][0]:
                current_time += datetime.timedelta(seconds=1)
                current_time_str = current_time.strftime('%H%M%S')
        except IndexError as e:
            break
    
    
    message = 'Waiting for the end of unfinished child processes ...'
    print(message)
    for process in processes:
        process.join()
    




if __name__ == "__main__":
    main()