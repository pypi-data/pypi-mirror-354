import json
from neutrino.kafka.tools import explore_kafka_topic

kafka_topic = "demo.cdc.mysql.retailer.orders"
kafka_config = {
    "security.protocol": 'SASL_SSL',
    "bootstrap.servers":'kafka.demo.timeplus.com:9092',
    "sasl.mechanism": 'PLAIN',
    "sasl.username":  'demo',
    "sasl.password":  'demo123',
    "enable.ssl.certificate.verification": 'false'
}

msg = explore_kafka_topic(kafka_topic, json.dumps(kafka_config), 1)
print(msg)