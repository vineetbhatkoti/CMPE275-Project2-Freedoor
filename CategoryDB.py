import pymysql
import json
import DBConnectionPool
from bottle import error,response

def cust_error(statuscode,message):
	error = dict()
	error[Constants.STATUS] = statuscode
	error[Constants.MESSAGE] = message
	errorResponse = json.dumps(error, indent = 4)
	response.status =statuscode
	response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
	return errorResponse

def getAllCategories():
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute("Select * from Category")
		row = cursor.fetchall()
		if not row:
			errorResponse = cust_error(Constants.NOT_FOUND,Constants.CATEGORY_ERROR1)
			return errorResponse
		else:
			categoryDict = dict()
			categoryList = []
			for data in row:
				d = dict()
				d[Constants.CATEGORY_ID] = data[0]
				d[Constants.CATEGORY_NAME] = data[1]
				categoryList.append(d)
			categoryDict[Constants.CATEGORY] = categoryList	
			dbresponse = json.dumps(categoryDict, indent = 4)
			cursor.close()
			return dbresponse
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.CATEGORY_ERROR2)
		cursor.close()
		return errorResponse

def getCategoryById(categoryId):
	try:
		cursor = DBConnectionPool.dbconnect()
		cursor.execute("Select categoryId, categoryName from Category where categoryId=%s",categoryId)
		row = cursor.fetchone()
		if row is not None:
			d = dict()
			d[Constants.CATEGORY_ID] = row[0]
			d[Constants.CATEGORY_NAME] = row[1]
			response = json.dumps(d, indent = 4)
			cursor.close()
			return response
		else:
			errorResponse = cust_error(Constants.NOT_FOUND,Constants.CATEGORY_ERROR3)
			cursor.close()
			return errorResponse
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.COMMENTHISTORY_EXP1)
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
			d[Constants.CATEGORY_ID] = row[0]
			d[Constants.CATEGORY_NAME] = row[1]
			response = json.dumps(d, indent = 4)
			cursor.close()
			return response
		else:
			errorResponse = cust_error(Constants.NOT_FOUND,Constants.CATEGORY_ERROR4)
			cursor.close()
			return errorResponse
	except:
		errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.COMMENTHISTORY_EXP1)
		cursor.close()
		return errorResponse
