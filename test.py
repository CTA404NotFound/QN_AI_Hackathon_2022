from eval import *

target = [[5,3,1,0,2,4],

        [5,2,0,0,4,0],

        [2,1,5,4,4,1],

        [0,3,5,2,5,5]]



prediction = [[4,2,0,2,2,5],

            [5,3,3,1,1,1],

            [3,0,5,3,2,1],

            [4,2,1,2,4,2]]


# prediction = [[1, 0, 3, 4, 2, 0], [0, 2, 2, 5, 1, 0]]
# target = [[1, 1, 3, 5, 3, 1], [0, 0, 3, 4, 0, 0]]
# num_examples = len(prediction)
# print(f"Num examples: {num_examples}")
# aspect_idx = 0
# count = 0
# numerator = []
# for i in range(num_examples):
#     numerator.append((prediction[i][aspect_idx] - target[i][aspect_idx])**2)
#     if prediction[i][aspect_idx] != 0 and target[i][aspect_idx] != 0:
#         count += 1

# print(numerator)

precisions, recalls, f1_scores, r2_scores = [], [], [], []

for i in range(6):
    prec, rec, f1, r2 = eval_metrics(i, prediction, target)
    precisions.append(prec)
    recalls.append(rec)
    f1_scores.append(f1)
    r2_scores.append(r2)

print(f"Precisions: {precisions}")
print(f"Recall: {recalls}")
print(f"F1 score: {f1_scores}")
print(f"R2 score: {r2_scores}")


res = sum([a*b for a,b in zip(f1_scores,r2_scores)])
print(1/6 * res)