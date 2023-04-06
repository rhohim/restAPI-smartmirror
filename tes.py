# import tweepy

# api_key = "WVeBmQEzSWp1uQLVGekxxWREv"
# api_key_secret = "ulPTAhIk1NlM659tcu14ayaGJAjw8usm9deUr6ghXSnCtZvWwq"
# barear_token = "AAAAAAAAAAAAAAAAAAAAAIJ0hAEAAAAA8YjV%2BNbJrlZhzlrfDxoHrHTjLXo%3DTh6o3yN24e5jyyj0tXKd2Sf6h21IAKH7hSpff1IzshcBM2vn9c"
# client_id = "ZFMwQXQ4WWRUOVFmTEZlZnhLWmI6MTpjaQ"
# client_secret = "IzLz1otek8-YsRC3jaPEI4fprZlrsZdHJF081Mr4MlsB216sJV"
# access_token = "1517003922099294208-rGmIIFxor5fD7206J6Gv8l18a4Jogl"
# access_token_secret = "aC8qWAY6vVukjgnEXmqT4rRZ2FomeZvE6FUfS9dhOVPfF"

# consumer_key = api_key
# consumer_secret = api_key_secret
# access_token = access_token
# access_token_secret = access_token_secret
 
# # authorization of consumer key and consumer secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
 
# # set access to user's access key and access secret
# auth.set_access_token(access_token, access_token_secret)
 
# # calling the api
# api = tweepy.API(auth)
 
# # WOEID of London
# woeid = 1047378
 
# # fetching the trends
# trends = api.get_place_trends(id = woeid)
 
# # printing the information
# print("The top trends for the location are :")
 
# for value in trends:
#     for trend in value['trends']:
#         print(trend['name'])

# import requests
# from bs4 import BeautifulSoup 

# url_arr = ['https://cretivox.com/home/author/fadhillah-nurlita/','https://cretivox.com/home/author/anastasiajessica/', 'https://cretivox.com/home/author/widiyulianto/', 'https://cretivox.com/home/author/adindavirta/']
# articl = 0
# for url in url_arr:
#     print(url)
#     response = requests.get(url) 
#     soup = BeautifulSoup(response.text, 'lxml')

#     page = soup.find_all('a',{'class':'page-numbers'})
#     page = page[len(page)-2]
#     # print(page.get_text())

#     title = soup.find_all('h2')
#     del title[0]
#     del title[len(title)-1]

#     url1 = url
#     for x in range(2,int(page.get_text())+1):
#         url_next = str(url1) + "page/" + str(x) + '/'
#         # print(url_next)
#         response = requests.get(url_next) 
#         soup = BeautifulSoup(response.text, 'lxml')
#         title_next = soup.find_all('h2')
#         #print(title_next)
#         del title_next[0]
#         del title_next[len(title_next)-1]
        

#         for i in range(len(title_next)):
#             title.append(title_next[i])
        
#     articl = articl + int(len(title))
    
# print(articl)
# from pytrends.request import TrendReq

# pytrends = TrendReq(hl='en-US', tz=360)
# trend = []
# # search1 = pytrends.trending_searches(pn='indonesia')
# # value_trendID = search1[0].values
# # for x in range(6):
# #     trend.append(value_trendID[x])
# #     print(value_trendID[x])
# trend.extend([1,2,3])
# print(trend[0])


import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
 
##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
#########################
 
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# while True:
#     success, img = cap.read()
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

detector = htm.handDetector(maxHands=1)
# wScr, hScr = autopy.screen.size()
# # print(wScr, hScr)
 
while True:
#     # 1. Find hand Landmarks
    success, img = cap.read()
    # img = detector.findHands(img)
    # lmList, bbox = detector.findPosition(img)
#     # 2. Get the tip of the index and middle fingers
#     if len(lmList) != 0:
#         x1, y1 = lmList[8][1:]
#         x2, y2 = lmList[12][1:]
#         # print(x1, y1, x2, y2)
    
#     # 3. Check which fingers are up
#     fingers = detector.fingersUp()
#     # print(fingers)
#     cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
#     (255, 0, 255), 2)
#     # 4. Only Index Finger : Moving Mode
#     if fingers[1] == 1 and fingers[2] == 0:
#         # 5. Convert Coordinates
#         x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
#         y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
#         # 6. Smoothen Values
#         clocX = plocX + (x3 - plocX) / smoothening
#         clocY = plocY + (y3 - plocY) / smoothening
    
#         # 7. Move Mouse
#         autopy.mouse.move(wScr - clocX, clocY)
#         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#         plocX, plocY = clocX, clocY
        
#     # 8. Both Index and middle fingers are up : Clicking Mode
#     if fingers[1] == 1 and fingers[2] == 1:
#         # 9. Find distance between fingers
#         length, img, lineInfo = detector.findDistance(8, 12, img)
#         print(length)
#         # 10. Click mouse if distance short
#         if length < 40:
#             cv2.circle(img, (lineInfo[4], lineInfo[5]),
#             15, (0, 255, 0), cv2.FILLED)
#             autopy.mouse.click()
    
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)