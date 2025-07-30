from neutrino.timeplus.utils import convert_confluent_to_stream_settings


confluent_config = {
        'bootstrap.servers': 'localhost:9092,broker2:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': 'my_username',
        'sasl.password': 'my_password',
        'ssl.ca.location': '/path/to/ca-cert.pem',
        'ssl.check.hostname': False,
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'session.timeout.ms': 30000,
        'heartbeat.interval.ms': 3000
    }
    
# Additional stream-specific settings
additional_settings = {
        'topic': 'user_events',
        'data_format': 'JSON',
        'one_message_per_row': True,
        'kafka_schema_registry_url': 'http://localhost:8081',
        'kafka_schema_registry_credentials': 'abc'
    }

stream_settings = convert_confluent_to_stream_settings(confluent_config, **additional_settings)
    
print("Converted Stream Settings:")
for key, value in stream_settings.items():
    print(f"  {key}: {value}")

print("\n" + "="*50 + "\n")