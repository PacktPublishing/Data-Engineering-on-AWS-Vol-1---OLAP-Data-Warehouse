import redshift_connector

conn = redshift_connector.connect(
    host='data-engg-on-aws-redshift-cluster.cffo4y05dmat.us-east-1.redshift.amazonaws.com',
    port=5439,
    database='three_aayaam_db',
    user='admin',
    password='Deepcontent2208'
 )

cursor = conn.cursor()
select_query = f"select * from retail.order_volume_details limit 10"
insert_query = f"insert into retail.orders select order_id, 0, seller_id, order_date, price, 'MANUAL' from retail.order_volume_details limit 100"
fetch_orders = f"select * from retail.orders limit 10"

cursor.execute(select_query)
query_output = cursor.fetchall()
print(query_output)

for record in query_output:
    print(record)
    
cursor.execute(insert_query)
cursor.execute(fetch_orders)
orders_output = cursor.fetchall()
for record in orders_output:
    print(record)
