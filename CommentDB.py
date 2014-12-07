import pymysql
import json
import DBConnectionPool

from datetime import datetime

#db = pymysql.connect("cmpe275.ciupcmtzesph.us-west-1.rds.amazonaws.com","root","password","cmpe275")
#cursor = db.cursor()

def createCommentByOfferId(categoryId,productId,offerId,jsonData):
	comment=jsonData['comment']
 	userId=jsonData['userId']
 	cursor=DBConnectionPool.dbconnect()
 	now=datetime.now()
 	time = now.strftime('%Y-%m-%d %H:%M:%S')
 	
 	commentInserted="""INSERT INTO Comment (commentDesc,lastUpdated,offerId,userId) VALUES (%s,%s,%s,%s)"""
 	cursor.execute(commentInserted, (comment,time,offerId,userId))
 	cursor.connection.commit()
 	
 	commentId = cursor.connection.insert_id()
 	
 	cursor.execute('SELECT * from Comment where commentId=%s',commentId)
 	row = cursor.fetchone()
 	result = []
 	columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
 	result.append(dict(zip(columns,row)))
 	
 	for data in result:
 		jdict = dict()
 		jdict['commentId'] = data['commentId']
 		jdict['comment'] = data['commentDesc']
 		jdict['userId'] = data['userId']
 	return json.dumps(jdict,indent = 4)
 	cursor.close()