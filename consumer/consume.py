import os
from datetime import datetime
import yaml
import json
import argparse
from kafka import KafkaConsumer

CONFIG_PATH = 'config.yaml'
OUTPUT_FOLDER_PATH = 'recv'
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

class Agent(object):
    def __init__(self, topic) -> None:
        # read from config file
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
            self.bootstrap_servers = config['bootstrap_servers']
            self.encoding = config['encoding']
            self.auto_offset_reset = config['auto_offset_reset']
        # create consumer
        self.consumer = KafkaConsumer(
            topic,
            auto_offset_reset= self.auto_offset_reset,
            bootstrap_servers= self.bootstrap_servers, 
            value_deserializer = lambda m: json.loads(m.decode(self.encoding))
        )
    
    def listen(self) -> None:
        for msg in self.consumer:
            # parse the message as a json object
            msg = msg.value
            # get current time up to milliseconds
            date_time = datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')
            # get output path
            output_file_path = os.path.join(OUTPUT_FOLDER_PATH, date_time + '.json')
            # write the message to file
            with open(output_file_path, 'w') as f:
                json.dump(msg, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, default='test', help='topic to listen to, default: test')
    args = parser.parse_args()
    agent = Agent(args.topic)
    agent.listen()