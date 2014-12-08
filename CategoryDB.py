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

def getAllCategories():
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute("Select * from Category")
		row = cursor.fetchall()
		if not row:
			errorResponse = cust_error(404,"Catgory not found. Please create a new category.")
			return errorResponse
		else:
			categoryDict = dict()
			categoryList = []
			for data in row:
				d = dict()
				d['categoryId'] = data[0]
				d['categoryName'] = data[1]
				categoryList.append(d)
			categoryDict['category'] = categoryList	
			dbresponse = json.dumps(categoryDict, indent = 4)
			cursor.close()
			return dbresponse
	except:
		errorResponse = cust_error(500,"Category could not be found due to exception")
		cursor.close()
		return errorResponse

def getCategoryById(categoryId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute("Select categoryId, categoryName from Category where categoryId=%s",categoryId)
		row = cursor.fetchone()
		if row is not None:
			d = dict()
			d['categoryId'] = row[0]
			d['categoryName'] = row[1]
			response = json.dumps(d, indent = 4)
			cursor.close()
			return response
		else:
			errorResponse = cust_error(404,"Category not found. Please check your categoryid again.")
			cursor.close()
			return errorResponse
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse
	
def createCategoryByName(categoryName):
	try:
		cursor=DBConnectionPool.dbconnect()
		cursor.execute("insert into Category (categoryName) values(%s)",categoryName)
		cursor.connection.commit()
		cursor.execute("Select * from Category where categoryName=%s",categoryName)
		row = cursor.fetchone()
		if row is not None:
			d = dict()
			d['categoryId'] = row[0]
			d['categoryName'] = row[1]
			response = json.dumps(d, indent = 4)
			cursor.close()
			return response
		else:
			errorResponse = cust_error(404,"Category not created properly.")
			cursor.close()
			return errorResponse
	except:
		errorResponse = cust_error(500,"Something went wrong in processing at server side")
		cursor.close()
		return errorResponse
