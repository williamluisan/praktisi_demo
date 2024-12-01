import pika
from pathlib import Path
from dotenv import dotenv_values

class Rmq:
    def connect_channel():
        dotenv_path = Path('./config/.env')
        config = dotenv_values(dotenv_path) 

        ### connections
        rmq = pika.BlockingConnection(pika.ConnectionParameters(config["RABBIT_MQ_URL"], config["RABBIT_MQ_PORT"]))
        rmq_chnl = rmq.channel()

        return rmq_chnl