
from datetime import datetime
from outscraper import ApiClient

#'https://www.google.com/maps/place/PwC/@25.2007427,55.2726391,17z/data=!4m9!1m2!2m1!1spwc!3m5!1s0x3e5f428139416ec1:0x1068135ebb8e92a7!8m2!3d25.201603!4d55.2726522!15sCgNwd2MiA4gBAZIBHmJ1c2luZXNzX21hbmFnZW1lbnRfY29uc3VsdGFudA'
api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMDgxMjg1MjUyMTM2MzgxNTIyMTB8NGRlMmRlOTU3Ng')
response = api_client.google_maps_business_reviews(
    'https://www.google.com/maps/place/Atlantis,+The+Palm/@25.1303886,55.1170255,16.56z/data=!4m9!3m8!1s0x3e5f153e3609c979:0x5945a418a804ac5!5m3!1s2021-07-17!4m1!1i2!8m2!3d25.1304426!4d55.1171498',
    language='en',
    limit=10,
    reviewsLimit = 50
)

print(response)

#esponse[0]
#rating
#reviews
#reviews_per_score

now = datetime.now()
current_time = now.strftime("%H_%M_%S")

f = open("/Users/maytham/Desktop/sentiment_analysis/reviews.txt", "w")
for review in response[0]['reviews_data']:
    print(review['review_text'])
    if review['review_text'] != None:
        f.write(review['review_text'])
    f.write('\n')

f.close()
