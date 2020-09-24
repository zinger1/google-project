import pickle
import json


def load_text_sources():

    print("Loading the files and prepraring the system...")

    with open("../offline/data.json", "r") as data_file:
        data = json.load(data_file)

    with open("../offline/sentences.pkl", "rb") as sentences_file:
        sentences = pickle.load(sentences_file)

    return data, sentences


data, list_data_sentences = load_text_sources()
