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
	COMMENTHISTORY_EXP1='Something went wrong while processing at server side'
	COMMENT_ERROR='Comment could not be created successfully'
	COMMENT_EXCEPTION2='Comment could not be created due to some exception'
	CATEGORY_ERROR1='Catgory not found. Please create a new category.'
	CATEGORY_ERROR2='Category could not be found due to exception'
	CATEGORY_ERROR3='Category not found. Please check your categoryid again.'
	CATEGORY_ERROR4='Category not created properly.'


#################################Comment#############################

	COMMENT='comment'
	COMMENTID='commentId'
	COMMENTDESC='commentDesc'


################################Category##############################
	CATEGORY_NAME='categoryName'
	CATEGORY_NAME_VALIDATION='Category name is required field'	
	CATEGORY_ID='categoryId'
	CATEGORY='category'
###############################Product################################
	JSON_INVALID='Product name expected in payload'
	#QUANTITY_VALIDATION='Please specify the quantity'
	#NEGATIVE_VALIDATION='Quanity cannot be less than zero'
###############################Offer #################################
	OFFERID = 'offerId'
	BUYINGQTY='buyingQty'	
	OFFEREDDETAILS='offeredDetails'
	BUYERSTATUS='buyerStatus'
	SELLERSTATUS='sellerStatus'
	OFFEREXPIRY='offerExpiry'
	BUYERID='buyerId'
	PRODUCTID ='productId'
	LASTMODIFIED = 'lastModified'
	COMMENTS='comments'
	LASTEVENT='lastEvent'
	OFFERS ='offers'
	DELETEOFFER_SUCCESS = 'Successfully deleted the Offer !!'
	DELETEOFFER_FAIL = 'Offer could not be deleted due to some exception'
	OFFER_NOT_FOUND = 'Offer not found. Please check your offerid.'
	OFFER_FAIL_MESSAGE = 'Offer could not be retrieved successfully due to some exception.'
################################OfferHistory##############################

	OFFERHISTORYID='offerHistoryId'
	MODIFIED='modified'
	LASTDATETIME='lastDateTime'
	OFFERID='offerId'
	OFFERHISTORY='OfferHistory'

#################################Category###################################



