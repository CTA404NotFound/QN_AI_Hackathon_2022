""" Created by Cyouisme """
# 08/20/2022
# -*-encoding:utf-8-*-

from flask import Flask, request, jsonify, render_template
import settings 
from solver import solve as sv
import pandas as pd
from py_mongodb import insert_db, reviews

app = Flask(__name__)

@app.get("/")
def root():
    return render_template('index.html')

@app.get("/admin")
def admin():
    data = []
    review_mg = reviews.find()
    data = pd.DataFrame(review_mg)
    return render_template('test.html',data=data.to_html(classes='table table-stripped mycustombtn',index=False,justify="center"))



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
            insert_db(reviews,review_dict)

            print(predict_results)

            i = 0
            while i < len(predict_results):
                if predict_results[i] != 0 :
                    predict_results[i] = str(predict_results[i]) + "⭐"
                i+=1

            data = dict(zip(RATING_ASPECTS, predict_results))
            data = pd.DataFrame([data])
            review_sentence = '" ' + review_sentence + ' "'
            return render_template("index.html", data=data.to_html(classes='table table-stripped mycustombtn',index=False,justify="center"),review_sentence=review_sentence)
        except:
            review_sent = request.form["review"] 
            return render_template('index.html',review_sent=review_sent)

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, debug=True)