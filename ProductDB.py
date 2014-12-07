import pymysql
import json
import DBConnectionPool
from bottle import error,response

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
		cursor.execute("INSERT into product(productName,quantity,userId,expectedOffer,productDesc,productExpiryDate,isValid,categoryId,lastUpdated) VALUES (?,?,?,?,?,?,?,?,?)",(product.productName,product.quantity,product.userId,product.expectedOffer,product.productDesc,product.productExpiryDate,product.isValid,product.categoryId,product.lastUpdated))
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
