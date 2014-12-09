class Constants:

############Request/Response##################
	CONTENT_TYPE='application/json'
	STATUS='status'
	MESSAGE='message'
	CONTENT='Content-Type'
	NOT_FOUND=404
	INTERNAL_SERVER_ERROR=500
	SUCCESS=200
	BAD_DATA=422  ## Unprocessable entity
	REQUIRED_FIELD_MISSING='Required Field missing in payload'
#################################User###############################	
	USERID='userId'
	FIRSTNAME='firstName'
	LASTNAME='lastName'
	EMAILID='emailId'
	MOBILE='mobile'
	USER_EXCEPTION1='User not found. Please check your userid'
	USER_EXCEPTION2='User could not be found due to some exception'
	USER_EXCEPTION3='User not created successfully'
	USER_EXCEPTION4='User not created successfully due to some exception'
	EMAIL_VALIDATION='EmailID is required field'


#################################Comment#############################

	COMMENT='comment'
	COMMENTID='commentId'
	COMMENTDESC='commentDesc'


################################Category##############################
	CATEGORY_NAME='categoryName'
	CATEGORY_NAME_VALIDATION='Category name is required field'	

###############################Product################################
	JSON_INVALID='Product name expected in payload'
	#QUANTITY_VALIDATION='Please specify the quantity'
	#NEGATIVE_VALIDATION='Quanity cannot be less than zero'