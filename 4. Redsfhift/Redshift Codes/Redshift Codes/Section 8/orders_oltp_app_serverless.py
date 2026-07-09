import pymysql
import argparse
import time

# Connect to Aurora MySQL database
def connect_to_aurora(aurora_endpoint,aurora_port,database,user,pwd):  
    conn = pymysql.connect( 
        host=aurora_endpoint, 
        port=aurora_port,
        user=user,  
        password=pwd, 
        db=database
        )
    print('connected to aurora...')
    return conn 

# INSERT records from files to Aurora MySQL database
def insert_record(conn,input_file):
    ins_cur = conn.cursor()
    ins_count = 0
    with open(input_file) as input_file:
        for records in input_file:
            order_id, product_id = records.split(',')
            query=f"INSERT INTO order_items VALUES ('{order_id}', '{product_id}')"
            ins_cur.execute(query)
            ins_count = ins_count + 1
            conn.commit()
            if ins_count == 1000:
                print('{} records inserted to ORDER_ITEMS table... sleeping for 5 mins '.format(ins_count))
                time.sleep(300)
            
        

# UPDATE the records that have been INSERTed in Aurora MySQL database
def update_record(conn,input_file):
    upd_cur = conn.cursor()
    upd_count = 0
    with open(input_file) as input_file:
        for records in input_file:
            order_id, product_id = records.split(',')
            query=f"UPDATE order_items SET product_id = 2208 WHERE order_id = '{order_id}'"
            upd_cur.execute(query)
            upd_count = upd_count + 1
            conn.commit()
            if upd_count == 1000:
                print('{} records updated in ORDER_ITEMS table... sleeping for 5 mins '.format(upd_count))
                time.sleep(300)


if __name__ == "__main__" : 
    # Parse arguments - host, port, input file, database, user and password
    parser = argparse.ArgumentParser()
    parser.add_argument("-host",required=True)
    parser.add_argument("-port",type=int,required=True)
    parser.add_argument("-file",required=True)
    parser.add_argument("-db",required=True)
    parser.add_argument("-u",required=True)
    parser.add_argument("-p",required=True)
    parser.add_argument("-op",required=True)
    args = parser.parse_args()
    aurora_endpoint=args.host
    print('aurora cluster : ', aurora_endpoint)
    aurora_port=args.port
    input_file=args.file
    print('file name : ',input_file)
    database = args.db
    user = args.u
    pwd = args.p
    operation = args.op
    operation = operation.upper()
    
    # Connect to database
    conn = connect_to_aurora(aurora_endpoint,aurora_port,database,user,pwd)
    
    # INSERT records
    if operation == "I":
        insert_record(conn,input_file)
    
    # UPDATE records
    if operation == "U":
        update_record(conn,input_file)