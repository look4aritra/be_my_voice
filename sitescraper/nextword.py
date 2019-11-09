text = "this is a sample text"


def getwordgroup(sentence, searchword, maxright=0, expectstring=False):
    words = sentence.split(" ")
    searchresult = []
    if searchword in words:
        indexofword = words.index(searchword)
        print("Found {" + searchword + "} at position " + str(indexofword + 1))
        if (indexofword + maxright) >= len(words):
            print(
                "specified right limit exceed length, can use additional " + str(len(words) - words.index(searchword) - 1) + " word(s)")
            searchresult = [words[ind]
                            for ind in list(range(indexofword, len(words)))]
        else:
            print("fetching " + str(maxright) +
                  " word(s) from position " + str(indexofword+1))
            searchresult = [words[ind]
                            for ind in list(range(indexofword, indexofword + maxright))]
    else:
        print("No matching word found")
    if expectstring:
        searchresult = " ".join(map(str, searchresult))
    print(searchresult)
    return searchresult


getwordgroup(text, "this", 2, True)
getwordgroup(text, "sample", 10)
getwordgroup(text, "is", 4, True)
getwordgroup(text, "a", 2)
getwordgroup(text, "is", 2)
getwordgroup(text, "text", 2)
