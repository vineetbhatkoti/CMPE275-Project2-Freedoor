import pymysql
import json
import DBConnectionPool
from bottle import response
from datetime import datetime
from Constants import Constants

def cust_error(statuscode,message):
	error = dict()
	error[Constants.STATUS] = statuscode
	error[Constants.MESSAGE] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
	return errorResponse


def getOfferHistoryByOfferId(offerId):
	try:
		cursor=DBConnectionPool.dbconnect()	
		cursor.execute("select * from OfferHistory where offerId=%s", offerId)
		historyData = cursor.fetchall()

		if not historyData:
			errString = "No History associated for this offerId " + offerId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
			return errorResponse
		else:	
			historyDict = dict()
			historyList = []
			for data in historyData:
				d = dict()
				d[Constants.OFFERHISTORYID] = data[0]
				d[Constants.MODIFIED] = data[1]
				d[Constants.LASTDATETIME] = str(data[2])
				d[Constants.OFFERID] = data[3]
				historyList.append(d)

			historyDict[Constants.OFFERHISTORY] = historyList	
			dbresponse = json.dumps(historyDict, indent = 4)

		cursor.close()
		return dbresponse
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.COMMENTHISTORY_EXP1)
		cursor.close()
		return errorResponse

def createCommentByOfferId(categoryId,productId,offerId,jsonData):
	comment=jsonData[Constants.COMMENT]
	userId=jsonData[Constants.USERID]
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
 				jdict[Constants.COMMENTID] = data[Constants.COMMENTID]
 				jdict[Constants.COMMENT] = data[Constants.COMMENTDESC]
 				jdict[Constants.USERID] = data[Constants.USERID]
 			return json.dumps(jdict,indent = 4)
 			cursor.close()
 		else:
 			cursor.close()
 			errorResponse = cust_error(Constants.NOT_FOUND,Constants.COMMENT_ERROR)
 			return errorResponse
	except:
 		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.COMMENT_EXCEPTION2)
 		cursor.close()
 		return errorResponse
