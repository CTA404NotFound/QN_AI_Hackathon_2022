from flask import Flask, request, jsonify
import settings 
from solver import solve as sv
import time
import torch

# review_solver = ClassifyReviewSolver(config)

app = Flask(__name__)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/review-solver/solve")
def solve():
    start_time = time.time()
    RATING_ASPECTS = ["giai_tri", "luu_tru", "nha_hang", "an_uong", "di_chuyen", "mua_sam"]

    review_sentence = request.args.get('review_sentence')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    predict_results = sv(review_sentence, device)

    output = {
        "review": review_sentence,
        "results": {}
      }
      
    for count, r in enumerate(RATING_ASPECTS):
        output["results"][r] = predict_results[count]

    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify(output)

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)