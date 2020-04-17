import math


#reading the txt and cleaning ".","," and etc.
with open("tf-idt-text.txt", 'r', encoding='utf8') as read:
    tf_idf = read.readlines()
documents = []
tf_idf_word_list = []
for i in range(len(tf_idf)):
    documents += tf_idf[i].replace("\n",'').replace(',','').replace("?","").replace("(","").replace(")","").lower().split('. ')
documents[-1] = documents[-1].replace('.','')

#Calculating TF(Term Frequency)
#Tokenize words
dictOfWords = {}

for index, sentence in enumerate(documents):
    tokenizedWords = sentence.split(' ')
    dictOfWords[index] = [(word, tokenizedWords.count(word)) for word in tokenizedWords]

#remove duplicates in dictOfWords
termFrequency = {}

for i in range(len(documents)):
    listOfNoDuplicates = []
    for wordFreq in dictOfWords[i]:
        if wordFreq not in listOfNoDuplicates:
            listOfNoDuplicates.append(wordFreq)
        termFrequency[i] = listOfNoDuplicates

# TF normalized term frequency
normalizedTermFrequency = {}
for i in range(len(documents)):
    sentence = dictOfWords[i]
    lenOfSentence = len(sentence)
    listOfNormalized = []
    for wordFreq in termFrequency[i]:
        normalizedFreq = wordFreq[1]/lenOfSentence
        listOfNormalized.append((wordFreq[0],normalizedFreq))
    normalizedTermFrequency[i] = listOfNormalized

# Calculating IDF(Inverse Document Frequency)

#Put all sentences together and tokenize

allDocuments = ''
for sentence in documents:
    allDocuments += sentence + ' '
allDocumentsTokenized = allDocuments.split(' ')

allDocumentsNoDuplicates = []

for word in allDocumentsTokenized:
    if  word not in allDocumentsNoDuplicates:
        allDocumentsNoDuplicates.append(word)

#Calculate the number of documents where the term t appears

dictOfNumberOfDocumentsWithTermInside = {}

for index, vocabulary in enumerate(allDocumentsNoDuplicates):
    count = 0
    for sentence in documents:
        if vocabulary in sentence:
            count += 1
    dictOfNumberOfDocumentsWithTermInside[index] = (vocabulary, count)

# Calculate IDF

dictOFIDFNoDuplicates = {}

for i in range(len(normalizedTermFrequency)):
    listOFIDFCalcs = []
    for word in normalizedTermFrequency[i]:
        for x in range(len(dictOfNumberOfDocumentsWithTermInside)):
            if word[0] == dictOfNumberOfDocumentsWithTermInside[x][0]:
                listOFIDFCalcs.append((word[0], math.log((len(documents)/dictOfNumberOfDocumentsWithTermInside[x][1]))))
    dictOFIDFNoDuplicates[i] = listOFIDFCalcs

# Multiply TF*IDF = TFIDF

dictOFTF_IDF = {}
for i in range(len(normalizedTermFrequency)):
    listOFTF_IDF = []
    TFsentence = normalizedTermFrequency[i]
    IDFsentence = dictOFIDFNoDuplicates[i]
    for x in range(len(TFsentence)):
        listOFTF_IDF.append((TFsentence[x][0], TFsentence[x][1]*IDFsentence[x][1]))
    dictOFTF_IDF[i] = listOFTF_IDF

print(dictOFTF_IDF)
