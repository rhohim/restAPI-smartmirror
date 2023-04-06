from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
import os 
from datetime import date

import requests
from bs4 import BeautifulSoup 

from pytrends.request import TrendReq

import instaloader
bot = instaloader.Instaloader()

today = date.today()

app = Flask(__name__)
api = Api(app)

CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Syuting(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    namesyuting = db.Column(db.String(255))
    dateTime = db.Column(db.Text)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    
class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    namekeyword = db.Column(db.String(255))
    dateTime = db.Column(db.Text)
    
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    namevisitor = db.Column(db.String(255))
    dateTime = db.Column(db.Text)
    
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nameAnnoun = db.Column(db.String(255))
    
class TopVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    namevideo = db.Column(db.String(255))
    url = db.Column(db.String(255))
    views = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    subs = db.Column(db.String(255))
    dateTime = db.Column(db.Text)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    
class TopVideo2(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    url = db.Column(db.String(255))
    subs = db.Column(db.String(255))
    
class CameraJS(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    
    
db.create_all()

class syuting(Resource):  
    def post(self):
        today = date.today()
        name = request.form.get('name')
        pic = request.files['image']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if name:
            dataModel = Syuting(namesyuting=name, img=pic.read(), 
                               name = filename , mimetype = mimetype, dateTime = today)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Name is empty"})
    #Read Relation Client    
    def get(self):
        # print(today)
        dataQuery = Syuting.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "name" : data.namesyuting,
                "dateUpdate" : data.dateTime,
                "image" : "http://192.168.1.253:2323/api/syuting/img/" + str(data.id) ,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(Syuting).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})   

class syutingto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = Syuting.query.filter(Syuting.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "client name" : data.namesyuting,
                "dateUpdate" : data.dateTime,
                "image" : "http://192.168.1.253:2323/api/syuting/img/" + str(data.id) ,
            }
        }
        ]
        return make_response(jsonify(output), 200)    
    
class GetImgSyuting(Resource):
    def get(self, data):
        print(data)
        img = Syuting.query.filter(Syuting.id == data).first()
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)


class keyword(Resource):  
    def post(self):
        today = date.today()
        name = request.form.get('name')
        dataModel = Keyword(namekeyword=name, dateTime = today)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    #Read Relation Client    
    def get(self):
        # print(today)
        dataQuery = Keyword.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "name" : data.namekeyword,
                "dateUpdate" : data.dateTime,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(Keyword).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})  

class keywordto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = Keyword.query.filter(Keyword.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "client name" : data.namekeyword,
                "dateUpdate" : data.dateTime,
            }
        }
        ]
        return make_response(jsonify(output), 200)   
    
    
class visitor(Resource):  
    def post(self):
        today = date.today()
        name = request.form.get('name')
        dataModel = Visitor(namevisitor=name, dateTime = today)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    #Read Relation Client    
    def get(self):
        # print(today)
        dataQuery = Visitor.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "name" : data.namevisitor,
                "dateUpdate" : data.dateTime,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(Visitor).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})  

class visitorto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = Visitor.query.filter(Visitor.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.namevisitor,
                "dateUpdate" : data.dateTime,
            }
        }
        ]
        return make_response(jsonify(output), 200)   
    
class announcement(Resource):  
    def post(self):
        name = request.form.get('name')
        dataModel = Announcement(nameAnnoun=name)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    #Read Relation Client    
    def get(self):
        # print(today)
        dataQuery = Announcement.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "name" : data.nameAnnoun
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(Announcement).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})  

class announcementto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = Announcement.query.filter(Announcement.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.nameAnnoun
            }
        }
        ]
        return make_response(jsonify(output), 200)   
    
    
class topvideo(Resource):  
    def post(self):
        url = request.form.get('url')
        subs = request.form.get('subs')
        if url:
            dataModel = TopVideo2(url = url,subs = subs)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Name is empty"})
    #Read Relation Client    
    def get(self):
        # print(today)
        dataQuery = TopVideo2.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "url" : data.url,
                "subs" : data.subs
                
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(TopVideo2).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})   

class topvideoto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = TopVideo.query.filter(TopVideo2.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "url" : data.url,
                "subs" : data.subs
            }
        }
        ]
        return make_response(jsonify(output), 200)    
    
class GetImgTopVideo(Resource):
    def get(self, data):
        print(data)
        img = TopVideo.query.filter(TopVideo.id == data).first()
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)

class article(Resource):
    def get(self):
        today = date.today()
        
        url_arr = ['https://cretivox.com/home/author/fadhillah-nurlita/','https://cretivox.com/home/author/anastasiajessica/', 'https://cretivox.com/home/author/widiyulianto/', 'https://cretivox.com/home/author/adindavirta/']
        articl = 0
        for url in url_arr:
            print(url)
            response = requests.get(url) 
            soup = BeautifulSoup(response.text, 'lxml')

            page = soup.find_all('a',{'class':'page-numbers'})
            page = page[len(page)-2]
            # print(page.get_text())

            title = soup.find_all('h2')
            del title[0]
            del title[len(title)-1]

            url1 = url
            for x in range(2,int(page.get_text())+1):
                url_next = str(url1) + "page/" + str(x) + '/'
                # print(url_next)
                response = requests.get(url_next) 
                soup = BeautifulSoup(response.text, 'lxml')
                title_next = soup.find_all('h2')
                #print(title_next)
                del title_next[0]
                del title_next[len(title_next)-1]
                

                for i in range(len(title_next)):
                    title.append(title_next[i])
                
            articl = articl + int(len(title))
            
        print(articl)
        output = [{
            "data" : {
                "total" : articl,
                "dateUpdate" : today,
            }
        }
        ]
        return make_response(jsonify(output), 200) 

