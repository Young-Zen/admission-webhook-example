# -*- coding: utf-8 -*-

import sys
import logging
import json
from serverless_db_sdk import database

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

logger.info('Loading function')

def main_handler(event,content):
    logger.info('start main_handler')
    logger.info('got event{}'.format(event))
    logger.info('got content{}'.format(content))
    # 连接数据库
    print('Start Serverlsess DB SDK function')

    connection = database().connection(autocommit=True)
    cursor = connection.cursor()
    json_dict = json.loads(event["body"])

    cursor.execute('SELECT * FROM tokens where tokens="'+ json_dict["object"]["metadata"]["annotations"]["token"] +'"')
    myresult = cursor.fetchall()
    allow = "false"
    if len(myresult) > 0:
        allow = "true"
        # 删除 tokens
        query_id = myresult[0][0]
        logger.info('query_id{}'.format(query_id))
        cursor.execute('DELETE FROM tokens where id='+ str(query_id) +'')
    logger.info('got myresult{}'.format(myresult))
    data = {}
    for k,v in myresult:
        data[k] = v
    return {"errorCode":0,"errorMsg":json_dict["object"]["metadata"]["annotations"]["token"],"allow":allow}