import json
import UserDB
import CommentDB
import ProductDB
import OfferDB
import CategoryDB

from bottle import route, run, template, request, response, get , post, error

# **************** User *******************************

@route('/users/<userId>',method='GET')
def getByUserId(userId):
    retData = UserDB.getByUserId(userId)
    return retData

@route('/users', method='POST')
def createUser():
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = UserDB.createUser(jsonData)
	return retData

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
	postData = request.body.read()
	jsonData = json.loads(postData)
	categoryName = jsonData['categoryName']
	retData = CategoryDB.createCategoryByName(categoryName)
	return retData

# **************** Product ****************************

@route('/category/<categoryId>/product', method='GET')
def getAllProductsByCategoryId(categoryId):
	retData = ProductDB.getAllProductsByCategoryId(categoryId)
	return retData

@route('/category/<categoryId>/product/<productId>', method='GET')
def getProductById(categoryId,productId):
	retData = ProductDB.getProductById(categoryId,productId)
	return retData

@route('/category/<categoryId>/product', method='POST')
def createProduct(categoryId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = ProductDB.createProduct(categoryId,jsonData)
	return retData
        
@route('/category/<categoryId>/product/<productId>', method='PUT')
def updateProduct(categoryId,productId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = ProductDB.updateProduct(categoryId,productId,jsonData)
	return retData

# *************** Comment *********************************

@route('/category/<categoryId>/product/<productId>/offer/<offerId>/comment', method='POST')
def createCommentByOfferId(categoryId,productId,offerId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = CommentDB.createCommentByOfferId(categoryId,productId,offerId,jsonData)
	return retData
	

# ********************* Offer *************************************
@route('/category/<categoryId>/product/<productId>/offer', method='POST')
def createOffer(categoryId,productId):
        postData = request.body.read()
        jsonData = json.loads(postData)
        
        retData1 = ProductDB.createOfferByProductId(categoryId,productId,jsonData)
        return str(retData1)

@route('/category/<categoryId>/product/<productId>/offer', method='GET')
def getOffer(categoryId,productId):
        retData1 = ProductDB.getOfferByProductId(categoryId,productId)
        print(retData1)
        return str(retData1)

@route('/category/<categoryId>/product/<productId>/offer/<offerId>', method='DELETE')
def deleteOffer(categoryId,productId,offerId):
	status = OfferDB.deleteOffer(offerId)
	return status
	
@route('/category/<categoryId>/product/<productId>/offer/<offerId>', methos='PUT')
def updateOffer(categoryId,productId,offerId):
	postData = request.body.read()
	jsonData = json.loads(postdata)
	retData = OfferDB.updateOffer(jsonData)
	return retData

@route('/category/<categoryId>/product/<productId>/offer/<offerId>', method='GET')
def retrieveOffer(categoryId,productId,offerId):
	retData = OfferDB.retrieveOffer(offerId)
	return retData
run(host='localhost', port=8090)