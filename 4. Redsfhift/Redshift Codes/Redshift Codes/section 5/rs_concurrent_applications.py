import redshift_connector
import argparse, threading


def connect_to_redshift(redshift_host,user,pwd): 
    conn = redshift_connector.connect(
        host=redshift_host,
        port=5439,
        database='three_aayaam_db',
        user=user,
        password=pwd
    )

    cursor = conn.cursor()

    select_query = f"select c.customer_name, c.shipping_address, c.email, c.phone, \
    count(o.*) as order_count, sum(product_price) as order_total_price \
    from retail.customers c,  retail.orders o, retail.order_items oi, retail.products p \
    where c.customer_id = o.customer_id and   o.order_id = oi.order_id \
    and   oi.product_id = p.product_id group by c.customer_name, c.shipping_address, c.email, c.phone \
    order by order_total_price desc, order_count desc;"

    cursor.execute(select_query)


def create_and_execute_threads(concurrency,redshift_host,user,pwd):
    threads = []
    n = int(concurrency)
    for i in range(1, n):
        t_i = threading.Thread(target=connect_to_redshift,args=(redshift_host,user,pwd,))
        threads.append(t_i)
        t_i.start()
        print("thread created and started... ",t_i)

    for thread in threads:
        thread.join()


if __name__ == "__main__" : 
    # Parse arguments - host, user,pwd
    parser = argparse.ArgumentParser()
    parser.add_argument("-host",required=True)
    parser.add_argument("-u",required=True)
    parser.add_argument("-p",required=True)
    parser.add_argument("-con",required=True)
    args = parser.parse_args()
    redshift_host=args.host
    user = args.u
    pwd = args.p
    concurrency = args.con

    create_and_execute_threads(concurrency,redshift_host,user,pwd)