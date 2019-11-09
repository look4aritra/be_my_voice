text = "this is a sample text"


def list2string(data):
    return " ".join(map(str, data))


def getwordgroup(sentence, searchword, maxright=0, expectstring=False):
    words = sentence.split(" ")
    searchresult = []
    if searchword in words:
        indexofword = words.index(searchword)
        print("Found {" + searchword + "} at position " + str(indexofword + 1))
        if maxright > 0:
            if (indexofword + maxright) >= len(words):
                print("specified right limit exceed length, can use additional " +
                      str(len(words) - words.index(searchword) - 1) + " word(s)")
                searchresult = [words[ind]
                                for ind in list(range(indexofword, len(words)))]
            else:
                print("fetching " + str(maxright) +
                      " word(s) right of position " + str(indexofword+1))
                searchresult = [
                    words[ind]
                    for ind in list(
                        range(indexofword, indexofword + maxright + 1))]
        else:
            if (indexofword + maxright) <= 0:
                print(
                    "specified left limit is below zero, can use additional " +
                    str(words.index(searchword)) + " word(s)")
                searchresult = [words[ind]
                                for ind in list(range(0, indexofword + 1))]
            else:
                print("fetching " + str(maxright) +
                      " word(s) before position " + str(indexofword + 1))
                searchresult = [
                    words[ind]
                    for ind in list(
                        range(indexofword + maxright, indexofword + 1))]
    else:
        print("No matching word found")
    if expectstring:
        searchresult = list2string(searchresult)
    print(searchresult)
    return searchresult


def getwordgroupby(sentence, searchstring, maxright=0, expectstring=True):
    searchwords = searchstring.split(" ")
    # print(searchwords)
    searchresult = ""
    if len(searchwords) <= 1:
        print("performing standard search")
        searchresult = getwordgroup(
            sentence, searchstring, maxright, True)
    else:
        print("search string has multiple word")
        if maxright > 0:
            print("using last word to search")
            searchresult = getwordgroup(
                sentence, searchwords[-1], maxright, True)
            # print(list2string(searchwords[:-1]))
            searchresult = list2string(searchwords[:-1]) + " " + searchresult
        else:
            print("using first word to search")
            searchresult = getwordgroup(
                sentence, searchwords[0], maxright, True)
            searchresult = searchresult + " " + list2string(searchwords[1:])
    if not expectstring:
        searchresult = searchresult.split(" ")
    print(searchresult)
    return searchresult


# getwordgroup(text, "this", 2, True)
# getwordgroup(text, "sample", 10)
# getwordgroup(text, "is", 4, True)
# getwordgroup(text, "a", 2)
# getwordgroup(text, "is", 2)
# getwordgroup(text, "text", 2)

# getwordgroupby(text, "is a", 2)
# getwordgroupby(text, "is a", 20)
# getwordgroupby(text, "text", 2)

# getwordgroup(text, "this", -2)
# getwordgroup(text, "text", -2)
# getwordgroup(text, "sample", -20)

# getwordgroupby(text, "a", 2)
# getwordgroupby(text, "a", -2)

# getwordgroupby(text, "is a", 2)
# getwordgroupby(text, "a sample", -2)
