# kafka_dummy_agent

The kafka dummy agent includes a dummy producer and a dummy consumer to generate and receive customizable dummy data streams for testing.

# prerequisites
* miniconda: https://docs.anaconda.com/free/miniconda/index.html

# Environment setup
To set up the environment, use the following commands:
```bash
conda env create -f environment.yml
conda activate kafka
```

## Producer
The producer contains the following components:
* A folder includes dummy data (images, latent, texts)
* A folder for customized message templates (YAML)
* A script scans the template, reads data from the data folder, composes a message, and sends the message to the corresponding queue.

### Usage
To run the producer, enter the producer folder and use the following command:
```bash
python produce.py --tmp <name of the template file>
```

## Consumer:
The consumer contains is a script reads the message of the designated topic and displays the content.

### Usage
To run the consumer, enter the consumer folder and use the following command:
```bash
python consume.py --topic <name of the topic to listen to>
```

