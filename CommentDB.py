import pymysql
import json
import DBConnectionPool

from datetime import datetime

def cust_error(statuscode,message):
	error = dict()
	error['status'] = statuscode
	error['message'] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	return errorResponse

def createCommentByOfferId(categoryId,productId,offerId,jsonData):
	comment=jsonData['comment']
	userId=jsonData['userId']
	cursor=DBConnectionPool.dbconnect()
	now=datetime.now()
	time = now.strftime('%Y-%m-%d %H:%M:%S')
	
	try:
 		commentInserted="""INSERT INTO Comment (commentDesc,lastUpdated,offerId,userId) VALUES (%s,%s,%s,%s)"""
 		cursor.execute(commentInserted, (comment,time,offerId,userId))
 		cursor.connection.commit()
 		commentId = cursor.connection.insert_id()
 		cursor.execute('SELECT * from Comment where commentId=%s',commentId)
 		row = cursor.fetchone()
 		if row is not None:
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
 		else:
 			cursor.close()
 			errorResponse = cust_error(404,"Comment could not be created successfully")
 			return errorResponse
	except:
 		errorResponse = cust_error(500,"Comment could not be created due to some exception")
 		cursor.close()
 		return errorResponse
