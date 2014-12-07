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

def getAllCategories():
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute("Select categoryId, categoryName from Category")
		row = cursor.fetchone()
		d = dict()
		d['categoryId'] = row[0]
		d['categoryName'] = row[1]
		response = json.dumps(d, indent = 4)
		cursor.close()
		return response
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse

def getCategoryById(categoryId):
	try:
		cursor.execute("Select categoryId, categoryName from Category where categoryId=%s",categoryId)
		row = cursor.fetchone()
		d = dict()
		d['categoryId'] = row[0]
		d['categoryName'] = row[1]
		response = json.dumps(d, indent = 4)
		cursor.close()
		return response
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse
	
def createCategoryByName(categoryName):
	try:
		cursor.execute("insert into Category (categoryName) values(%s)",categoryName)	
		cursor.execute("Select * from Category where categoryName=%s",categoryName)
		row = cursor.fetchone()
		d = dict()
		d['categoryId'] = row[0]
		d['categoryName'] = row[1]
		response = json.dumps(d, indent = 4)
		cursor.close()
		return response
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse
