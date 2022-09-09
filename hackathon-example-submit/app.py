from flask import Flask, request, jsonify, render_template
import settings 
from solver import solve as sv
import pandas as pd

app = Flask(__name__)

@app.get("/")
def root():
    return render_template('index.html')


# @app.get("/review-solver/solve")
# def solve():
#     # start_time = time.time()
#     RATING_ASPECTS = ["giai_tri", "luu_tru", "nha_hang", "an_uong", "di_chuyen", "mua_sam"]

#     review_sentence = request.args.get('review_sentence')
#     predict_results = sv(review_sentence)

#     output = {
#         "review": review_sentence,
#         "results": {}
#       }
      
#     for count, r in enumerate(RATING_ASPECTS):
#         output["results"][r] = predict_results[count]

#     # print("--- %s seconds ---" % (time.time() - start_time))
#     return jsonify(output)



@app.post("/")
def getdata():
    RATING_ASPECTS = ["Giải trí", "Lưu trú", "Nhà hàng", "Ăn uống", "Di chuyển", "Mua sắm"]
    if request.method == "POST":
        review_sentence = request.form["review"]
        data = []
        predict_results = sv(review_sentence)
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

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, debug=True)