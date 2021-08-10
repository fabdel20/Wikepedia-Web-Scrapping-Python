import wikipediaapi
import wikipedia 
import nltk
import math 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

name = input("Enter Wikipedia Page Name or link: ")
if("https://en.wikipedia.org/wiki/" in name):
    replace = ""
    for i in range(30, len(name)):
        if(i != "_"):
            replace = replace + name[i]
    name = replace
language = wikipediaapi.Wikipedia('en')
page = language.page(name)
link = wikipedia.page(name)

print("Title: %s" % page.title)
print("Summary: %s" % wikipedia.summary(name, sentences=2))

sectDict = dict()

# This produces a dictionary with all the section names in the page
def get_sections(sections, level=0):
    for s in sections:
        sectDict[s.title] = level
        get_sections(s.sections, level + 1)

# This gets the frequency of every word in the entire page, not including 
# stop words
def wordFrequency(page):
    dictionary = dict()
    stop_words = set(stopwords.words('english'))
    mostFrequent = dict()
    for line in page.splitlines(): 
        for word in line.split(" "):
            if (word.lower() not in stop_words):
                letters = False
                for char in word:
                    if(char.isalpha()):
                        letters = True
                    else:
                        letters = False
                        break 
                if(word in dictionary and letters == True):
                    dictionary[word] += 1
                if(word not in dictionary and letters == True):
                    dictionary[word] = 1
    return dictionary

# this finds the most frequent words 
def mostFrequentWords(page):
    dictionary = wordFrequency(page)
    mostFrequent = dict()
    mfList = list()
    numList = list()
    countHighest = 1
    countMiddle = 1
    countLower = 1 
    total = 0 
    num = 0
    for word in dictionary: 
        num += 1 
        total += dictionary[word]
    if(num != 0):
        average = total / num
    for word in dictionary:
        val = dictionary[word]
        if (val >= countHighest or  val >= countMiddle or val >= countLower):
            if(val >= countHighest):
                countHighest = val
                mostFrequent[word] = val
                mfList.append(word)
                numList.append(num)
            if(val >= countMiddle and val <= countHighest):
                countMiddle = val
            else:
                countLower = val
    if(len(mostFrequent) > 0):
        print(mfList)
    else:
        print("This section was empty")

# Uses all helper functions to produce the section name, most frequent words
# and URLs included in the section 
def eachSection(page):
    get_sections(page.sections)
    text = page.text
    indexDict = dict()
    section = list()
    count = 0   
    place = 0  
    for word in sectDict:
        section.append(word)
        index = text.find(word)
        indexDict[count] = index
        count += 1
    for index in range(len(indexDict) - 1):
        num = index + 1
        startIndex = indexDict[index]
        endIndex = indexDict[num]
        string = text[startIndex : endIndex]
        linkList = list()
        for l in link.links:
            if(l in string):
                linkList.append(l)
        print("Section Title: " + section[index])
        print("Most Frequent Words:")
        mostFrequentWords(string)
        print("URL Links")
        if(len(linkList) > 0):
            print(linkList)
            print("-" * 15)
        else:
            print("No URL links are included in the section")
            print("-" * 42)

eachSection(page)
