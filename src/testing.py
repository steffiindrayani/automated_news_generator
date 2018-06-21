# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 12:52:33 2018

@author: User
"""

#from automated_news_generator import automatedNewsGeneration
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
from nltk import word_tokenize
from string import punctuation

def readFile(filename):
    with open(filename, 'r', encoding='utf-8') as myfile:
        return myfile.read()

def stringToList(text):
    words = word_tokenize(text)
    # print(words)
    return words


# def readLineinFile(filename):
# 	ref = []
# 	with open(filename, 'r') as f:
# 		lines = f.readlines()
# 		for line in lines:
# 			line = line.lower()
# 			a = stringToList(line)
# 			ref.append([a])
# 	return ref

# def readLineinFile2(filename):
# 	hyp = []
# 	with open(filename, 'r') as f:
# 		lines = f.readlines()
# 		for line in lines:
# 			line = line.lower()
# 			a = stringToList(line)
# 			hyp.append(a)
# 	return hyp
    
# def readReferences():
# 	refs = []
# 	for i in range(0,32):
# 		a = i + 1
# 		ref = readFile("../testset/test"+str(a)).lower()
# 		ref = stringToList(ref)
# 		refs.append(ref)
# 	return refs

# def readReferences():
# 	refs1 = []
# 	refs2 = []
# 	reference = readFile("../testset/test"+str(1))
# 	ref = stringToList(reference.lower())
# 	refs1.append(ref)
# 	ref = sentenceSplit(reference)
# 	refs2.extend(ref)
# 	return refs1, refs2

#DARI SINI##
# def readReferences1():
# 	refs1 = []
# 	refs2 = []
# 	for i in range(0,1):
# 		a = i + 1
# 		reference = readFile("../trainset/test"+str(a))
# 		ref = stringToList(reference.lower())
# 		refs1.append(ref)
# 		ref = sentenceSplit(reference)
# 		refs2.extend(ref)
# 	return refs1, refs2

def readReferences():
	refs1 = []
	refs2 = []
	for i in range(0,35):
		a = i + 1
		reference = readFile("../testset/test"+str(a))
		ref = stringToList(reference.lower())
		refs1.append(ref)
		ref = sentenceSplit(reference)
		refs2.extend(ref)
	return refs1, refs2

def sentenceSplit(sentence):
	sentences = []
	listofwords = ['kh','h','hj','drs','hi', 'ir']
	words = stringToList(sentence)
	sentence = ""
	for i in range(0, len(words) - 1):
		if words[i+1] != "":
			if (words[i] == "." and words[i+1][0].isupper() and i != 0 and words[i-1].lower() not in listofwords):
				sentence += words[i]
				sentence = stringToList(sentence.lower())
				sentences.append(sentence)
				sentence = ""
			else:
				sentence += words[i] + " "

	sentence += words[len(words) - 1]
	sentence = stringToList(sentence.lower())
	sentences.append(sentence)
	return sentences

#check 
article = readFile("../results/article.txt")
hyp1 = stringToList(article.lower())
hyp2 = sentenceSplit(article)
ref1, ref2 = readReferences()
#ref3, ref4 = readReferences2()
#print(hyp1)
#print(ref1)
sf = SmoothingFunction()
#print(hyp1)
#print(hyp2)
print("training")
print(sentence_bleu(ref1, hyp1))

print(" ")


max1, max2, min1, min2 = -999, -999, 999, 999
count = len(hyp2)
bleu4 = 0
bleu3 = 0
sen1, sen2, sen3, sen4 = "", "", "", ""

for sentence in hyp2:
	a = sentence_bleu(ref2, sentence)
	b = sentence_bleu(ref2, sentence, weights=(0.33, 0.33, 0.33, 0))
	print(sentence, a, )
	bleu4 += a
	bleu3 += b
	if a > max1:
		max1 = a
		sen1 = sentence
	if a < min1:
		min1 = a
		sen2 = sentence
	if b > max2:
		max2 = b
		sen3 = sentence
	if b < min2:
		min2 = b
		sen4 = sentence


print("avg4:", bleu4/count)
print("max4:", max1, sen1)
print("min4:", min1, sen2)
# print("avg4:", bleu3/count)
# print("max4:", max2, sen3)
# print("min4:", min2, sen4)

# print("testing")
# print(sentence_bleu(ref3, hyp1))

# print(" ")


# max1, max2, min1, min2 = -999, -999, 999, 999
# count = len(hyp2)
# bleu4 = 0
# bleu3 = 0
# sen1, sen2, sen3, sen4 = "", "", "", ""

# for sentence in hyp2:
# 	a = sentence_bleu(ref4, sentence)
# 	#print(sentence, a, )
# 	bleu4 += a
# 	bleu3 += b
# 	if a > max1:
# 		max1 = a
# 		sen1 = sentence
# 	if a < min1:
# 		min1 = a
# 		sen2 = sentence
# 	if b > max2:
# 		max2 = b
# 		sen3 = sentence
# 	if b < min2:
# 		min2 = b
# 		sen4 = sentence


# print("avg4:", bleu4/count)
# print("max4:", max1, sen1)
# print("min4:", min1, sen2)

