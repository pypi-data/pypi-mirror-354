from neutrino.onboard.agent import DataOnboardingAgent

data = """{
		"customer_id": 999,
		"name": "Johnathan Rodriguez",
		"email": "thomasramirez@example.org",
		"phone": "001-845-290-8721x77863",
		"address": "743 Cervantes Causeway Apt. 762\nPort Lauren, NY 12698",
		"ip": "127.0.0.1",
		"time": "2023-01-01 00:00:00",
		"event_time": "2023-01-01 00:00:00",
		"uid": "2a02:aa08:e000:3100::2",
		"uid2":"1f71acbf-59fc-427d-a634-1679b48029a9"
}"""



agent = DataOnboardingAgent()
properties = {
  "type": "kafka",
  "brokers": "redpanda:9092",
  "topic": "customer"
}
inference_ddl, inference_json = agent.inference_external_stream(data, "customer", properties, "customer information from kafka", raw_format=True)
print(f"schema sql : {inference_ddl}")
print(f" schema json : {inference_json}")

