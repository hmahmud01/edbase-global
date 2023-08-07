UserSubscription
	-user
	-subscriptionStatus 	booleanfield
	-subscriptionreference	subscriptioncode connection

SubscriptionType
	-title
	-cost

SubscriptionCodes	
	-code
	-ref  - 			SusbscriptionType connection
	-timePeriod

Course
	-title
	-detail
	-subscriptionrequired  	booleanfield
	-timedate

Lesson
	-title
	-detail
	-video
	-course 			Course Connection