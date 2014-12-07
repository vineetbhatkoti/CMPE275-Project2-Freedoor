import json
import pymysql


def dbconnect():
	db = pymysql.connect("cmpe275.ciupcmtzesph.us-west-1.rds.amazonaws.com","root","password","cmpe275")
	return db.cursor()