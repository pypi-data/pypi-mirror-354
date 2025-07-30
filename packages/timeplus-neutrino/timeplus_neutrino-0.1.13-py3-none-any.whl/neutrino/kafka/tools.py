import json
import time
import logging

from confluent_kafka import Consumer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def explore_kafka_topic(topic: str, config: str, message_count: int = 1):

    """
    Consume messages from a specified Kafka topic.

    Args:
        topic (str): The name of the Kafka topic to consume messages from.
        config (str): The configuration dictionary for the Kafka consumer.
        message_count (int, optional): The number of messages to consume. Defaults to 1.

    Returns:
        list: A list of JSON objects representing the consumed messages.
    """

    conf = json.loads(config)  # Parse the JSON config
    conf["group.id"] = f"timeplus-{time.time()}"
    conf["auto.offset.reset"] = "earliest"  # read from earliest offset
    try:
        client = Consumer(conf)
        client.subscribe([topic])
        messages = []
        for i in range(message_count):
            logger.info(f"Consuming message {i + 1}")
            message = client.poll()
            if message is None:
                logger.info("No message received")
                continue
            if message.error():
                logger.error(f"Error consuming message: {message.error()}")
                continue
            else:
                logger.info(f"Received message {i + 1}")
                messages.append(json.loads(message.value()))
        client.close()
        return messages
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
        client.close()
        return []
