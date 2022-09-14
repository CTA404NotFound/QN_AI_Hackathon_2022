# # dict_ls = ["review","giai_tri","luu_tru","nha_hang","an_uong","di_chuyen","mua_sam"]
# # rv = "nha hang dep"
# # score = [0,0,4,0,0,0]
# # score.insert(0,rv)
# # print(score)
# # a = dict(zip(dict_ls,rv))
# # a = dict(zip(a,score))

# # print(a)

# txt = "an uong ngon qua"

# ls = [0,0,0,5,0,0]

# ls.insert(0,txt)
# print(s)

from py_mongodb import reviews

review_mg = reviews.find()
for rv in review_mg:
    print(rv)
