import pymysql
import json
import DBConnectionPool

def cust_error(statuscode,message):
	error = dict();
	error['status'] = statuscode
	error['message'] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	return errorResponse

def deleteOffer(offerId):
	try:
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("DELETE FROM Offer WHERE offerId=%s",(offerId))
		cursor.connection.commit()
		cursor.close()
		response.headers['Content-Type'] = 'application/json'
		response.status=200
		return response
	except:
		cursor.close()
		errorResponse = cust_error(500,"Something went wrong in deleting Offer at server side")
		return errorResponse
	
def updateOffer(jsonData):
	try:
		offerId = jsonData['offerId']
		buyingQty = jsonData['buyingQty']
		offeredDetails = jsonData['offeredDetails']
		buyerStatus = jsonData['buyerStatus']
		sellerStatus = jsonData['sellerStatus']
		offerExpiry = jsonData['offerExpiry']
		productId = jsonData['productId']
		buyerId = jsonData['buyerId']
		lastModified = jsonData['lastModified']
	
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("UPDATE Offer SET buyingQty=%s, offeredDetails=%s, buyerStatus=%s, sellerStatus=%s, offerExpiry=%s, productId=%s, buyerId=%s, lastModified=%s WHERE offerId=%s",(buyingQty,offeredDetails,buyerStatus,sellerStatus,offerExpiry,productId,buyerId,lastModified,offerId))
		cursor.connection.commit()   
		cursor.close()       
	except:
		cursor.close()
		errorResponse = cust_error(500,"Something went wrong in updating Offer at server side")
		return errorResponse
	
def retrieveOffer(offerId):
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
			d['offerExpiry'] = row[5]
			d['productId'] = row[6]
			d['buyerId'] = row[7]
			d['lastModified'] = row[8]
			d['comments'] = ""
			d['lastEvent'] = ""
			response.headers['Content-Type'] = 'application/json'
			response.status=200
			dbResponse = json.dumps(d, indent = 4)
			return dbResponse
		cursor.close()
	except:
		cursor.close()
		errorResponse = cust_error(500,"Something went wrong in updating Offer at server side")
		return errorResponse