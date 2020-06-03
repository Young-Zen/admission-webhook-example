# -*- coding: utf-8 -*-

import sys
import logging
import json
import psycopg2
import os

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logger.info('Loading function')
DB_HOST = os.environ.get('PG_CONNECT_STRING')


def main_handler(event,content):
    logger.info('start main_handler')
    logger.info('got event{}'.format(event))
    logger.info('got content{}'.format(content))
    # 连接数据库
    print('Start Serverlsess DB SDK function')

    conn = psycopg2.connect(DB_HOST)
    print("Opened database successfully")

    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS TOKENS
           (ID INT PRIMARY KEY     NOT NULL,
           tokens TEXT    NOT NULL);''')
    conn.commit()

    cur.execute("select * from TOKENS")
    myresult = cur.fetchall()
    for row in myresult:
       print("ID = " + str(row[0]))
       print("tokens = " + row[1])

    if not bool(cur.rowcount):
        print("insert default tokens")
        cur.execute("INSERT INTO TOKENS (ID,tokens) \
            VALUES (1, '1111')")
        cur.execute("INSERT INTO TOKENS (ID,tokens) \
            VALUES (2, '2222')")
        cur.execute("INSERT INTO TOKENS (ID,tokens) \
            VALUES (3, '3333')")
        cur.execute("INSERT INTO TOKENS (ID,tokens) \
            VALUES (4, '4444')")
        conn.commit()

    json_dict = json.loads(event["body"])
    cur.execute("SELECT * FROM TOKENS where tokens=%s",[json_dict["object"]["metadata"]["annotations"]["token"]])
    myresult = cur.fetchall()
    allow = "false"
    if len(myresult) > 0:
        allow = "true"
        query_id = myresult[0][0]
        cur.execute("DELETE FROM TOKENS where ID=%s",[query_id])
        conn.commit()
    conn.close()
    return {"errorCode":0,"errorMsg":json_dict["object"]["metadata"]["annotations"]["token"],"allow":allow}