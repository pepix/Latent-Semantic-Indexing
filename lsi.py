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
stopword = ["する", "です", "、", "。", "ます", "が", "を", "あり", "ない", "いる", "も", "さ", "ある", "こと", "れ", "で", "だ", "し", "で", "と", "て", "は", "た", "（", "）", "な", "い", "や", "だっ", "よう", "れる", "から", "など", "ため", "なる", "なっ", "という", "でき", "的", "この", "その", "だけ", "それ", "しかし", "へ", "しよ", "として", "「", "」", "これ", "まで"]

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
    #print(mydict)
    f.close()
    # 出現頻度が高すぎる単語、低すぎる単語を除去
    for key in list(mydict):
        if 1 <= mydict[key] and mydict[key] <= 10:
            # ストップワードリストに含まれている単語を除去
            if not key in stopword:
                for k in range(mydict[key]):
                    exec("tango" + str(cnt) + ".append(\"" + str(key) + "\")")
    cnt += 1

for j in range(20):
    exec("mylist.append(tango" + str(j) + ")")
    #exec("print(tango" + str(j) + ")")

#print(mylist)

# 行列化
# arr = v.fit_transform(mylist).toarray()
# print(arr)
# print(v.get_feature_names())

dictionary = corpora.Dictionary(mylist)
dictionary.save_as_text('output.dict')

#print(dictionary.token2id)

# コーパス生成・外部保存
corpus = [dictionary.doc2bow(text) for text in mylist]
corpora.MmCorpus.serialize('output.mm', corpus)
#print(corpus)

# コーパス読み込み
mm = gensim.corpora.MmCorpus('output.mm')
#print(mm)

lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=dictionary, num_topics=2)

for i in lsi.print_topics(2):
    print(i)
