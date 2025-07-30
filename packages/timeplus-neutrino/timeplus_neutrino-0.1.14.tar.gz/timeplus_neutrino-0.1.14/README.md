# neutrino
Neutrinos are nearly massless and can pass through matter effortlessly, representing smooth and efficient data onboarding.


# pipeline build

install neutrino 'pip install timeplus-neutrino'

1. run timeplus enterprise
2. export following environment
  
```sh
export TIMEPLUS_HOST=localhost
export TIMEPLUS_AISERVICE_USER=user
export TIMEPLUS_AISERVICE_PASSWORD=password
export TIMEPLUS_AISERVICE_DB=aiservice
```

3. run following python code

```python
import os
import json
from neutrino.conf import TimeplusAgentConfig
from neutrino.pipeline.cdc import build_debezium_pipeline_sync

from neutrino.utils.tools import extract_code_blocks_with_type

agent_config = TimeplusAgentConfig()
# config open ai compatible model
#agent_config.config("default", "https://generativelanguage.googleapis.com/v1beta/openai/", os.environ["GEMINI_API_KEY"], "gemini-2.5-pro-preview-06-05")
agent_config.config("default", "https://api.openai.com/v1", os.environ["OPENAI_API_KEY"], "gpt-4o")

# config kafka
kafka_topic = "mongodb.lumi_data.unstructured_data"
kafka_config = {
    "security.protocol": 'PLAINTEXT',
    "bootstrap.servers":'localhost:19092'
}

# config kafka with SASL
'''

kafka_topic = "demo.cdc.mysql.retailer.orders"
kafka_config = {
    "security.protocol": 'SASL_SSL',
    "bootstrap.servers":'kafka.demo.timeplus.com:9092',
    "sasl.mechanism": 'PLAIN',
    "sasl.username":  'demo',
    "sasl.password":  'demo123',
    "enable.ssl.certificate.verification": 'false'
}
'''

# external stream settings
settings = {
	"type" :'s3',
    "access_key_id" : 'minioadmin',
    "secret_access_key" : 'minioadmin',
    "region" : 'us-east-1',
    "bucket" : 'timeplus',
    "data_format" : 'JSONEachRow',
    "endpoint" : 'http://minio:9000',
    "write_to" : 'lumi/data.json',
    "use_environment_credentials" : False
}

result = build_debezium_pipeline_sync(kafka_topic, kafka_config, database="test", target_stream_settings=settings)

print(f"the pipeline building for topic {kafka_topic} result is: {result}")

extracted_codes =extract_code_blocks_with_type(result)
extracted_code_type, extracted_code_content = extracted_codes[0]
print(f"the extracted code type is: {extracted_code_type}")

extracted_code_content_obj = json.loads(extracted_code_content)
print(f"the extracted code content is: {json.dumps(extracted_code_content_obj, indent=2)}")  

print(f"the extracted source_stream is: {extracted_code_content_obj["source_stream"]}")
print(f"the extracted target_stream is: {extracted_code_content_obj["target_stream"]}")
print(f"the extracted extraction_mv is: {extracted_code_content_obj["extraction_mv"]}")
```