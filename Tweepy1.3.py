import tweepy
import json
from selenium import webdriver 
from time import sleep 
from PIL import Image
from gtts.tokenizer import PreProcessorRegex, PreProcessorSub, symbols
from gtts import gTTS
from moviepy.editor import *

#Youtube upload modules
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload


#twitter algorithm
auth = tweepy.OAuthHandler("rIRlNfDSqeKSG3S28y1lftbHB",
                           "FO8ljQPJNZfNucfrIqz4SluY1ZvoidezpZYYR6smsGp19Tiv9X")#API public and secret keys
auth.set_access_token("871671216901427201-8xLxXu1mGnw9hW268mlTHSn0ayvbXD7",
                      "soFJg6EQbCJmJdj014Zbdeo2MxJlhylBTLyF3ejclZZ3m")#Access token and secret
api = tweepy.API(auth)
trendsList = list()
trendsFilter = str()
output = list()
transcript = list()
countConst = 5

language = 'en'#Language that tts reads
localizer ='ie'#co.uk,ca,co.in,ie,ca

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)



trendsDick = api.trends_place(2295414)#Get list of dictionaries of trends of yahoo WOEID code
for trend in trendsDick[0]["trends"]:
    trendsList.append(trend["name"]) #Make list of lookup terms


for i in range(0,4):
    output.append(trendsList[i])#Name of trend added to list before respective trends
    trendsFilter = trendsList[i]+' -filter:retweets'#Filtering out retweets
    for tweet in api.search(q=trendsFilter,lang="en",count = 5,result_type="mixed",tweet_mode = "extended"):#Tweet lookup
            output.append("https://twitter.com/twitter/statuses/"+str(tweet.id))#Create link for screenshots
            transcript.append(tweet.full_text)#Create transcript for tts
            
for i in range(0,len(transcript)): 
    if((transcript[i])[-23:-18] == 'https'):#Find tweet transcripts with link attached at end
        transcript[i] = (transcript[i])[0:-23]#Remove link

#TTS

for i in range(0,len(transcript)):
    #gtts.tokenizer.pre_processors.abbreviations(transcript[i])
    myobj = gTTS(text=transcript[i],
                 lang=language,
                 tld = localizer,
                 slow=False)
                 #Slow = False to force high speed
    myobj.save("data/audio/"+str(i+1)+".mp3")
    
#screenshot algorithm

l1=list()
l2=list()
l3=list()
l4=list()
l5=list()
temp=0


for i in range(0,len(output)):
    if (len(output[i])!=56):
        l5.append(output[i])
        temp+=1
    else:
        if temp==1 :
            l1.append(output[i])
        elif temp==2 :
            l2.append(output[i])
        elif temp==3 :
            l3.append(output[i])
        elif temp==4 :
            l4.append(output[i])


print(l5)
driver = webdriver.Chrome("chromedriver.exe")
for a in range(0,len(l1)):
        driver.get(l1[a])
        sleep(2)
        driver.save_screenshot("data/screenshots/"+str(a+1)+".png")
for b in range(0,len(l2)):
        driver.get(l2[b])
        sleep(2)
        driver.save_screenshot("data/screenshots/"+str(b+6)+".png")
for c in range(0,len(l3)):
        driver.get(l3[c])
        sleep(2)
        driver.save_screenshot("data/screenshots/"+str(c+11)+".png")
for d in range(0,len(l4)):
        driver.get(l4[d])
        sleep(2)
        driver.save_screenshot("data/screenshots/"+str(d+16)+".png")

driver.quit()

#cropping algorithm

width = 910
height = 512

for j in range(1,21):
        im=Image.open("data/screenshots/"+str(j)+".png")
        im=im.crop((0,0,width,height))
        im=im.resize((1280,720), Image.BOX)
        im.save("data/screenshots/"+str(j)+".png")


#clipping algorithm

finalClipList = list()
for i in range(1,21):
    audio = AudioFileClip("data/audio/"+str(i)+".mp3")
    clip = ImageClip("data/screenshots/"+str(i)+".png").set_duration(audio.duration)
    clip = clip.set_audio(audio)
    finalClipList.append(clip)

final_clip = concatenate_videoclips(finalClipList)
    
final_clip.write_videofile("data/finalclip.mp4", fps=6,threads=8,logger = None)


#Youtube upload
request_body = {
    'snippet': {
        'categoryI': 20,
        'title': l5[0]+','+l5[1]+','+l5[2]+','+l5[3],
        'description': 'HI PARTH!!!',
        'tags': ['Creeper', 'Video Game']
    },
    'status': {
        'privacyStatus': 'public',
        #'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False, 
    },
    'notifySubscribers': False
}

mediaFile = MediaFileUpload('data/finalclip.mp4')

response_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()


service.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload(V3.)
).execute()



















                
