import pymysql
import json
import DBConnectionPool
from bottle import error,response

def cust_error(statuscode,message):
    error = dict()
    error['status'] = statuscode
    error['message'] = message
    errorResponse = json.dumps(error, indent = 4)
    response.status =statuscode
    response.headers['Content-Type'] = 'application/json'
    return errorResponse

def getByUserId(userId):
    try:
        cursor=DBConnectionPool.dbconnect()
        cursor.execute('SELECT * from User where userId=%s',userId)
        row = cursor.fetchone()
        if row is not None:
            jdict = dict()
            jdict['userId'] = row[0]
            jdict['firstName'] = row[1]
            jdict['lastName'] = row[2]
            jdict['emailId'] = row[3]
            jdict['mobile'] = row[4]
            cursor.close()
            return json.dumps(jdict,indent =4 )
        else:
            cursor.close()
            errorResponse = cust_error(404,"User not found. PLease check your userid")
            return errorResponse
    except:
        errorResponse = cust_error(500,"User could not be found due to some exception")
        return errorResponse

def createUser(jsonData):
    try :
        firstName=jsonData['firstName']
        lastName=jsonData['lastName']
        emailId=jsonData['emailId']
        mobile=jsonData['mobile']
        cursor=DBConnectionPool.dbconnect()
        insertUser = """INSERT INTO User (firstName, lastName, emailId, mobile) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insertUser, (firstName,lastName,emailId,mobile))
        cursor.connection.commit()
        user_id = cursor.connection.insert_id()
        cursor.execute('SELECT * from User where userId=%s',user_id)
        row = cursor.fetchone()
        if row is not None:
            jdict = dict()
            jdict['userId'] = row[0]
            jdict['firstName'] = row[1]
            jdict['lastName'] = row[2]
            jdict['emailId'] = row[3]
            jdict['mobile'] = row[4]
            cursor.close()
            return json.dumps(jdict,indent = 4)
        else:
            cursor.close()
            errorResponse = cust_error(404,"User not created successfully")
            return errorResponse
    except:
        errorResponse = cust_error(500,"User not created successfully due to some exception")
        cursor.close()
        return errorResponse