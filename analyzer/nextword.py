# -*- coding: utf-8 -*-

from utilities import list2string


def get_wordgroup(sentence, search_word, max_right=0, expect_string=False):
    words = sentence.split(" ")
    # print(words)
    search_result = []
    if search_word in words:
        index_of_word = words.index(search_word)
        print("Found {" + search_word + "} at position "
              + str(index_of_word + 1))
        search_result = words[index_of_word:len(words)] \
            if (index_of_word + max_right) >= len(words) \
            else words[index_of_word:(index_of_word + max_right + 1)] \
            if max_right > 0 else \
            words[0: index_of_word + 1] \
            if (index_of_word + max_right) <= 0 \
            else words[(index_of_word + max_right):index_of_word + 1]
    if expect_string:
        search_result = list2string(search_result)
    # print(search_result)
    return search_result


def get_wordgroup_by(sentence, search_string, max_right=0, expect_string=True):
    search_words = search_string.split(" ")
    # print(search_words)
    search_result = ""
    if len(search_words) <= 1:
        # print("performing standard search")
        search_result = get_wordgroup(
            sentence, search_string, max_right, True)
    else:
        # print("search string has multiple word")
        search_result = list2string(search_words[:-1]) + " " + \
            get_wordgroup(sentence, search_words[-1], max_right, True) \
            if max_right > 0 else \
            get_wordgroup(sentence, search_words[0], max_right, True) \
            + " " + list2string(search_words[1:])
    if not expect_string:
        search_result = search_result.split(" ")
    # print(search_result)
    return search_result


# get_wordgroup("this is a sample text", "this", 2, True)
# get_wordgroup("this is a sample text", "sample", 10)
# get_wordgroup("this is a sample text", "is", 4, True)
# get_wordgroup("this is a sample text", "a", 2)
# get_wordgroup("this is a sample text", "is", 2)
# get_wordgroup("this is a sample text", "text", 2)

# get_wordgroup("this is a sample text", "this", -2)
# get_wordgroup("this is a sample text", "text", -2)
# get_wordgroup("this is a sample text", "sample", -20)

# get_wordgroup_by("this is a sample text", "is a", 2)
# get_wordgroup_by("this is a sample text", "is a", 20)
# get_wordgroup_by("this is a sample text", "text", 2)

# get_wordgroup_by("this is a sample text", "a", 2)
# get_wordgroup_by("this is a sample text", "a", -2)

# get_wordgroup_by("this is a sample text", "is a", 2)
# get_wordgroup_by("this is a sample text", "a sample", -2)

# get_wordgroup_by("this is a sample text", "a sample text", -2)
# get_wordgroup_by("this is a sample text", "this is a", 2)
