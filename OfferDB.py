import pymysql
import json
import DBConnectionPool
from bottle import error,response
from Constants import Constants
from datetime import datetime

def cust_error(statuscode,message):
	error = dict();
	error['status'] = statuscode
	error['message'] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	return errorResponse
	
def cust_success(statuscode,message):
	success = dict();
	success['status'] = statuscode
	success['message'] = message
	successResponse = json.dumps(success, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	print successResponse
	return successResponse

def deleteOffer(offerId):
	try:
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("DELETE FROM Offer WHERE offerId=%s",(offerId))
		cursor.connection.commit()
		cursor.close()
		response=cust_success(Constants.SUCCESS,"Successfully deleted the Offer !!")
		return response
	except:
		cursor.close()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Offer could not be deleted due to some exception.")
		return errorResponse
	
def updateOffer(jsonData):
	try:
		cursor=DBConnectionPool.dbconnect()
		offerId = jsonData['offerId']
		buyingQty = jsonData['buyingQty']
		offeredDetails = jsonData['offeredDetails']
		buyerStatus = jsonData['buyerStatus']
		sellerStatus = jsonData['sellerStatus']
		offerExpiry = str(jsonData['offerExpiry'])
		productId = jsonData['productId']
		buyerId = jsonData['buyerId']
		lastModified = str(jsonData['lastModified'])
		if buyerStatus == sellerStatus:
			cursor.execute("SELECT quantity from Product WHERE productId =%s",(productId))
			fRow = cursor.fetchone()
			if not fRow:
				errString = "Not a Valid productId " + productId + "!!!"
				errorResponse = cust_error(Constants.NOT_FOUND,errString)
				return errorResponse	
			else:
				if int(fRow[0])-int(buyingQty) == 0:
					cursor.execute("UPDATE Product SET quantity=%s,isValid=%s WHERE productId=%s",(0,0,productId))
					cursor.connection.commit() 
				else:
					cursor.execute("UPDATE Product SET quantity=%s WHERE productId=%s",(int(fRow[0])-int(buyingQty),productId))
					cursor.connection.commit() 
		
		cursor.execute('SELECT buyingQty from Offer where offerId=%s',(offerId))
		offerQty=cursor.fetchone()
		
		
		modify=str("old"+`offerQty[0]`+":"+"new"+`buyingQty`)
	
		now=datetime.now()
		time = now.strftime('%Y-%m-%d %H:%M:%S')
		
		
		sqlForOfferHistory = """INSERT INTO OfferHistory(modified,lastModified,offerId) VALUES (%s,%s,%s)"""
		cursor.execute(sqlForOfferHistory, (modify,str(time),offerId))		
		cursor.connection.commit()  
		
		cursor.execute('SELECT * from Comment where offerId=%s',(offerId))
		commentData = cursor.fetchall()
		commList = []
		print "DB3*****"
		cursor.execute("UPDATE Offer SET buyingQty=%s,offeredDetails=%s,buyerStatus=%s,sellerStatus=%s,offerExpiry=%s,productId=%s,buyerId=%s,lastModified=%s WHERE offerId=%s",(buyingQty,offeredDetails,buyerStatus,sellerStatus,offerExpiry,productId,buyerId,lastModified,offerId))
		cursor.connection.commit()  
		cursor.execute('SELECT * from Offer where offerId=%s', (offerId))
		row = cursor.fetchone()
		if not row:
			errString = "Not a Valid productId " + productId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
			return errorResponse
		else:
			d = dict()
			d['offerId'] = row[0]
			d['buyingQty'] = row[1]
			d['offeredDetails'] = str(row[2])
			d['buyerStatus'] = row[3]
			d['sellerStatus'] = row[4]
			d['offerExpiry'] = str(row[5])
			d['productId'] = row[6]
			d['buyerId'] = row[7]
			d['lastModified'] = str(row[8])
			for commData in commentData:
				commList.append(commData[1])
			d['comments'] = commList
			response = json.dumps(d, indent = 4)
			cursor.close() 
			return response 
		      
	except:
			cursor.close()
			errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Offer could not be updated successfully due to some exception.")
			return errorResponse
	
def getOfferById(offerId):
	try:
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("SELECT * FROM Offer WHERE offerId=%s",(offerId))
		cursor.connection.commit()
		row = cursor.fetchone()
		if not row is None:
			d = dict()
			d['offerId'] = row[0]
			d['buyingQty'] = row[1]
			d['offeredDetails'] = row[2]
			d['buyerStatus'] = row[3]
			d['sellerStatus'] = row[4]
			d['offerExpiry'] = str(row[5])
			d['productId'] = row[6]
			d['buyerId'] = row[7]
			d['lastModified'] = str(row[8])
			d['comments'] = ""
			d['lastEvent'] = ""
			dbResponse = json.dumps(d, indent = 4)
			cursor.close()
			return dbResponse
		else:
			errorResponse = cust_error(Constants.NOT_FOUND,"Offer not found. Please check your offerid.")
			cursor.close()
			return errorResponse
	except:
		cursor.close()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Offer could not be retrieved successfully due to some exception.")
		return errorResponse

def createOfferByProductId(categoryId, productId,jsonData):
#	try:
		cursor = DBConnectionPool.dbconnect()
		buyingQty = jsonData['buyingQty']
		offeredDetails = jsonData['offeredDetails']
		buyerStatus = jsonData['buyerStatus']
		sellerStatus = jsonData['sellerStatus']
		offerExpiry = str(jsonData['offerExpiry'])
		buyerId = jsonData['buyerId']
		commentDesc = jsonData['comments']
		now=datetime.now()
		time = now.strftime('%Y-%m-%d %H:%M:%S')
		
#		try:
		sql = """Insert into Offer (buyingQty,offeredDetails,buyerStatus,sellerStatus,offerExpiry,productId,buyerId,lastModified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
		cursor.execute(sql, (buyingQty,offeredDetails,buyerStatus,sellerStatus,offerExpiry,productId,buyerId,time))
		row = cursor.connection.commit()
		offerId = cursor.connection.insert_id()
		commentSql = """Insert into Comment (commentDesc,lastUpdated,offerId,userId) VALUES (%s,%s,%s,%s)"""
		cursor.execute(commentSql, (commentDesc,time,offerId,buyerId))
		row1 = cursor.connection.commit()
		cursor.execute('SELECT * from Offer where offerId=%s',offerId)
		data = cursor.fetchone()
	
		cursor.execute('SELECT * from Comment where offerId=%s',offerId)
		commentData = cursor.fetchall()
	
		commList = []
		if not data is None:
			jdict = dict()
			jdict['offerId'] = data[0]
			jdict['buyingQty'] = data[1]
			jdict['offeredDetails'] = data[2]
			jdict['buyerStatus'] = data[3]
			jdict['sellerStatus'] = data[4]
			jdict['offerExpiry'] = str(data[5])
			jdict['productId'] = data[6]
			jdict['buyerId'] = data[7]
			jdict['lastModified'] = str(data[8])
			for commData in commentData:
				commList.append(commData[1])
			jdict['comments'] = commList
			dbResponse=json.dumps(jdict,indent = 4)
			return dbResponse
		else:			
			errorResponse = cust_error(Constants.NOT_FOUND,"No such offer created !!!")
			return errorResponse
#		except:
#			errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong while processing at server side")
#			return errorResponse
#			cursor.close()		
#	except:
#		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Internal Server Error !!!")
#		return errorResponse


def getAllOffersByProductId(categoryId, productId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute('SELECT * from Offer where productId=%s order by lastModified DESC',productId)
		offerData = cursor.fetchall()
		if not offerData:
			errString = "No offers created for productId " + productId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
			return errorResponse
		else:	
			offerDict = dict()
			offerList = []
			for data in offerData:
				jdict = dict()
				jdict['offerId'] = data[0]
				jdict['buyingQty'] = data[1]
				jdict['offeredDetails'] = data[2]
				jdict['buyerStatus'] = data[3]
				jdict['sellerStatus'] = data[4]
				jdict['offerExpiry'] = str(data[5])
				jdict['productId'] = data[6]
				jdict['buyerId'] = data[7]
				jdict['lastModified'] = str(data[8])
				offerList.append(jdict)		
			offerDict['offers'] = offerList		
			dbResponse=json.dumps(offerDict,indent = 4)
			return dbResponse						
	except:
		db.rollback()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong while processing at server side")
		cursor.close()
		return errorResponse