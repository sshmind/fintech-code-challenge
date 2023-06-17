# CODE CHALLENGE SOLUTION
## Requirements
 Create a virtual environment
```sh
virtualenv .venv
```
Activate your virtual environment
```sh
source .venv/bin/activate
```
Install project requirements
```sh
pip install -r requirements.txt
```
## start project services
please enter to redis directory and run following command:
```sh
sudo docker-compose up -d
```
Then we have to go to the Kafka directory and run it as follows:
```sh
sudo docker-compose up -d
```
## Step one & two solution
Please enter the step_one directory
```sh
cd step_one
```
You can run the updater service as follows.
```sh
sudo docker-compose up
```
## step three solution
For this step, we need to use two terminals. 
One for the producer script and one for running consumer

```sh
cd step_three
```

Running producer
```sh
python producer.py
```
Running consumer
```sh
python consumer.py
```

## step four
In this section, we first enter the step_four directory.
```sh
cd step_four
```
In this section, you will also need two terminals. One to run the Django server and the other to run Celery workers
Run django server:
```sh
python manage.py runserver
```
Run Celery workers:
```sh
celery -A config worker -l info --beat
```
Both of these commands must be executed inside the step_four directory.