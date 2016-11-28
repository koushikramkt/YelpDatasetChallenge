import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from numpy import mean
from sklearn import metrics
import sys
import time

def loadData(filename, startLine, endLine, classificationLabel):
    data, labels = [], []
    i = 0

    for line in open(filename, 'r'):
        if i > endLine:
            break
        elif i >= startLine:
            obj = json.loads(line)
            data.append(obj['text'])
            if classificationLabel == 'stars':
                rating = (obj['stars'])
                if rating >= 3: labels.append('positive review')
                else: labels.append('negative review')
            elif classificationLabel == 'funny':
                votes = (obj['votes'])
                if votes['funny'] >= 2: labels.append('funny vibe')
                else: labels.append('not funny vibe')
            elif classificationLabel == 'cool':
                votes = (obj['votes'])
                if votes['cool'] >= 5: labels.append('a cool place to hangout')
                else: labels.append('not a cool place')
            elif classificationLabel == 'useful':
                votes = (obj['votes'])
                if votes['useful'] >= 5: labels.append('people found this review useful')
                else: labels.append('not a useful review')
        i += 1
    return data, labels

def numLines(filename):
    return sum(1 for line in open(filename))

if __name__ == '__main__':    
    #classify(technique, posneg, percentData)
    filename = 'yelp_academic_dataset_review.json'
    testfilename = 'test.txt'
    classificationLabel = 'stars'
    num_lines = numLines(filename)
    print "file size %d" % num_lines
    linesToRead = int(num_lines*(float(100)/100.0))
    train_end = linesToRead*0.7

    train_data, train_labels = loadData(filename, 0, train_end, classificationLabel)
    #print train_data
    
    test_data, test_labels = loadData(filename, train_end+1, linesToRead, classificationLabel)
    #test_data, test_labels = loadData(testfilename, 0, 4)
	
    clf_obj = LogisticRegression()
	
    start_time = time.time()
    text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                        ('tfidf', TfidfTransformer()),
                        ('clf', clf_obj),
    ])

    text_clf = text_clf.fit(train_data, train_labels)

    #print text_clf.decision_function(test_data)
    #print "sfgdg" 
    predicted = text_clf.predict(test_data)
    
    print "time: %s seconds" % (time.time() - start_time)

    print "accuracy:", mean(predicted == test_labels)
	
    print predicted
    print(metrics.classification_report(test_labels, predicted))


