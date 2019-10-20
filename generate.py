from json import load
from re import sub
from string import punctuation

from logzero import logger
from keract import get_activations
from keras.models import load_model, Model
from keras.layers import Lambda
import numpy as np
from numpy.random import multinomial

model = load_model("model.h5")

def to_tokens(text, mapping):
    '''
    Takes a list of words and outputs a list of the coresponding tokens
    :param text: list, the words to be tokenzied
    :param mapping: the dictionary to do the lookup with
    :returns: list, the tokens
    '''
    output = []
    for word in text:
        word = word.lower()
        try:
            mapping[word]
        except KeyError:
            logger.warning(f'Unknown word "{word}"')
            mapping[word] = 1
        output.append(mapping[word])
    return output

def to_word(token, mapping):
    '''
    Takes a token and outputs the coresponding word
    :param token: int, the token to be converted to a word
    :param mapping: the dictionary to do the lookup with
    :returns: str, the word
    '''
    try:
        return mapping[str(token)]
    except KeyError:
        return "~"

word_to_token = load(open("word_to_token.json", 'r'))
token_to_word = load(open("token_to_word.json", 'r'))

target_length = model.layers[0].output_shape[-1]

while True:
    phrase = input("    ")
    input_phrase = phrase
    #removes punctuation from the copy of the inputted phrase that will be inputted to the model
    for punc in punctuation:
        input_phrase = input_phrase.replace(punc, "")
    input_phrase = input_phrase.split(" ")
    while len(input_phrase) > 20:
        logger.info(f"Maximum sentence length exceeded removing {input_phrase.pop(0)}")
    tokenized_input_phrase = to_tokens(input_phrase, word_to_token)
    padded_input_phrase = tokenized_input_phrase
    while len(padded_input_phrase) < target_length:
        padded_input_phrase.append(0)
    print(padded_input_phrase)
    predictions = model.predict(np.array([padded_input_phrase]))[0].astype("float64")
    #argsort gives the index of every value in acending order of the values
    #[::-1] reverses the array to give decending order
    #[:8] gets the top eight predicitons
    predictions = np.argsort(predictions)[::-1][:8]
    #print the inputed phrase followed by the predicited words in decending order of confidence
    print(f"{phrase} ({'/'.join([to_word(prediction, token_to_word) for prediction in predictions])})")
