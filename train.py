from json import dump
from math import ceil
from random import randint
import string

from keras.layers import Input, Dense, Embedding
#uncoment if using CPU
##from keras.layers import LSTM
#comment out the line bellow if using CPU
from keras.layers import CuDNNLSTM as LSTM
from keras.models import Model, load_model
from keras.metrics import categorical_accuracy
from keras.utils import to_categorical, plot_model
import numpy as np

def DataGenerator(x_data, y_data, batch_size, lookback_length):
    '''
    A generator that yields batches of training x and y data
    :param x_data: list, the input data that batches should be drawn from
    :param y_data: list, the output data that batches should be drawn from
    :param batch_size: int, the number of datapoints that should be yielded in each batch
    :param lookback_length: int, the length that the model expects every datapoint to be
    :returns: numpy array, an x batch
    :returns: numpy array, a y batch
    '''
    indexes = np.arange(len(x_data))
    while True:
        batch_indexes = np.random.choice(indexes, batch_size)

        X = []
        Y = []
        i = 0
        for i in batch_indexes:
            curr_X = x_data[i]
            if len(curr_X) >= 1:
                #cuts off a random number of words from the start of the datapoint as a form of dropout
                curr_X = curr_X[randint(0, len(curr_X) - 1):]
            #padds with 0s until the datapoint is lookback_length long
            while len(curr_X) < lookback_length:
                curr_X.append(0)
            X.append(curr_X)
            Y.append(y_data[i])

        X = np.array(X)
        Y = np.array(Y)
        yield X, Y
        
#this is what will be removed from words
punctuation = list(string.punctuation)+[" "]+[""]

lines = []
with open("data.txt", "r", encoding="ascii", errors="ignore") as f:
    for line in f.read().splitlines():
        curr_line = ""
        #we aren't intrested in blank lines
        if line != "":
            for word in line.split(" "):
                #theres a problem in the bash download pipeline that means the filenames get scattered through the data file
                if ".en" not in word:
                    for char in word:
                        #removes puntuation characters
                        if char not in string.punctuation:
                            curr_line += char
                    curr_line += " "
        lines.append(curr_line.lower())

#generates a list of words which appear frequently enough to be tokenized
valid_words = []
word_counts = {}
for line in lines:
    for word in line.split(" "):
        if word not in valid_words and word not in punctuation:
            try:
                word_counts[word] += 1
                #the threshold is currently set at 45 occurences over the entire file but this is by no means defiantely the best value
                if word_counts[word] > 45:
                    valid_words.append(word)
                    del word_counts[word]
            except KeyError:
                word_counts[word] = 1

#how many words the model will take as input
#I felt an input of 20 words struck a good balance but feel free to change
max_len = 20

X = []
Y = []

word_to_token = {}

#generates the dictionary for word token lookups
i = 2
for word in valid_words:
    word_to_token[word] = i
    i += 1
word_count = max(word_to_token.values())
print(word_count)

def to_token(word):
    '''
    Takes a word and outputs the coresponding token
    :param word: string, the word to be tokenzied
    :returns: int, the token
    '''
    word = word.lower()
    if word in word_to_token:
        return word_to_token[word]
    return 1

#generates the x and y data by tokenizing segments of each line
#the best analogy for what this does is it slides a window of size max_len words along each line with a stride of 1
#and then adds the tokenized contents of the winodw to the X list
#and then adds the tokenized word after the end of the window to the Y list
for line in lines:
    line = line.split(" ")
    try:
        i = 1
        j = -1*(max_len - 1)
        while True:
            y_tokenized = [to_token(line[i])]
            if y_tokenized != [1] and y_tokenized != [None]:
                tokenized = list(map(to_token, line[j:i]))
                X.append(tokenized)
                Y.append(y_tokenized)
            i += 1
            j += 1
    except IndexError:
        pass

#makes the Y data one-hot encoded
Y = to_categorical(np.array(Y))

#creates an inverse dictionary for going from token to word
token_to_word = {}
for key, value in zip(word_to_token.keys(), word_to_token.values()):
    token_to_word[value] = key

#saves each token dictionary to a json file
dump(word_to_token, open("word_to_token.json", 'w'))
dump(token_to_word, open("token_to_word.json", 'w'))

#trys to resume training if a model file already exists
try:
    open("model.h5").close()
    model = load_model("model.h5")
except FileNotFoundError:
    print("Creating new models")
    inp = Input((max_len,))
    #embedding size is 2 times the cube root of the word count
    embedding = Embedding(word_count, 2*ceil(word_count**(1/3)))(inp)
    lstm = LSTM(512, return_sequences=True)(embedding)
    lstm = LSTM(256)(lstm)
    dense_out = Dense(Y.shape[-1], activation="softmax")(lstm)
    model = Model(inp, dense_out)
    #mse is used beacuse we want to capture the probability distribution
    model.compile("adam", "mse", metrics=[categorical_accuracy])
    plot_model(model, "model.png", show_shapes=True, expand_nested=True)

batch_size = 256
epoch = 0
num_samples = len(X)
DataGen = DataGenerator(X, Y, batch_size, 20)
target_epoch = 0
#I found training stagnated at around epoch 200
while target_epoch < 250:
    x, y = next(DataGen)
    loss, acc = model.train_on_batch(x, y)
    #if we have gone past the epoch which we are lookign for
    if (epoch*batch_size)//num_samples > target_epoch:
        #gives a rough esitmate of the number of passes over the dataset
        print("Epoch", (epoch*batch_size)//num_samples)
        print(f"Accuracy: {acc} Loss: {loss}")
        model.save("model.h5")
        target_epoch += 10
    epoch += 1
