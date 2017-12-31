# Latent Semantic Indexing

import os
from natto import MeCab
import gensim
from gensim import corpora, models, similarities
import collections
from sklearn.feature_extraction import DictVectorizer

mcb = MeCab("-Owakati")
v = DictVectorizer()
mylist = []
mini1 = []
mini2 = []

for i in range(20):
    exec("tango" + str(i) + "= []")

# サブディレクトリに格納した全データテキストファイルを順に読み込み分かち書き
data_list = os.listdir("./data")
print(os.getcwd())
cnt = 0
for name in data_list:
    filename = "./data/" + name
    f = open(filename)
    #print(filename)
    news = f.read()
    wakati = mcb.parse(news).split(" ")
    mydict = collections.Counter(wakati)
    print(mydict)
    f.close()
    # 出現頻度が高すぎる単語、低すぎる単語を除去
    for key in list(mydict):
        if 3 <= mydict[key] and mydict[key] <= 20:
            #print("tango" + str(cnt) + ".append(\"" + str(key) + "\")")
            exec("tango" + str(cnt) + ".append(\"" + str(key) + "\")")
    print(cnt)
    cnt += 1

for j in range(20):
    exec("print(tango" + str(j) + ")")




f = open('it_news1.txt')
news2 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

wakati2 = mcb.parse(news2).split(" ")
mydict2 = collections.Counter(wakati2)

# 出現頻度が高すぎる単語、低すぎる単語を除去
for key in list(mydict2):
    if mydict2[key] <= 3:
        mydict2.pop(key)
    elif mydict2[key] >= 25:
        mydict2.pop(key)
    else:
        mini2.append(key)

mylist.append(mini1)
mylist.append(mini2)
#print(mylist)


# 行列化
#arr = v.fit_transform(mylist).toarray()
#print(arr)
#print(v.get_feature_names())

dictionary = corpora.Dictionary(mylist)
dictionary.save_as_text('deerwester.dict')

#print(dictionary.token2id)

# コーパス生成・外部保存
corpus = [dictionary.doc2bow(text) for text in mylist]
corpora.MmCorpus.serialize('deerwester.mm', corpus)
#print(corpus)

# コーパス読み込み
mm = gensim.corpora.MmCorpus('deerwester.mm')
#print(mm)

lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=dictionary, num_topics=2)

for i in range(5):
    print(lsi.print_topics(i))

