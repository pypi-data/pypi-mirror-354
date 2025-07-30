from neutrino.pipeline.ddl_translation import translate_ddl_sync

ddl = """CREATE EXTERNAL TABLE default.demo_cdc_mysql_retailer_orders_target_stream
(
  orderNumber uint32,
  orderDate uint32,
  requiredDate uint32,
  shippedDate uint32,
  status string,
  comments string,
  customerNumber uint32
)
SETTINGS type='clickhouse',
         address='clickhouse:9000',
         user='default',
         database='default',
         table='test'
"""

db_type = "clickhouse"

result = translate_ddl_sync(ddl, db_type)

print(result)