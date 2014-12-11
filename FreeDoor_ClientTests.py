import requests,json
from datetime import datetime
categoryId=""
productId=""
userId=""
offerId=""

#CREATE USER
url = "http://localhost:8090/users"
data = {'firstName': 'Alice1', 'lastName': 'Bob1', 'emailId': 'balice@abc.com', 'mobile':'408902341'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.post(url, data=json.dumps(data), headers=headers)
print "----CREATEUSER------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	userId = int(jsonData['userId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------
#GET USER
url = "http://localhost:8090/users/" + str(userId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GETUSERBYID------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#GET Categories
url = "http://localhost:8090/category"
resp = requests.get(url)#.json
#print resp.status_code
print "----GETCATEGORIES------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#CREATE NEW CATEGORY
url = "http://localhost:8090/category"
data = {'categoryName': 'Mobile'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.post(url, data=json.dumps(data), headers=headers)
print "----CREATE NEW CATEGORY------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	categoryId = int(jsonData['categoryId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------
#GET Category Details
url = "http://localhost:8090/category/" + str(categoryId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GET CATEGORY DETAILS------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#GET list of Categories
url = "http://localhost:8090/category/" + str(categoryId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GET CATEGORY DETAILS------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#CREATE NEW Product
now=datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
url = "http://localhost:8090/category/" + str(categoryId) + "/product"
data = {'productName': 'Apple iphone6','quantity': '6','userId': str(userId),'expectedOffer': '5%cashback','productDesc': 'Apples New iphone','productExpiryDate':'2015-01-01','isValid':'1','categoryId':str(categoryId),'lastUpdated':str(time)}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.post(url, data=json.dumps(data), headers=headers)
print "----CREATE NEW PRODUCT------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	productId = int(jsonData['productId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------
#GET Products By Category
url = "http://localhost:8090/category/" + str(categoryId) + "/product"
resp = requests.get(url)#.json
#print resp.status_code
print "----GET PRODUCTS DETAILS BY CATEGORY------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#GET Products By ProductId
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GET PRODUCT DETAILS BY PRODUCTID------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#Update Product
now=datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId)
data = {'productId': str(productId),'productName': 'Apple iphone4S','quantity':'2','userId':userId,'expectedOffer':'5%cashback','productDesc':'Apples Old iphone','productExpiryDate':'2015-01-01','isValid':'1','categoryId':categoryId,'lastUpdated':str(time)}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.put(url, data=json.dumps(data), headers=headers)
print "----UPDATE PRODUCT------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	productId = int(jsonData['productId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------

#CREATE NEW Offer
now=datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer"
data = {'buyingQty': '6','offeredDetails':'10% Cash Back','buyerStatus':'Pending','sellerStatus':'Pending','offerExpiry':'2015-1-1','productId':str(productId),'buyerId':str(userId),'comments':'Hurry up'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.post(url, data=json.dumps(data), headers=headers)
print "----CREATE NEW Offer------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	offerId = int(jsonData['offerId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------
#GET Offer
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GET Offers------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#GET Offer based on offerId
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId)
resp = requests.get(url)#.json
#print resp.status_code
print "----GET Offers------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#Update Offer
now=datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId)
data = {'buyingQty': '6','offeredDetails':'20% Cash Back','buyerStatus':'Pending','sellerStatus':'Pending','offerExpiry':'2015-1-1','productId':str(productId),'buyerId':'1','comments':'Hurry up'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.put(url, data=json.dumps(data), headers=headers)
print "----Update Offer------"
if resp.status_code == 200:
	jsonData = json.loads(resp.content)
	offerId = int(jsonData['offerId'])
	print "PASS"
else:
	print "FAIL"
print "---------------------"

#POST NEW COMMENT
now=datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId) + "/comment"
data = {'comment':'New Comment','userId':str(userId)}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
resp = requests.post(url, data=json.dumps(data), headers=headers)
print "----CREATE NEW Comment------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
print "---------------------"
#---------------------------------------------------------------
#GET Comments History
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId) + "/history"
resp = requests.get(url)#.json
#print resp.status_code
print "----GET Comments History------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#---------------------------------------------------------------
#DELETE offer By offerid
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId) +"/offer/" + str(offerId)
resp = requests.delete(url)#.json
#print resp.status_code
print "----DELETE Offer------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------
#DELETE Products By ProductId
url = "http://localhost:8090/category/" + str(categoryId) + "/product/" + str(productId)
resp = requests.delete(url)#.json
#print resp.status_code
print "----DELETE PRODUCT BY PRODUCTID------"
if resp.status_code == 200:
	print "PASS"
else:
	print "FAIL"
	print "---------------------"
#---------------------------------------------------------------