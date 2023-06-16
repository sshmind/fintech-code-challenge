from confluent_kafka import Consumer

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'stock-price-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer has been initiated...')

c.subscribe(['main_topic'])

def main():
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        print(data)
    c.close()
        
if __name__ == '__main__':
    main()