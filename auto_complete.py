from collections import defaultdict
import json
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

    def get_score(self):
        return self.score

    def set_score(self, num):
        self.score -= num

def initialized_data():

    offset = 0
    data_file = open("about.txt")
    data_sentences = data_file.read().split("\n")

    
    for sentence in data_sentences:
        
        if sentence:
            
            for i in range(len(sentence)):

                for j in range(i + 1, len(sentence) + 1):
                    new_data = AutoCompleteData(sentence, "file.txt", offset, 2*len(sentence[i: j]))

                    data[sentence[i: j]].add(offset)

            list_data_sentences.append(new_data)
            offset += 1

    # for item in data:
    #     print(data[item])

    # with open("data.json", "w") as f:

    #     for key in data.keys():
        
    #         for a in data[key]:
    #             json.dump({key:a.get_completed_sentence()}, f)

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
    founded_completions = [*data.get(prefix),]

    # if len(founded_completions) < 5:
    #     founded_completions += complete_prefix(prefix) 
    founded_completions = sorted(list(map(lambda x: list_data_sentences[x], founded_completions)), key=lambda x: (x.get_score(), x.get_completed_sentence()))
    # founded_completions = sorted(founded_completions, key=lambda x: (list_data_sentences[x].get_score(), x.get_completed_sentence()))
    
    return founded_completions[:5]


def menu():
    print("Loading the files and preparing the system...")
    initialized_data()
    print("The system is ready. Enter your text:")
    prefix = input()
    best_completions_of_prefix = get_best_k_completions(prefix)
    print(best_completions_of_prefix)
    for complete in best_completions_of_prefix:
        print(complete.completed_sentence, complete.offset, complete.score) 

menu()