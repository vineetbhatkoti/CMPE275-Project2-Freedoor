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

def cust_success(statuscode,message):
	success = dict();
	success['status'] = statuscode
	success['message'] = message
	successResponse = json.dumps(success, indent = 4)
	response.status =statuscode
	response.headers['Content-Type'] = 'application/json'
	print successResponse
	return successResponse	

def getProductById(categoryId, productId):
	try:
		cursor=DBConnectionPool.dbconnect()
		sql = "select * from Product where productId=%s and categoryId=%s"
		cursor.execute(sql, (productId,categoryId))
		row = cursor.fetchone()
		if not row:
			cursor.close()
			errString = "No Products for this categoryId " + categoryId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
			return errorResponse
		else:
			d = dict()
			d['productId'] = row[0]
			d['productName'] = row[1]
			d['quantity'] = row[2]
			d['userId'] = row[3]
			d['expectedOffer'] = row[4]
			d['productDesc'] = row[5]
			d['productExpiryDate'] = str(row[6])
			d['isValid'] = row[7]
			d['categoryId'] = row[8]
			d['lastUpdated'] = str(row[9])
			dbResponse = json.dumps(d, indent = 4)
			return dbResponse
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Product could not be found due to some exception")
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
		categoryID = categoryId
		now=datetime.now()
		time = now.strftime('%Y-%m-%d %H:%M:%S')

		cursor=DBConnectionPool.dbconnect()
		prodSql = """Insert into Product(productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		cursor.execute(prodSql, (productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryID,time))
		cursor.connection.commit()
		product_id = cursor.connection.insert_id()
		cursor.close()
		createdProduct = getProductById(categoryId,product_id)
		return createdProduct
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Product could not be created successfully due to exception.")
		cursor.close()
		return errorResponse

def updateProduct(categoryId,productId,jsonData):

		cursor = DBConnectionPool.dbconnect()
		quantity = jsonData['quantity']
		productName = jsonData['productName']
		userId = jsonData['userId']
		expectedOffer = jsonData['expectedOffer']
		productDesc = jsonData['productDesc']
		productExpiryDate = jsonData['productExpiryDate']
		isValid = jsonData['isValid']
		lastUpdated = jsonData['lastUpdated']
		
		try:
			query="""UPDATE Product SET productName="%s", quantity=%s, expectedOffer="%s", productDesc="%s", productExpiryDate="%s", isValid=%s, categoryId=%s, lastUpdated="%s" WHERE productId=%s AND userId=%s""" %(productName,quantity,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated,productId,userId)

			print query
 			cursor.execute(query)  
 			cursor.connection.commit()

			cursor.execute("SELECT * from Product where productId=%s AND userId=%s", (productId,userId))
			row = cursor.fetchone()
			if not row:
				errString = "Not a Valid productId " + productId + "!!!"
				errorResponse = cust_error(Constants.NOT_FOUND,errString)
				return errorResponse
			else:

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

				response = json.dumps(d, indent = 4)
		#	print response
		          	 	
				return response      
		except:
			cursor.connection.rollback()
			errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Exception thrown while processing at server side")
			return errorResponse
	 	
		cursor.close()
		
def getAllProductsByCategoryId(categoryId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute('SELECT * from Product where categoryId=%s',(categoryId))
		productData = cursor.fetchall()
		
		if not productData:
			errString = "No Products for this categoryId " + categoryId + "!!!"
			errorResponse = cust_error(Constants.NOT_FOUND,errString)
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
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong while processing at server side")
		cursor.close()
		return errorResponse


def deleteProduct(categoryId,productId):
	try:
		cursor = DBConnectionPool.dbconnect()
		print 'DELETE from Product where productId=%s and categoryId=%s ',productId,categoryId
		cursor.execute('DELETE from Product where productId=%s and categoryId=%s',(productId,categoryId))
		cursor.connection.commit()
		cursor.close()
		response=cust_success(Constants.SUCCESS,"Successfully deleted the product !!")
		return response
	except:
		cursor.close()
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,"Something went wrong in deleting Product at server side")
		return errorResponse