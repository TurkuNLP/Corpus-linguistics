from sklearn import svm
import sklearn.feature_extraction
from sklearn import cross_validation
import sys
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
import numpy as np
import codecs

inp = codecs.getreader(u"utf-8")(sys.stdin)
out8 = codecs.getwriter(u"utf-8")(sys.stdout)

labels_train = [] # training labels
labels_test = [] # testset labels

feats_test = [] # testset features
feats_train = [] #training set feautures

label_feats = [] # combination of label + all feats per document, as read in line by kube

dictionary = {} # these are to split bw train and test
dictionary2 = {}

for f in inp:
    label_feats.append(f)

for s in (label_feats):
    l, f = s.split(" ",1)
    if l not in dictionary:
        dictionary[l]=0
    dictionary[l]+=1

for t in (label_feats):
    x, feat = t.split(u" ",1)
    if x not in dictionary2:
        dictionary2[x]=0
    dictionary2[x]+=1
    if dictionary[x]*0.2 > dictionary2[x]:
        labels_test.append(int(x[0]))
        feats_test.append(feat)
    else:
        labels_train.append(int(x[0]))
        feats_train.append(feat)
                                                         
def data_iterator(f):
    for token in f:
        yield token

def tokenizer(txt):
    return txt.split()

vectorizer=sklearn.feature_extraction.text.CountVectorizer(tokenizer=tokenizer, min_df=0.01)

for count, t in enumerate(label_feats):
    x, feat = t.split(u" ",1)
    if x not in dictionary2:
        dictionary2[x]=0
    dictionary2[x]+=1
    if dictionary[x]*0.2 > dictionary2[x]:
        labels_test.append(int(x[0]))
        feats_test.append(feat)
    else:
        labels_train.append(int(x[0]))
        feats_train.append(feat)

iterator=data_iterator(feats_train)
test_iterator=data_iterator(feats_test)

d = vectorizer.fit_transform(iterator)
d_test=vectorizer.transform(test_iterator)

for c in [0.5]: # here you can test with different c values
    classifier=LinearSVC(penalty="l1", C=c, dual=False, class_weight="auto")
    classifier.fit(d,labels_train)

    labels_test_pred = classifier.predict(d_test)
    target_names = []
    
    print classification_report(labels_test, labels_test_pred)
    print
    f_names=vectorizer.get_feature_names()

    print >> out8,  "CLASS 0: Positiiviset avainlemmat:"
    print
    
    sorted_by_weight=sorted(zip(classifier.coef_[0], f_names))
    for f_weight, f_name in sorted_by_weight[:50]:
            print >> out8, f_name, f_weight
    print
  #  print >> out8, "CLASS 1: Positiiviset avainlemmat:"
 #   print
#    for f_weight, f_name in sorted_by_weight[-10:]:
#            print >> out8, f_name, f_weight
#    print
