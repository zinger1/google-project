from online.load import data, list_data_sentences
from utils.ignore_casing import ignore_casing
from copy import deepcopy


class AutoComplete:

    def __init__(self, prefix):
        self.prefix = ignore_casing(prefix)
        self.len_prefix = len(self.prefix)
        self.founded_completions = {}

    def get_founded_completions(self):
        return self.founded_completions

    def update_founded_completions(self, obj):
        search_obj = self.founded_completions.get(obj.get_completed_sentence())

        if search_obj:

            if obj.get_score() > search_obj.get_score():
                search_obj.set_score(obj.get_score())
        else:
            self.founded_completions[obj.get_completed_sentence()] = obj

    def change_prefix(self):

        for i in range(self.len_prefix):
            for letter in range(ord('a'), ord('z') + 1):
                if chr(letter) not in self.prefix:
                    substring_for_search = data.get(self.prefix.replace(self.prefix[i], chr(letter), 1))
                    if substring_for_search:
                        for index_of_auto_complete_data in substring_for_search:
                            changed = deepcopy(list_data_sentences[index_of_auto_complete_data])
                            changed.set_score(2 * (self.len_prefix - 1) - (1 if i > 3 else 5 - i))
                            self.update_founded_completions(changed)

    def erase_prefix(self):

        for i in range(self.len_prefix):
            for letter in range(ord('a'), ord('z') + 1):
                if chr(letter) not in self.prefix:
                    substring_for_search = data.get(self.prefix[:i] + chr(letter) + self.prefix[i:])
                    if substring_for_search:
                        for index_of_auto_complete_data in substring_for_search:
                            erased = deepcopy(list_data_sentences[index_of_auto_complete_data])
                            erased.set_score(2 * (self.len_prefix) - (2 if i > 3 else 10 - 2 * i))
                            self.update_founded_completions(erased)

    def add_prefix(self):

        for i in range(self.len_prefix):
            substring_for_search = data.get(self.prefix.replace(self.prefix[i], "", 1))
            if substring_for_search:
                for index_of_auto_complete_data in substring_for_search:
                    added = deepcopy(list_data_sentences[index_of_auto_complete_data])
                    added.set_score(2 * (self.len_prefix - 1) - (2 if i > 3 else 10 - 2 * i))
                    self.update_founded_completions(added)

    def complete_prefix(self):
        self.change_prefix()
        self.erase_prefix()
        self.add_prefix()
        self.founded_completions = {k: v for k, v in
                                    sorted(self.get_founded_completions().items(), key=lambda item: item[1].get_score(),
                                           reverse=True)}


def get_best_k_completions(prefix):
    k = 5
    completions = AutoComplete(prefix)

    if data.get(completions.prefix):

        for item in data.get(completions.prefix):
            complete = list_data_sentences[item]
            complete.set_score(2 * len(completions.prefix))
            completions.update_founded_completions(complete)

    if len(completions.get_founded_completions()) < k:
        completions.complete_prefix()

    completion_list = [value for value in completions.get_founded_completions().values()]

    return completion_list[:k]
