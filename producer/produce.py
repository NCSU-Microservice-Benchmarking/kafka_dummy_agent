import os
import yaml
import json
import base64
import argparse
from kafka import KafkaProducer

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
TEMPLATES_ROOT_PATH = os.path.join(os.path.dirname(__file__), 'templates')

class Agent(object):
    def __init__(self) -> None:
        # read from config file
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
            self.bootstrap_servers = config['bootstrap_servers']
            self.encoding = config['encoding']
        # create producer
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers, 
            value_serializer=lambda m: json.dumps(m).encode(self.encoding)
            )
        # define parameters awaiting to be filled from template
        self.topic = None
        self.data = {}

    def loadTemplate(self, template_name: str) -> None:
        template_path = os.path.join(TEMPLATES_ROOT_PATH, template_name + '.yaml')
        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)
            self.topic = template['topic']
            self.data = self.readData(template['data'])

    @staticmethod
    def readData(data: dict) -> dict:
        readout = {}
        for key, type_value in data.items():
            if type_value['type'] == 'int':
                readout[key] = int(type_value['value'])
            elif type_value['type'] == 'float':
                readout[key] = float(type_value['value'])
            elif type_value['type'] == 'string':
                readout[key] = str(type_value['value'])
            elif type_value['type'] == 'file':
                # read the file and encode it into base64
                with open(type_value['value'], 'rb') as f:
                    readout[key] = base64.b64encode(f.read())
            elif type_value['type'] == 'image':
                # read the image and encode it into base64 with "data:image/png;base64,"
                with open(type_value['value'], 'rb') as f:
                    readout[key] = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')
            else:
                raise ValueError('Unknown type: {}'.format(type_value['type']))
        return readout

    def produce(self) -> None:
        # check if the topic and data are ready
        if self.topic is None:
            raise ValueError('Topic is not defined')
        if self.data == {}:
            raise ValueError('Data is not defined')
        # send data
        self.producer.send(self.topic, value=self.data)
        self.producer.flush()

                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tmp', type=str, default='latent_generation_request', help='name of templates, check the templates folder for available templates')
    args = parser.parse_args()

    agent = Agent()
    agent.loadTemplate(args.tmp)
    agent.produce()