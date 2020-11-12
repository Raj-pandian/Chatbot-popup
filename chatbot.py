'''
Requirement:
Numpy      == 1.16.1
Tensorflow == 1.2.0
tflearn    == 0.3.2
Nltk       == 3.5

'''
import json
import numpy
import tensorflow
import random
import nltk
import tflearn
import pickle

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

try:
    # when you add a new data in json file then simply put x in here it will run the except part
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    # Removing duplicate words

    labels = sorted(labels)

    # Nural networks only understand numbers., we have string in intent file.
    # bags of words it reperesnet any given patten. bages of words is one hard encoding

    training = []
    output = []

    output_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = output_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# If you want to retrain the bot just delete
# model.*  and data.pickel files then comment the try and model.load
try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=3000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_word(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat(message):
    inp = message
    results = model.predict([bag_of_word(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.7:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        return random.choice(responses)
    else:
        message = "I didn't get that, try again."
        return message
