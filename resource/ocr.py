from flask_restful import Resource 
from flask import jsonify
from flask_restful import reqparse
from google.oauth2 import service_account
from google.cloud import vision
import io
import json
import binascii
import base64


class ocr (Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('source', required=True, help='source is required')

    def post(self):
        """Detects text in the file."""
        arg = self.parser.parse_args()
        source=arg['source']

        #with open(source,"rb") as img_file:
           #source = base64.b64encode(img_file.read())

        credentials = service_account.Credentials.from_service_account_file('C:/Users/mountain17/group17project/ScanCalendarTest-b6787030ec8c.json')
        client = vision.ImageAnnotatorClient(credentials=credentials)
        content = binascii.a2b_base64(source)

        image = vision.types.Image(content=content)
    
        response = client.text_detection(image=image)
        #print(f'response:{response}')
        
        texts = response.text_annotations
        
        timelist=[]
        eventlist=[]
        
        count=1
        dic={}
        list1=[]
        date = ""
        texts_split = texts[0].description.split('\n')
        
        for t, i in enumerate(texts_split):
            if (i.find(r'/')) != -1:
                date = i
            else:
                if (i.find(':'))!=-1:
                    timelist.append(i)
                    print(timelist)
                else:
                    if i!="":#解決最後一項會是空的狀況
                        eventlist.append(i)
                        print(eventlist)
                        dic.update({'行程': count})
                        count+=1
                        if(date.find('|')) != -1: 
                            date=date.replace("|","1")
                        elif(date.find('l')) != -1:
                            date=date.replace("l","1")
                        elif(date.find('z')) != -1:
                            date=date.replace("z","2")
                        elif(date.find('q')) != -1:
                            date=date.replace("q","9")
                        elif(date.find('b')) != -1:
                            date=date.replace("b","6")
                        elif(date.find('o')) != -1:
                            date=date.replace("o","0")
                        elif(date.find('O')) != -1:
                            date=date.replace("O","0")
                        date = date.replace(" ","")
                        #print(date)
                        dic.update({'startDate':date.split('/')[0]+'-'+ date.split('/')[1]+'-'+date.split('/')[2],'endDate':date.split('/')[0]+'-'+ date.split('/')[1]+'-'+date.split('/')[2]})
                        list1.append(dic)
                        dic={}
        
        try:
            for i in range(len(eventlist)):
                if(timelist[i].find('|')) != -1: 
                    timelist[i]=timelist[i].replace("|","1")
                elif(timelist[i].find('l')) != -1:
                    timelist[i]=timelist[i].replace("l","1")
                elif(timelist[i].find('z')) != -1:
                    timelist[i]=timelist[i].replace("z","2")
                elif(timelist[i].find('q')) != -1:
                    timelist[i]=timelist[i].replace("q","9")
                elif(timelist[i].find('b')) != -1:
                    timelist[i]=timelist[i].replace("b","6")
                elif(timelist[i].find('o')) != -1:
                    timelist[i]=timelist[i].replace("o","0")
                elif(timelist[i].find('O')) != -1:
                    timelist[i]=timelist[i].replace("O","0")
                timelist[i]=timelist[i].replace(" ","")
                #print(timelist[i])
                list1[i].update({'startTime':timelist[i].split('-')[0].replace(" ","")})
                list1[i].update({'endTime':timelist[i].split('-')[1].replace(" ","")})
                list1[i].update({'title':eventlist[i]})
                #print(list1[i])
                #print(len(timelist))
        finally:
            return jsonify(list1)
    