import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import tree
from numpy import mean
from sklearn import metrics
import sys
import time

def loadData(filename, startLine, endLine):
    data, labels = [], []
    i = 0

    for line in open(filename, 'r'):
        if i > endLine:
            break
        elif i >= startLine:
            obj = json.loads(line)
            data.append(obj['text'])
            votes = (obj['votes'])
            if votes['funny'] >= 2: labels.append('funny vibe')
            else: labels.append('not funny vibe')
          
        i += 1

    return data, labels
    
def loadcontent(filename,chunksize, linesToRead,testindex):
    testdata,testlabels,traindata,trainlabels = [],[],[],[]
    i = 0
    index = 0
    for line in open(filename, 'r'):
        index = i / chunksize
        if index == testindex:
            obj = json.loads(line)
            testdata.append(obj['text'])
            votes = (obj['votes'])
            if votes['funny'] >= 2: testlabels.append('funny vibe')
            else: testlabels.append('not funny vibe')
        else:
            obj = json.loads(line)
            traindata.append(obj['text'])
            votes = (obj['votes'])
            if votes['funny'] >= 2: trainlabels.append('funny vibe')
            else: trainlabels.append('not funny vibe')
        
        i += 1
        if i > linesToRead:
            break
    return traindata,trainlabels,testdata,testlabels                

def numLines(filename):
    return sum(1 for line in open(filename))

if __name__ == '__main__':    
    #classify(technique, posneg, percentData)
    filename = 'yelp_academic_dataset_review.json'
    testfilename = 'test.txt'
    num_lines = numLines(filename)
    print "file size %d" % num_lines
    linesToRead = int(num_lines*(float(3)/100.0))
    train_end = linesToRead*0.7

    #train_data, train_labels = loadData(filename, 0, train_end)
    #print train_data
    
    #test_data, test_labels = loadData(filename, train_end+1, linesToRead)
    #test_data, test_labels = loadData(testfilename, 0, 4)
    testindex = 0
    k = 10
    chunksize = linesToRead / k
    clf_obj = LogisticRegression()
    #clf_obj = tree.DecisionTreeClassifier()

    
    text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                        ('tfidf', TfidfTransformer()),
                        ('clf', clf_obj),
    ])
    start_time = time.time()
    for j in range(0,k):            
        print "iteration %d" % j 
        train_data, train_labels,test_data, test_labels = loadcontent(filename,chunksize, linesToRead,j)
        #clf_obj = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)
       
    
        text_clf = text_clf.fit(train_data, train_labels)

        #print text_clf.decision_function(test_data)
        #print "sfgdg" 
        predicted = text_clf.predict(test_data)
    
        

        print "accuracy:", mean(predicted == test_labels)
	
        #thefile = open('test.txt', 'w')
        #for item in predicted:
            #thefile.write("%s\n" % item)
        #print len(predicted)
        print(metrics.classification_report(test_labels, predicted))

    print "time: %s seconds" % (time.time() - start_time)
