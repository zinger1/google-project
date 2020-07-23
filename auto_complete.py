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

def add_prefix(prefix):
    added_prefix =  set()

    for i in range(len(prefix)):
        substring_for_search = data.get(prefix.replace(prefix[i], "", 1))
        
        if substring_for_search:
            for index_of_auto_complete_data in substring_for_search:
                added = deepcopy(list_data_sentences[index_of_auto_complete_data])
                added.set_score(2*(len(prefix) -1) - (2 if i > 3 else 10 - 2*i))
                added_prefix.add(added)
    return added_prefix
    
def change_prefix(prefix):
    changed_prefix = set()

    for i in range(len(prefix)):
        for letter in range(ord('a'), ord('z') + 1):
            if chr(letter) not in prefix:
                substring_for_search = data.get(prefix.replace(prefix[i], chr(letter), 1))
                if substring_for_search:
                    for index_of_auto_complete_data in substring_for_search:
                        changed = deepcopy(list_data_sentences[index_of_auto_complete_data])
                        changed.set_score(2*(len(prefix) -1) - (1 if i > 3 else 5 - i))
                        changed_prefix.add(changed)
    return changed_prefix

def earase_prefix(prefix):
    earased_prefix = set()

    for i in range(len(prefix) + 1):
        for letter in range(ord('a'), ord('z') + 1):
            if chr(letter) not in prefix:
                substring_for_search = data.get(prefix[:i] + chr(letter) + prefix[i:])
                if substring_for_search:
                    for index_of_auto_complete_data in substring_for_search:
                        earased = deepcopy(list_data_sentences[index_of_auto_complete_data])
                        earased.set_score(2*(len(prefix)) - (2 if i > 3 else 10 - 2*i))
                        earased_prefix.add(earased)

    return earased_prefix

def complete_prefix(prefix):
    completed_prefix = earase_prefix(prefix)
    completed_prefix.update(change_prefix(prefix))
    completed_prefix.update(add_prefix(prefix))
    return completed_prefix

def get_best_k_completions(prefix):
    founded_completions = set()
    if data.get(prefix): 
        for item in data.get(prefix):
            complete = list_data_sentences[item]  
            complete.set_score(2 * len(prefix)) 
            founded_completions.add(complete)
        # founded_completions.update([list_data_sentences[item] for item in data.get(prefix)])
    if len(founded_completions) < 5:
        founded_completions.update(complete_prefix(prefix)) 
    founded_completions = sorted( founded_completions, key=lambda x: (x.get_score(), x.get_completed_sentence()), reverse=True)
    
    return founded_completions[:5]


def menu():
    print("Loading the files and preparing the system...")
    initialized_data()
    print("The system is ready. Enter your text:")
    prefix = input()
    while(True):
        if("#" == prefix[-1]):
            prefix = input()

        best_completions_of_prefix = get_best_k_completions(prefix_ignore_casing(prefix))
        if best_completions_of_prefix:
            for complete in best_completions_of_prefix:
                print(complete.get_completed_sentence(), complete.get_source_text(), complete.get_offset(), complete.get_score())
            print(prefix, end="")
            prefix += input()
        else:
            print("There are no suggestions")
            break

menu()
