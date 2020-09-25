from offline.data import data, list_data_sentences, AutoCompleteData
from utils.ignore_casing import ignore_casing
from utils.encoder import SetEncoder

import os
import json
import pickle


def initialized_data(file_name, completed_sentence, offset):
    initialized_data.id_sentence += 1

    for i in range(len(completed_sentence)):

        for j in range(i + 1, len(completed_sentence) + 1):
            adding_data = ignore_casing(completed_sentence[i: j])

            if len(data[adding_data]) < 5:
                data[adding_data].add(initialized_data.id_sentence)

    new_data = AutoCompleteData(completed_sentence, file_name, offset, 0)
    list_data_sentences.append(new_data)


initialized_data.id_sentence = -1


def preparing_system():
    path = "../System data/python-3.8.4-docs-text/python-3.8.4-docs-text/c-api"

    for root, dirs, files in os.walk(path, topdown=True):
        
        for file in files:
            data_file = open(root + '/' + file, encoding="utf8")
            data_sentences = data_file.read().split("\n")
            offset = 1

            for sentence in data_sentences:

                if sentence:
                    initialized_data(file, sentence, offset)
                    
                offset += 1

    with open("data.json", "w") as f:
        json.dump(data, f, cls=SetEncoder)

    with open('sentences.pkl', 'wb') as sentences:
        pickle.dump(list_data_sentences, sentences)


preparing_system()

