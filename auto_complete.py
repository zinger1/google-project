

from collections import defaultdict
from copy import deepcopy

data = defaultdict(set)
list_data_sentences = []

class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def get_completed_sentence(self):
        return self.completed_sentence

    def get_source_text(self):
        return self.source_text

    def get_offset(self):
            return self.offset

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    

def prefix_ignore_casing(prefix):
    prefix = "".join(filter(lambda x: x.isalnum() or x.isspace(), prefix)).lower()
    prefix = " ".join(prefix.split())
    return prefix


def initialized_data():

    id_sentence = 0
    file_name = "about.txt"
    data_file = open("about.txt", encoding="utf8")
    data_sentences = data_file.read().split("\n")
    offset = 1
    
    for sentence in data_sentences:
        
        if sentence:
            for i in range(len(sentence)):
                for j in range(i + 1, len(sentence) + 1):
                    data[prefix_ignore_casing(sentence[i: j])].add(id_sentence)
            new_data = AutoCompleteData(sentence, file_name, offset, 0)
            list_data_sentences.append(new_data)
            id_sentence += 1
        offset += 1


