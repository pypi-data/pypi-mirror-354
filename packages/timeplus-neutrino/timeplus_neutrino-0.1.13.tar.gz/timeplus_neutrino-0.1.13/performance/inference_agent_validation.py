import json
import os
import time
import json
import requests

from datetime import datetime
from neutrino.onboard.agent import DataOnboardingAgent
from neutrino.utils.tools import extract_code_blocks_with_type
from neutrino.conf import TimeplusAgentConfig

from neutrino.timeplus.analyzer import Client

from proton_driver import client


timeplus_host = os.getenv("TIMEPLUS_HOST") or "localhost"
timeplus_user = os.getenv("TIMEPLUS_AISERVICE_USER") or "proton"
timeplus_password = os.getenv("TIMEPLUS_AISERVICE_PASSWORD") or "timeplus@t+"

timeplusd_client = client.Client(
            host=timeplus_host,
            user=timeplus_user,
            password=timeplus_password,
            port=8463,
        )

analyzer_client = Client(username=timeplus_user, password=timeplus_password, host=timeplus_host)

test_db = "test_db"
inference_validation_report_stream = "inference_validation_report"



def test_case_to_table_name(test_case_name):
    """
    Convert a test case name to a valid database table name by:
    1. Converting to lowercase
    2. Replacing spaces with underscores
    3. Removing any characters that aren't alphanumeric or underscores
    4. Ensuring the name doesn't start with a digit (prefixes with 't_' if needed)
    
    Args:
        test_case_name (str): The name of the test case
        
    Returns:
        str: A valid database table name
    """
    # Convert to lowercase
    table_name = test_case_name.lower()
    
    # Replace spaces with underscores
    table_name = table_name.replace(' ', '_')
    
    # Remove any characters that aren't alphanumeric or underscores
    table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
    
    # Ensure the name doesn't start with a digit
    if table_name and table_name[0].isdigit():
        table_name = 't_' + table_name
        
    return table_name

def run_sql(client, sql):
    try:
        client.execute(sql)
        print(f"SQL executed successfully: {sql}")
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        raise e
    
def ingest_data(data, stream_name, database=test_db):
    sql =f"INSERT INTO {database}.{stream_name} FORMAT JSONEachRow"
    #ndjson_data = '\n'.join(json.dumps(row) for row in data)
    
    response = requests.post(
        f"http://{timeplus_host}:8123/?query={sql}",
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'},
        auth=(timeplus_user, timeplus_password)  
    )

    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code != 200:
        raise Exception(f"Failed to ingest data: {response.text}")
    else:   
        print("Data ingested successfully")
        
def get_stream_count(client, stream_name, database=test_db):
    sql = f"SELECT COUNT(*) FROM table({database}.{stream_name})"
    try:
        result = client.execute(sql)
        print(f"Stream count: {result[0][0]}")
        return result
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        raise e
    
def create_report_stream(client):
    sql = f"CREATE STREAM IF NOT EXISTS {inference_validation_report_stream} (report string)"
    try:
        client.execute(sql)
        print(f"Stream created successfully: {sql}")
    except Exception as e:
        print(f"Error creating stream: {sql}")
        raise e
    
def insert_report(client, report_item):
    sql = f"INSERT INTO {inference_validation_report_stream} (report) VALUES"
    try:
        client.execute(sql, [[report_item]])
        print(f"Report item inserted successfully: {report}")
    except Exception as e:
        print(f"Error inserting report: {report}")
        raise e


agent_config = TimeplusAgentConfig()
#agent_config.config("default", "https://0515-34-53-31-10.ngrok-free.app/v1", "ollama", "qwen3:8b")
agent_config.config("default", "https://api.openai.com/v1", os.getenv("OPENAI_API_KEY"), "gpt-4o-mini")
#agent_config.config("default", "https://api.groq.com/openai/v1", os.getenv("GROQ_API_KEY"), "llama-3.3-70b-versatile")

time.sleep(3) # wait for the agent to be saved

current_config = agent_config._get_config('default')
del current_config["api_key"]
current_time = datetime.now().strftime("%Y%m%d%H%M%S")

create_report_stream(timeplusd_client)

with open("inference.json", "r") as f:
    data = json.load(f)
    
print(f"there are total {len(data)} test cases")
    
# create test_db
run_sql(timeplusd_client, f"CREATE DATABASE IF NOT EXISTS {test_db}")

report = []

for testcase in data:
    agent = DataOnboardingAgent()
    stream_name = test_case_to_table_name(testcase["test_case_name"])
    report_item = {}
    report_item["test_case_name"] = testcase["test_case_name"]
    report_item["data_payload"] = testcase["data_payload"]
    report_item["expected_types"] = testcase["expected_types"]
    report_item["report_time"] = current_time
    report_item["report_config"] = current_config
    
    try:
        inference_ddl, inference_json = agent.inference(testcase["data_payload"],stream_name, database=test_db)
        report_item["schema_sql"] = inference_ddl
        report_item["schema_json"] = inference_json
        report_item["inference_status"] = "success"
    except Exception as e:
        report_item["inference_status"] = "failed"
        report_item["inference_error"] = str(e)
        report.append(report_item)
        insert_report(timeplusd_client, json.dumps(report_item))
        continue
    
    try:
        run_sql(timeplusd_client, inference_ddl)
        report_item["creation_status"] = "success"
    except Exception as e:
        report_item["creation_status"] = "failed"
        report_item["creation_error"] = str(e)
    
    time.sleep(3)
    
    if report_item["creation_status"] == "success":
        try:
            ingest_data(testcase["data_payload"], stream_name, database=test_db) 
            report_item["ingest_status"] = "success"
        except Exception as e:
            report_item["ingest_status"] = "failed"
            report_item["ingest_error"] = str(e)
            
        time.sleep(3)
        
        try:
            stream_count = get_stream_count(timeplusd_client, stream_name, database=test_db)
            report_item["stream_count"] = stream_count[0][0]
            report_item["expected_count"] = len(testcase["data_payload"])
            report_item["count_status"] = report_item["stream_count"] == report_item["expected_count"]
        except Exception as e:
            report_item["count_status"] = "failed"
            report_item["count_error"] = str(e)
            
        try:
            recommendation_result = agent.recommendations(data, inference_ddl)
            
            recommendation_result_json = json.loads(recommendation_result)
            failed_recommendations_count = 0
            failed_recommendations = []
            for recommendation in recommendation_result_json:
                sql = recommendation["sql"]
                try:
                    analyzer_client.analyze_sql(sql=sql)
                except Exception as e:
                    failed_recommendations_count += 1
                    failed_item = {}
                    failed_item["sql"] = sql
                    failed_item["error"] = str(e)
                    failed_recommendations.append(failed_item)
            
            report_item["failed_recommendations"] = failed_recommendations
            report_item["failed_recommendations_count"] = failed_recommendations_count
        except Exception as e:
            report_item["recommendation_status"] = "failed"
            report_item["recommendation_error"] = str(e)
    
    try:
        run_sql(timeplusd_client, f"DROP STREAM {test_db}.{stream_name}")
        report_item["drop_status"] = "success"
    except Exception as e:
        report_item["drop_status"] = "failed"
        report_item["drop_error"] = str(e)
        
    report.append(report_item)
    insert_report(timeplusd_client, json.dumps(report_item))
    
    
# drop test_db
run_sql(timeplusd_client, f"DROP DATABASE {test_db} CASCADE")
print("all test cases are done")
print(json.dumps(report, indent=4))

with open(f"report_{current_time}.json", "w") as f:
    json.dump(report, f, indent=4)
    

