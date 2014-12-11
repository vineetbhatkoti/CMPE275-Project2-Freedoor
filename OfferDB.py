import pymysql
import json
import DBConnectionPool
from bottle import error,response
from Constants import Constants
from datetime import datetime

def cust_error(statuscode,message):
	error = dict()
	error[Constants.STATUS] = statuscode
	error[Constants.MESSAGE] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
	return errorResponse

def cust_success(statuscode,message):
	success = dict();
	success[Constants.STATUS] = statuscode
	success[Constants.MESSAGE] = message
	successResponse = json.dumps(success, indent = 4)
	response.status =statuscode
	response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
	#print successResponse
	return successResponse

def deleteOffer(offerId):
	try:
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("DELETE FROM Offer WHERE offerId=%s",(offerId))
		cursor.connection.commit()
		cursor.close()
		response=cust_success(Constants.SUCCESS,Constants.DELETEOFFER_SUCCESS)
		return response
	except:
		cursor.close()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.DELETEOFFER_FAIL)
		return errorResponse
	
def updateOffer(productId,offerId,jsonData):
	try:	
		cursor=DBConnectionPool.dbconnect()
		buyingQty = jsonData[Constants.BUYINGQTY]
		offeredDetails = jsonData[Constants.OFFEREDDETAILS]
		buyerStatus = jsonData[Constants.BUYERSTATUS]
		sellerStatus = jsonData[Constants.SELLERSTATUS]
		offerExpiry = str(jsonData[Constants.OFFEREXPIRY])
		#productId = jsonData['productId']
		buyerId = jsonData[Constants.BUYERID]

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
		cursor.execute("UPDATE Offer SET buyingQty=%s,offeredDetails=%s,buyerStatus=%s,sellerStatus=%s,offerExpiry=%s,productId=%s,buyerId=%s,lastModified=%s WHERE offerId=%s",(buyingQty,offeredDetails,buyerStatus,sellerStatus,offerExpiry,productId,buyerId,str(time),offerId))
		cursor.connection.commit()  
		cursor.execute('SELECT * from Offer where offerId=%s', (offerId))
		row = cursor.fetchone()
		if not row:
			errString = "Not a Valid productId " + productId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
			return errorResponse
		else:
			d = dict()
			d[Constants.OFFERID] = row[0]
			d[Constants.BUYINGQTY] = row[1]
			d[Constants.OFFEREDDETAILS] = str(row[2])
			d[Constants.BUYERSTATUS] = row[3]
			d[Constants.SELLERSTATUS] = row[4]
			d[Constants.OFFEREXPIRY] = str(row[5])
			d[Constants.PRODUCTID] = row[6]
			d[Constants.BUYERID] = row[7]
			d[Constants.LASTMODIFIED] = str(row[8])
			for commData in commentData:
				commList.append(commData[1])
			d[Constants.COMMENTS] = commList
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
		cursor.execute('SELECT * from Comment where offerId=%s',offerId)
		commentData = cursor.fetchall()
		commList = []
		if not row is None:
			d = dict()
			d[Constants.OFFERID] = row[0]
			d[Constants.BUYINGQTY] = row[1]
			d[Constants.OFFEREDDETAILS] = row[2]
			d[Constants.BUYERSTATUS] = row[3]
			d[Constants.SELLERSTATUS] = row[4]
			d[Constants.OFFEREXPIRY] = str(row[5])
			d[Constants.PRODUCTID] = row[6]
			d[Constants.BUYERID] = row[7]
			d[Constants.LASTMODIFIED] = str(row[8])
			d[Constants.LASTEVENT] = ""
			for commData in commentData:
				commList.append(commData[1])
			d[Constants.COMMENTS] = commList
			dbResponse = json.dumps(d, indent = 4)
			cursor.close()
			return dbResponse
		else:
			errorResponse = cust_error(Constants.NOT_FOUND,Constants.OFFER_NOT_FOUND)
			cursor.close()
			return errorResponse
	except:
		cursor.close()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.OFFER_FAIL_MESSAGE)
		return errorResponse

def createOfferByProductId(categoryId, productId,jsonData):
	try:
		cursor = DBConnectionPool.dbconnect()
		buyingQty = jsonData[Constants.BUYINGQTY]
		offeredDetails = jsonData[Constants.OFFEREDDETAILS]
		buyerStatus = jsonData[Constants.BUYERSTATUS]
		sellerStatus = jsonData[Constants.SELLERSTATUS]
		offerExpiry = str(jsonData[Constants.OFFEREXPIRY])
		buyerId = jsonData[Constants.BUYERID]
		commentDesc = jsonData[Constants.COMMENTS]
		now=datetime.now()
		time = now.strftime('%Y-%m-%d %H:%M:%S')
		
		try:
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
				jdict[Constants.OFFERID] = data[0]
				jdict[Constants.BUYINGQTY] = data[1]
				jdict[Constants.OFFEREDDETAILS] = data[2]
				jdict[Constants.BUYERSTATUS] = data[3]
				jdict[Constants.SELLERSTATUS] = data[4]
				jdict[Constants.OFFEREXPIRY] = str(data[5])
				jdict[Constants.PRODUCTID] = data[6]
				jdict[Constants.BUYERID] = data[7]
				jdict[Constants.LASTMODIFIED] = str(data[8])
				for commData in commentData:
					commList.append(commData[1])
				jdict[Constants.COMMENTS] = commList
				dbResponse=json.dumps(jdict,indent = 4)
				return dbResponse
			else:			
				errorResponse = cust_error(Constants.NOT_FOUND,"No such offer created !!!")
				return errorResponse
		except:
			errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong while processing at server side")
			return errorResponse
			cursor.close()		
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Internal Server Error !!!")
		return errorResponse


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
				jdict[Constants.OFFERID] = data[0]
				jdict[Constants.BUYINGQTY] = data[1]
				jdict[Constants.OFFEREDDETAILS] = data[2]
				jdict[Constants.BUYERSTATUS] = data[3]
				jdict[Constants.SELLERSTATUS] = data[4]
				jdict[Constants.OFFEREXPIRY] = str(data[5])
				jdict[Constants.PRODUCTID] = data[6]
				jdict[Constants.BUYERID] = data[7]
				jdict[Constants.LASTMODIFIED] = str(data[8])
				offerList.append(jdict)		
			offerDict[Constants.OFFERS] = offerList		
			dbResponse=json.dumps(offerDict,indent = 4)
			return dbResponse						
	except:
		db.rollback()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong while processing at server side")
		cursor.close()
		return errorResponse