class trends(Resource):
    def get(self):
        dateTime = date.today()
        pytrends = TrendReq(hl='en-US', tz=360)
        trend = []
        search1 = pytrends.trending_searches(pn='indonesia')
        value_trendID = search1[0].values
        for x in range(6):
            trend.append(value_trendID[x])
            print(value_trendID[x])
        output = [{
            "data" : {
                "trend1" : value_trendID[0],
                "trend2" : value_trendID[1],
                "trend3" : value_trendID[2],
                "trend4" : value_trendID[3],
                "trend5" : value_trendID[4],
                "trend6" : value_trendID[5],
                "dataUpdate" : dateTime
            }
        }
        ]
        return make_response(jsonify(output), 200) 

class insta(Resource):
    def get(self):
        datax = []
        d2 = today.strftime("%B %d, %Y")
        profileid = ["cretivox", "condfe" , "overon.gaming"]
        for x in profileid:
            profile = instaloader.Profile.from_username(bot.context, x)
            # print("Username: ", profile.username)
            # print("User ID: ", profile.userid)
            # print("Number of Posts: ", profile.mediacount)
            # print("Followers Count: ", profile.followers)
            # print("Following Count: ", profile.followees)
            # print("Bio: ", profile.biography)
            # print("External URL: ", profile.external_url)   
            # print('\n')
            num_followers = profile.followers
            total_num_likes = 0
            total_num_comments = 0
            total_num_posts = 0
            valueA = []
            truncA = 0
            i = 0
            for post in profile.get_posts():
                total_num_likes += post.likes
                total_num_comments += post.comments
                total_num_posts += 1
                # post = {
                #     "url_post": post.url,
                #     "like": post.likes,
                #     "comment": post.comments
                # }
                # datapost.append(post)
                engagement = float(total_num_likes + total_num_comments) / (num_followers * total_num_posts)
                valueA.append(engagement * 100)
                
                if i == 11:
                    ER_account = float(total_num_likes / 12) + float(total_num_comments / 12)
                    truncA = (ER_account / profile.followers)*100
                    break
                i += 1
            print("%.1f" % truncA)
            print(profile.username)
            print(profile.followers)
            print("%.1f" % float(total_num_likes/total_num_posts))
            print('\n')
            datax.extend([profile.username, profile.followers, "%.1f" % float(total_num_likes/total_num_posts), "%.1f" % truncA ])
        print(len(datax))    
        output = [{
            "id" : 0,
            "data" : {
                "Username" : datax[0],
                "Followers_Count" :  datax[1],
                "Evg_like" :  datax[2],
                "ER" :  datax[3]      
                }
            },
            {
                "id" : 1,
                "data" : {
                    "Username" : datax[4],
                    "Followers_Count" :  datax[5],
                    "Evg_like" :  datax[6],
                    "ER" :  datax[7]      
                }
            },{    
            
            "id" : 2,
            "data" : {
                "Username" : datax[8],
                "Followers_Count" :  datax[9],
                "Evg_like" :  datax[10],
                "ER" :  datax[11]      
                }
            } 
        ]
        print(output)
        
        return make_response(jsonify(output), 200)


class camerajs(Resource):
    def post(self):
        pic = request.files['image']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if pic:
            dataModel = CameraJS(img=pic.read(), name = filename , mimetype = mimetype)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Name is empty"})
    
    def get(self):
        # print(today)
        dataQuery = CameraJS.query.all()
        # print(dataQuery[0].consumable)
        output = [{
            "id" : data.id,
            "data" : {
                "image" : "http://192.168.1.253:2323/api/camera/img/" + str(data.id) ,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(CameraJS).delete()
        db.session.commit()
        
        return jsonify({"msg" : "Deleted"})
    
class GetImgcamera(Resource):
    def get(self, data):
        print(data)
        img = CameraJS.query.filter(CameraJS.id == data).first()
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)  
                    
api.add_resource(camerajs, "/api/camera", methods=["POST", "GET", "DELETE"])
api.add_resource(GetImgcamera,"/api/camera/img/<data>", methods=["GET"])

api.add_resource(syuting, "/api/syuting", methods=["POST","GET","DELETE"])
api.add_resource(GetImgSyuting,"/api/syuting/img/<data>", methods=["GET"]) 
api.add_resource(syutingto2,"/api/syuting/<id>", methods=["GET"])

api.add_resource(topvideo, "/api/top-video", methods=["POST","GET","DELETE"])
api.add_resource(topvideoto2,"/api/top-video/<id>", methods=["GET"]) 
api.add_resource(GetImgTopVideo,"/api/top-video/img/<data>", methods=["GET"])

api.add_resource(keyword, "/api/keyword", methods=["POST","GET","DELETE"])
api.add_resource(keywordto2,"/api/keyword/<id>", methods=["GET"])

api.add_resource(visitor, "/api/visitor", methods=["POST","GET","DELETE"])
api.add_resource(visitorto2,"/api/visitor/<id>", methods=["GET"])

api.add_resource(announcement, "/api/announcement", methods=["POST","GET","DELETE"])
api.add_resource(announcementto2,"/api/announcement/<id>", methods=["GET"])

api.add_resource(article,"/api/article", methods=["GET"])
api.add_resource(trends,"/api/trending", methods=["GET"])
api.add_resource(insta,"/api/instagram", methods=["GET"])


if __name__ == "__main__":
    app.run(debug=True,port=2323, host="0.0.0.0")