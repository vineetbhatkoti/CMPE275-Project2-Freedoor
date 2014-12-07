import json

import UserDB
import CommentDB


from bottle import route, run, template, request, response, get , post, error

#db=pymysql.connect('cmpe275.ciupcmtzesph.us-west-1.rds.amazonaws.com','root','password','cmpe275')
#cursor=db.cursor()

#data=DBConnectionPool.createPool()


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


@route('/category/<categoryId>/product/<productId>/offer/<offerId>/comment', method='POST')
def createCommentByOfferId(categoryId,productId,offerId):
	postData = request.body.read()
	jsonData = json.loads(postData)
	retData = CommentDB.createCommentByOfferId(categoryId,productId,offerId,jsonData)
	return retData










run(host='localhost', port=3000)