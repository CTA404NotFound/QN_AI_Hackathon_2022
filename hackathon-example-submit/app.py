""" Created by Cyouisme """
# 08/20/2022
# -*-encoding:utf-8-*-

from wsgiref.util import request_uri
from flask import Flask, request, jsonify, render_template,redirect
import settings 
from solver import solve as sv
import pandas as pd
from py_mongodb import insert_data, reviews,remove_data, wrong_reviews
# import Guide

app = Flask(__name__)

@app.get("/")
def root():
    return render_template('index.html')

# @app.get("/admin")
# def admin():
#     # data = []
#     review_mg = reviews.find()
#     data = pd.DataFrame(review_mg)
#     return render_template('test.html',data=data.to_html(classes='table table-stripped mycustombtn',index=False,justify="center"))

@app.get("/admin")
def admin():
    # data = []
    review_mg = reviews.find()
    # data = pd.DataFrame(review_mg)
    return render_template('admin.html',review_mg=review_mg)

@app.get("/delete/<id>")
def delete(id):

    path_del = request.path
    id_del = path_del.split("/")[-1]
    remove_data(reviews,id_del)

    # review_mg = reviews.find()
    return redirect("http://127.0.0.1:8000/admin", code=302)

@app.get("/wrongrv")
def wrong_rv():
    wr_rv = wrong_reviews.find()
    return render_template('wrong.html',wr_rv=wr_rv)

@app.post("/")
def getdata():
    RATING_ASPECTS = ["Giải trí", "Lưu trú", "Nhà hàng", "Ăn uống", "Di chuyển", "Mua sắm"]
    if request.method == "POST":


        try:
            dict_ls = ["Review","Giải trí", "Lưu trú", "Nhà hàng", "Ăn uống", "Di chuyển", "Mua sắm"]          
            review_sentence = request.form["review"]
            data = []

            #predict aspect and rating
            predict_results = sv(review_sentence)
            pre_result_copy = predict_results.copy()

            #Insert review to predict list
            pre_result_copy.insert(0,review_sentence)
            review_dict = dict(zip(dict_ls,pre_result_copy))
            #Insert data to mongodb
            insert_data(reviews,review_dict)

            print(predict_results)

            i = 0
            while i < len(predict_results):
                if predict_results[i] != 0 :
                    predict_results[i] = str(predict_results[i]) + "⭐"
                i+=1

            data = dict(zip(RATING_ASPECTS, predict_results))
            data.update()
            data = pd.DataFrame([data])
            review_sentence = '" ' + review_sentence + ' "'
            return render_template("index.html", data=data.to_html(classes='table table-stripped mycustombtn',index=False,justify="center"),review_sentence=review_sentence)
        except:
            review_sent = request.form["review"] 
            insert_data(wrong_reviews,{"Review": review_sent})
            return render_template('index.html',review_sent=review_sent)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, debug=True)