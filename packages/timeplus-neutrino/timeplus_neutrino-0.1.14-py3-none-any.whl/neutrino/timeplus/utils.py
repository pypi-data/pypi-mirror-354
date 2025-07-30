def convert_confluent_to_stream_settings(confluent_config, **additional_settings):
    """
    Convert Confluent Python Kafka properties to external stream settings.

    Args:
        confluent_config (dict): Confluent Kafka Python configuration dictionary
        **additional_settings: Additional settings like topic, data_format, etc.

    Returns:
        dict: External stream settings dictionary
    """

    # Property mapping from Confluent Python to external stream settings
    property_mappings = {
        "bootstrap.servers": "brokers",
        "security.protocol": "security_protocol",
        "sasl.mechanism": "sasl_mechanism",
        "sasl.username": "username",
        "sasl.password": "password",
        "ssl.ca.location": "ssl_ca_cert_file",
        "ssl.ca.certificate.stores": "ssl_ca_pem",
        "ssl.ca.pem": "ssl_ca_pem",  # Alternative mapping
    }

    # Initialize stream settings with required type
    stream_settings = {"type": "kafka"}

    if "enable.ssl.certificate.verification" in confluent_config:
        stream_settings["skip_ssl_cert_check"] = (
            "false"
            if confluent_config["enable.ssl.certificate.verification"] == "true"
            else "true"
        )

    # Convert basic properties
    for confluent_prop, stream_prop in property_mappings.items():
        if confluent_prop in confluent_config:
            stream_settings[stream_prop] = confluent_config[confluent_prop]

    # Handle additional Kafka properties
    excluded_props = set(property_mappings.keys()) | {
        "enable.ssl.certificate.verification",
        "group.id",
        "client.id",
        "enable.auto.commit",
        "auto.offset.reset",
    }

    additional_kafka_props = {}
    for prop, value in confluent_config.items():
        if prop not in excluded_props:
            additional_kafka_props[prop] = value

    if additional_kafka_props:
        # Convert additional properties to string format
        props_str = ",".join([f"{k}={v}" for k, v in additional_kafka_props.items()])
        stream_settings["properties"] = props_str

    # Add additional settings passed as parameters
    for key, value in additional_settings.items():
        if key in [
            "topic",
            "data_format",
            "format_schema",
            "one_message_per_row",
            "kafka_schema_registry_url",
            "kafka_schema_registry_credentials",
            "config_file",
        ]:
            stream_settings[key] = value

    return stream_settings
