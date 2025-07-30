import os
from neutrino.timeplus.analyzer import Client

timeplus_host = os.getenv("TIMEPLUS_HOST") or "localhost"
timeplus_user = os.getenv("TIMEPLUS_AISERVICE_USER") or "proton"
timeplus_password = os.getenv("TIMEPLUS_AISERVICE_PASSWORD") or "timeplus@t+"

client = Client(username=timeplus_user, password=timeplus_password, host=timeplus_host)

result = client.analyze_sql(
    sql="SELECT abc",
)

print(result)