#!/usr/bin/python3
from flask import Flask, jsonify
from flask_restful import Resource, Api

from WebScrapping.MyWebScrapping import BandecoWebScrapper
from WebScrapping.DownloadHtmlPage import DowloadHtmlPage

app = Flask(__name__)
api = Api(app)

downHtml = DowloadHtmlPage()

def getData():
    #return BandecoWebScrapper('..\Pages\cardapionaoreg.html').extract_data()
    return BandecoWebScrapper().extract_data()


class  StartApi(Resource):
    def get(self):
        return jsonify({'status':'success'})

class  BandecoApi(Resource):
    def get(self):
        return jsonify(getData())

api.add_resource(StartApi, '/')  # Route_3
api.add_resource(BandecoApi, '/menu')  # Route_3


app.run()