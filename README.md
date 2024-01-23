# kafka_dummy_agent

The kafka dummy agent includes a dummy producer and a dummy consumer to generate and receive customizable dummy data streams for testing.

## Producer
The producer contains the following components:
* A folder includes dummy data (images, latent, texts)
* A folder for customized message templates (YAML)
* A script scans the template, reads data from the data folder, composes a message, and sends the message to the corresponding queue.

## Consumer:
The consumer contains is a script reads the message of the designated topic and displays the content.
