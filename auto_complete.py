from collections import defaultdict
import json
data = defaultdict(set)

class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score
    def get_completed_sentence(self):
        return self.completed_sentence
    def get_score(self):
        return self.score
    def set_score(self, num):
        self.score -= num
def initialized_data():
    data_file = open("about.txt")
    data_sentences = data_file.read().split("\n")
    for sentence in data_sentences:
        if sentence:
            # first_word = sentence.split()[0]
            for i in range(len(sentence)):
                for j in range(i + 1, len(sentence) + 1):
                    data[sentence[i: j]].add(AutoCompleteData(sentence, "file.txt", 0, 2*len(sentence[i: j])))
            # first_word = sentence.split()[0]         
            # for i in range(len(first_word)):
            #   for j in range(i + 1, len(first_word) + 1):        
            #       data[first_word[i: j]].add(AutoCompleteData(sentence, "file.txt", 0, 2*len(first_word[i: j])))
    with open("data.json", "w") as f:
        for key in data.keys():
            for a in data[key]:
                json.dump({key:a.get_completed_sentence()}, f)

def earase_prefix(prefix):
    earased_prefix =  []
    for i in range(len(prefix)):
        substring_for_search = data.get(prefix.replace(prefix[i], "", 1))
        if(substring_for_search):
            substring_for_search.set_score(10 - 2 * i + 2) if i < 4 else substring_for_search.set_score(2 + 2)
            earased_prefix.append(substring_for_search)
    return earased_prefix
    
def change_prefix(prefix):
    changed_prefix =  []
    for i in range(len(prefix)):
        for letter in range(ord('a'), ord('z') + 1):
            substring_for_search = data.get(prefix.replace(prefix[i], letter, 1))
            if substring_for_search:
                substring_for_search.set_score(5 - i + 2) if i < 4 else substring_for_search.set_score(2 + 2)
                changed_prefix.append(substring_for_search)
    return changed_prefix

def add_prefix(prefix):
    added_prefix = []
    for i in range(len(prefix) + 1):
        for letter in range(ord('a'), ord('z') + 1):
            substring_for_search = data.get(prefix[:i] + letter + prefix[i:])
            if substring_for_search:
                substring_for_search.set_score(5 - i + 2) if i < 4 else substring_for_search.set_score(2 + 2)
                changed_prefix.append(substring_for_search)
    return added_prefix

def complete_prefix(prefix):
    completed_prefix = add_prefix(prefix)
    completed_prefix += change_prefix(prefix)
    completed_prefix +=  earase_prefix(prefix)
    return completed_prefix

def get_best_k_completions(prefix):
    founded_completions = list(data.get(prefix))
    if len(founded_completions) < 5:
        founded_completions += complete_prefix(prefix) 
    founded_completions = sorted(founded_completions, key=lambda x: (x.get_score, x.get_completed_sentence))
    return founded_completions[:5]
    # print(data)
initialized_data()