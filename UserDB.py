import pymysql
import json
import DBConnectionPool

#db = pymysql.connect("cmpe275.ciupcmtzesph.us-west-1.rds.amazonaws.com","root","password","cmpe275")
#cursor = db.cursor()

def getByUserId(userId):
 cursor=DBConnectionPool.dbconnect()   
 cursor.execute('SELECT * from User where userId=%s',userId)
 row = cursor.fetchone()
 if row:
 	d=json.dumps(row)
    	jdict = dict()
    	jdict['userId'] = row[0]
    	jdict['firstName'] = row[1]
    	jdict['lastName'] = row[2]
    	jdict['emailId'] = row[3]
    	jdict['mobile'] = row[4]
 return json.dumps(jdict,indent =4 )
 cur.close()

def createUser(jsonData):
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
    if row:
        jdict = dict()
        jdict['userId'] = row[0]
        jdict['firstName'] = row[1]
        jdict['lastName'] = row[2]
        jdict['emailId'] = row[3]
        jdict['mobile'] = row[4]
    return json.dumps(jdict,indent = 4)
    cursor.close()