import sqlalchemy.pool as pool
import json
import pymysql 


def dbconnect():
	connection = pool.manage(pymysql)
	db = connection.connect("cmpe275.ciupcmtzesph.us-west-1.rds.amazonaws.com","root","password","cmpe275")
	return db.cursor()