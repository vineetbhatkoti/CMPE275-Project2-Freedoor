import json
import UserDB
import CommentDB
import ProductDB
import OfferDB
import CategoryDB
import OfferHistoryDB
from Constants import Constants
from bottle import route, run, template, request, response, get , post, error

def cust_error(statuscode,message):
    error = dict()
    error[Constants.STATUS] = statuscode
    error[Constants.MESSAGE] = message
    errorResponse = json.dumps(error, indent = 4)
    response.status =statuscode
    response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
    return errorResponse
# **************** User *******************************

@route('/users/<userId>',method='GET')
def getByUserId(userId):
	retData = UserDB.getByUserId(userId)
	return retData

@route('/users', method='POST')
def createUser():
	try:
		print "in making users"
		postData = request.body.read()
		jsonData = json.loads(postData)
		emailId=jsonData[Constants.EMAILID]
		print "Email Id is " +emailId
		if emailId is None or emailId=="":
			errorResponse = cust_error(Constants.BAD_DATA,Constants.EMAIL_VALIDATION)
			return errorResponse
		else:

			retData = UserDB.createUser(jsonData)
			return retData
	except:
		errorResponse = cust_error(Constants.BAD_DATA,Constants.REQUIRED_FIELD_MISSING)
		return errorResponse
# **************** Category ***************************

@route('/category', method='GET')
def getAllCategories():
	retData = CategoryDB.getAllCategories()
	return retData

@route('/category/<categoryId>', method='GET')
def getCategoryById(categoryId):
	retData = CategoryDB.getCategoryById(categoryId)
	return retData

@route('/category', method='POST')
def createCategoryByName():
	try:
		postData = request.body.read()
		jsonData = json.loads(postData)
		categoryName = jsonData[Constants.CATEGORY_NAME]
		print "Email Id is " +categoryName
		if categoryName is None or categoryName=="":
			errorResponse = cust_error(Constants.BAD_DATA,Constants.CATEGORY_NAME_VALIDATION)
			return errorResponse
		else:
			retData = CategoryDB.createCategoryByName(categoryName)
			return retData
	except:
		errorResponse = cust_error(Constants.BAD_DATA,Constants.REQUIRED_FIELD_MISSING)
		return errorResponse	

# **************** Product ****************************

def validate_productData(jsonData):
	productName = jsonData['productName']
	quantity = jsonData['quantity']
	userId = jsonData['userId']
	productExpiryDate = str(jsonData['productExpiryDate'])
	isValid = jsonData['isValid']
	#print "Email Id is " +categoryName
	if productName is None or productName=="" or quantity is None or quantity=="" or int(quantity) < 0 or userId is None or userId=="" or productExpiryDate is None or productExpiryDate =="" or isValid is None or isValid=="":
			return False	
	else:		
			return True

@route('/category/<categoryId>/product', method='GET')
def getAllProductsByCategoryId(categoryId):
	retData = ProductDB.getAllProductsByCategoryId(categoryId)
	return retData

@route('/category/<categoryId>/product/<productId>', method='DELETE')
def deleteProdcutOffer(categoryId,productId):
	retData1 = ProductDB.deleteProduct(categoryId,productId)
	return str(retData1)	

@route('/category/<categoryId>/product/<productId>', method='GET')
def getProductById(categoryId,productId):
	retData = ProductDB.getProductById(categoryId,productId)
	return retData

@route('/category/<categoryId>/product', method='POST')
def createProduct(categoryId):
	try:
		postData = request.body.read()
		jsonData = json.loads(postData)
		isJSONValid = validate_productData(jsonData)
		if isJSONValid:
			retData = ProductDB.createProduct(categoryId,jsonData)
			return retData
		else:
			errorResponse = cust_error(Constants.BAD_DATA,Constants.JSON_INVALID)
			return errorResponse
	except:
		errorResponse = cust_error(Constants.BAD_DATA,Constants.REQUIRED_FIELD_MISSING)
		return errorResponse				

@route('/category/<categoryId>/product/<productId>', method='PUT')
def updateProduct(categoryId,productId):
    postData = request.body.read()
    jsonData = json.loads(postData)
    response = ProductDB.updateProduct(categoryId,productId,jsonData)
    return response

# ********************* Offer *************************************
@route('/category/<categoryId>/product/<productId>/offer', method='GET')
def getAllOffersByProductId(categoryId,productId):
	retData = OfferDB.getAllOffersByProductId(categoryId,productId)
	return retData

@route('/category/<categoryId>/product/<productId>/offer/<offerId>', method='GET')
def getOfferById(categoryId,productId,offerId):
	retData = OfferDB.getOfferById(offerId)
	return retData

@route('/category/<categoryId>/product/<productId>/offer', method='POST')
def createOffer(categoryId,productId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = OfferDB.createOfferByProductId(categoryId,productId,jsonData)
	return retData

@route('/category/<categoryId>/product/<productId>/offer/<offerId>', method='PUT')
def updateOffer(categoryId,productId,offerId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = OfferDB.updateOffer(productId,offerId,jsonData)
	return retData

@route('/category/<categoryId>/product/<productId>/offer/<offerId>', method='DELETE')
def deleteOffer(categoryId,productId,offerId):
	status = OfferDB.deleteOffer(offerId)
	return status

# *************** Comment *********************************

@route('/category/<categoryId>/product/<productId>/offer/<offerId>/comment', method='POST')
def createCommentByOfferId(categoryId,productId,offerId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = CommentDB.createCommentByOfferId(categoryId,productId,offerId,jsonData)
	return retData

# ***************** Offer History *****************************

@route('/category/<categoryId>/product/<productId>/offer/<offerId>/history')
def getOfferHistoryByOfferId(categoryId, productId, offerId):
	retData1 = OfferHistoryDB.getOfferHistoryByOfferId(offerId)
	return retData1

run(host='localhost', port=8090)

