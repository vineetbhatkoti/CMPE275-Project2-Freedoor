import pymysql
import json
import DBConnectionPool
from bottle import error,response
from Constants import Constants

def cust_error(statuscode,message):
    error = dict()
    error[Constants.STATUS] = statuscode
    error[Constants.MESSAGE] = message
    errorResponse = json.dumps(error, indent = 4)
    response.status =statuscode
    response.headers[Constants.CONTENT] = Constants.CONTENT_TYPE
    return errorResponse

def getByUserId(userId):
    try:
        cursor=DBConnectionPool.dbconnect()
        cursor.execute('SELECT * from User where userId=%s',userId)
        row = cursor.fetchone()
        if row is not None:
            jdict = dict()
            jdict[Constants.USERID] = row[0]
            jdict[Constants.FIRSTNAME] = row[1]
            jdict[Constants.LASTNAME] = row[2]
            jdict[Constants.EMAILID] = row[3]
            jdict[Constants.MOBILE] = row[4]
            cursor.close()
            return json.dumps(jdict,indent =4 )
        else:
            cursor.close()
            errorResponse = cust_error(Constants.NOT_FOUND,Constants.USER_EXCEPTION1)
            return errorResponse
    except:
        errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.USER_EXCEPTION2)
        return errorResponse

def createUser(jsonData):
    try :
        firstName=jsonData[Constants.FIRSTNAME]
        lastName=jsonData[Constants.LASTNAME]
        emailId=jsonData[Constants.EMAILID]
        mobile=jsonData[Constants.MOBILE]
        print mobile
        cursor=DBConnectionPool.dbconnect()
        insertUser = """INSERT INTO User (firstName, lastName, emailId, mobile) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insertUser, (firstName,lastName,emailId,mobile))
        cursor.connection.commit()
        user_id = cursor.connection.insert_id()
        cursor.execute('SELECT * from User where userId=%s',user_id)
        row = cursor.fetchone()
        if row is not None:
            jdict = dict()
            jdict[Constants.USERID] = row[0]
            jdict[Constants.FIRSTNAME] = row[1]
            jdict[Constants.LASTNAME] = row[2]
            jdict[Constants.EMAILID] = row[3]
            jdict[Constants.MOBILE] = row[4]
            cursor.close()
            return json.dumps(jdict,indent = 4)
        else:
            cursor.close()
            errorResponse = cust_error(Constants.NOT_FOUND,Constants.USER_EXCEPTION3)
            return errorResponse
    except:
        errorResponse = cust_error(Constants.INTERNAL_SERVER_ERROR,Constants.USER_EXCEPTION4)
        return errorResponse