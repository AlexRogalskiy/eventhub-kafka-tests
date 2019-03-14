import os
import random
import string
import time
import uuid
import datetime, time

from locust import TaskSet, task, events, Locust

from additional_handlers import additional_success_handler, additional_failure_handler
from kafka_client import KafkaClient

WORK_DIR = os.path.dirname(__file__)

# read kafka brokers from config
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092").split(sep=",")

# read topic from config
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "test")

# read other environment variables
QUIET_MODE = True if os.getenv("QUIET_MODE", "true").lower() in ['1', 'true', 'yes'] else False
TASK_DELAY = int(os.getenv("TASK_DELAY", "0"))

# register additional logging handlers
if not QUIET_MODE:
    events.request_success += additional_success_handler
    events.request_failure += additional_failure_handler


class KafkaLocust(Locust):
    client = None

    def __init__(self, *args, **kwargs):
        super(KafkaLocust, self).__init__(*args, **kwargs)
        if not KafkaLocust.client:
            KafkaLocust.client = KafkaClient(KAFKA_BROKERS)


class KafkaBehaviour(TaskSet):

    @task
    def sendTemperature(self):
        eventId = str(uuid.uuid4())
        createdAt = str(datetime.datetime.utcnow().replace(microsecond=3).isoformat()) + "Z"

        deviceIndex = random.randint(0, 999)

        json={
            'eventId': eventId,
            'type': 'TEMP',
            'deviceId': 'contoso://device-id-{0}'.format(deviceIndex),
            'createdAt': createdAt,
            'value': random.uniform(10,100),
            'complexData': {            
                'moreData0': random.uniform(10,100), 
                'moreData1': random.uniform(10,100),
                'moreData2': random.uniform(10,100),
                'moreData3': random.uniform(10,100),
                'moreData4': random.uniform(10,100),
                'moreData5': random.uniform(10,100),
                'moreData6': random.uniform(10,100),
                'moreData7': random.uniform(10,100),
                'moreData8': random.uniform(10,100),            
                'moreData9': random.uniform(10,100)                        
            }
        }

        self.locust.client.send(OUTPUT_TOPIC, message=str(json))

    # @task
    # def sendCO2(self):
    #     eventId = str(uuid.uuid4())
    #     createdAt = str(datetime.datetime.utcnow().replace(microsecond=3).isoformat()) + "Z"

    #     deviceIndex = random.randint(0, 999) + 1000

    #     json={
    #         'eventId': eventId,
    #         'type': 'CO2',
    #         'deviceId': 'contoso://device-id-{0}'.format(deviceIndex),
    #         'createdAt': createdAt,
    #         'value': random.uniform(10,100),            
    #         'complexData': {            
    #             'moreData0': random.uniform(10,100), 
    #             'moreData1': random.uniform(10,100),
    #             'moreData2': random.uniform(10,100),
    #             'moreData3': random.uniform(10,100),
    #             'moreData4': random.uniform(10,100),
    #             'moreData5': random.uniform(10,100),
    #             'moreData6': random.uniform(10,100),
    #             'moreData7': random.uniform(10,100),
    #             'moreData8': random.uniform(10,100),            
    #             'moreData9': random.uniform(10,100)                        
    #         }
    #     }

    #     self.client.send(OUTPUT_TOPIC, message=str(json))

class KafkaUser(KafkaLocust):
    """
    Locust user class that pushes messages to Kafka
    """
    task_set = KafkaBehaviour
    min_wait = TASK_DELAY
    max_wait = TASK_DELAY
