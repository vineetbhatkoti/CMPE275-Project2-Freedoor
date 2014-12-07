import pymysql
import json
import DBConnectionPool
from bottle import error,response
from datetime import datetime


def cust_error(statuscode,message):
	error = dict();
	error['status'] = statuscode
	error['message'] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	return errorResponse

def getProductById(categoryId, productId):
	try:
		cursor=DBConnectionPool.dbconnect()
		sql = "select * from Product where productId=%s and categoryId=%s"
		cursor.execute(sql, (productId,categoryId))
		row = cursor.fetchone()
		if not row is None:
			d = dict()
			d['productId'] = row[0]
			d['productName'] = row[1]
			d['quantity'] = row[2]
			d['userId'] = row[3]
			d['expectedOffer'] = row[4]
			d['productDesc'] = row[5]
			d['productExpiryDate'] = row[6]
			d['isValid'] = row[7]
			d['categoryId'] = row[8]
			d['lastUpdated'] = row[9]
			response.headers['Content-Type'] = 'application/json'
			response.status=200
			dbResponse = json.dumps(d, indent = 4)
			return dbResponse
		else:
			errorResponse = cust_error(404,"Product not found")
			return errorResponse
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse


def createProduct(categoryId,jsonData):
	try:
		productName = jsonData['productName']
		quantity = jsonData['quantity']
		userId = jsonData['userId']
		expectedOffer = jsonData['expectedOffer']
		productDesc = jsonData['productDesc']
		productExpiryDate = jsonData['productExpiryDate']
		isValid = jsonData['isValid']
		categoryId = jsonData['categoryId']
		lastUpdated = jsonData['lastUpdated']

		cursor=DBConnectionPool.dbconnect()
		prodSql = """Insert into Product (productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		cursor.execute(prodSql, (productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated))
		
		cursor.connection.commit()
		product_id = cursor.connection.insert_id()
		cursor.close()
		
		return getProductById(categoryId,product_id)
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse

def updateProduct(categoryId,productId,jsonData):
	productName = jsonData['productName']
	quantity = jsonData['quantity']
	userId = jsonData['userId']
	expectedOffer = jsonData['expectedOffer']
	productDesc = jsonData['productDesc']
	productExpiryDate = jsonData['productExpiryDate']
	isValid = jsonData['isValid']
	categoryId = jsonData['categoryId']
	lastUpdated = jsonData['lastUpdated']
	cursor=DBConnectionPool.dbconnect()
	try:
		cursor.execute("""UPDATE Product SET productName=%s, quantity=%s, userId=%s, expectedOffer=%s, productDesc=%s, productExpiryDate=%s), isValid=%s, categoryId=%s, lastUpdated=%s WHERE productId=%s""" %(productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated,productId))
		cursor.close()
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse


def createOfferByProductId(categoryId, productId,jsonData):

	try:

		cursor = DBConnectionPool.dbconnect()
		buyingQty = jsonData['buyingQty']
		offeredDetails = jsonData['offeredDetails']
		buyerStatus = jsonData['buyerStatus']
		sellerStatus = jsonData['sellerStatus']
		offerExpiry = jsonData['offerExpiry']
		buyerId = jsonData['buyerId']
		commentDesc = jsonData['comments']
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
				
				errorResponse = cust_error(404,"No such offer created !!!")
				return errorResponse
		except:
		
			errorResponse = cust_error(500,"Something went wrong while processing at server side")
			return errorResponse
			cursor.close()
		
	except:
		errorResponse = cust_error(500,"Internal Server Error !!!")
		return errorResponse


def getOfferByProductId(categoryId, productId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute('SELECT * from Offer where productId=%s order by lastModified DESC',productId)
		offerData = cursor.fetchall()
		
		if not offerData:
		
			errString = "No offers created for productId " + productId + "!!!"
			errorResponse = cust_error(404,errString)
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
		errorResponse = cust_error(500,"Something went wrong while processing at server side")
		cursor.close()
		return errorResponse
	
		
		
def getAllProductsByCategoryId(categoryId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute('SELECT * from Product where categoryId=%s',(categoryId))
		productData = cursor.fetchall()
		
		if not productData:
			errString = "No Products for this categoryId " + categoryId + "!!!"
			errorResponse = cust_error(404,errString)
			return errorResponse
		else:	
			productDict = dict()
			productList = []
			for data in productData:
				jdict = dict()
				jdict['productId'] = data[0]
				jdict['productName'] = str(data[1])
				jdict['quantity'] = data[2]
				jdict['userId'] = data[3]
				jdict['expectedOffer'] = str(data[4])
				jdict['productDesc'] = str(data[5])
				jdict['productExpiryDate'] = str(data[6])
				jdict['isValid'] = data[7]
				jdict['categoryId'] = data[8]
				jdict['lastUpdated'] = str(data[9])
				productList.append(jdict)
				
			productDict['products'] = productList		
			dbResponse=json.dumps(productDict,indent = 4)
			return dbResponse						
	except:
		errorResponse = cust_error(500,"Something went wrong while processing at server side")
		cursor.close()
		return errorResponse