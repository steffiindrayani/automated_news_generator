# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 12:52:33 2018

@author: User
"""

#from automated_news_generator import automatedNewsGeneration
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
from string import punctuation

def readFile(filename):
    with open(filename, 'r') as myfile:
        return myfile.read()

def stringToList(text):
    words = text.split()
    return words

def readLineinFile(filename):
	ref = []
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			line = line.lower()
			a = stringToList(line)
			ref.append([a])
	return ref

def readLineinFile2(filename):
	hyp = []
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			line = line.lower()
			a = stringToList(line)
			hyp.append(a)
	return hyp
    
#article1 = readFile("../results/article.txt").lower()
# article2 = readFile("../results/article2.txt").lower()
#article1 = readFile("../results/article.txt").lower()
#test1 = readFile("../testset/test2").lower()
#test2 = readFile("../testset/test1.1").lower()

#article1 = ''.join(ch for ch in article1 if ch not in exclude).lower()
#article2 = ''.join(ch for ch in article2 if ch not in exclude).lower()
#test1 = ''.join(ch for ch in test1 if ch not in exclude).lower()
#test2 = ''.join(ch for ch in test2 if ch not in exclude).lower()

#hyp1 = stringToList(article1)
#hyp2 = stringToList(article2)
#ref1 = [stringToList(test1)]
#ref2 = stringToList(test2)
# print(hyp1)
# print(hyp2)
# print(ref1)
# print(ref2)
hyp1 = readLineinFile2("../results/article.txt")
ref1 = readLineinFile("../testset/test2")
print(hyp1)
print(ref1)

#for i in range(0,9):

#	print(sentence_bleu(ref1[i], hyp1[i]))

sf = SmoothingFunction()
print(len(ref1))
print(len(hyp1))
print("1 ref, 1 hyp")
#print(corpus_bleu(ref1, hyp1))

print(corpus_bleu(ref1, hyp1))
print(sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7))

# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method1))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method1))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method1))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method2))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method2))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method2))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method2))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method3))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method3))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method3))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method3))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method4))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method4))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method4))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method4))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method5))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method5))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method5))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method5))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method6))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method6))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method6))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method6))

# # print('ref1, hyp1', sentence_bleu([ref1], hyp1, smoothing_function=sf.method7))
# # print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method7))
# # print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method7))
# # print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method7))

# # print("2 ref, 1 hyp")
# print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method1))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method2))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method2))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method3))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method3))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method4))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method4))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method5))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method5))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method6))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method6))

# # print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7))
# # print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method7))


print(sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(0.33, 0.33, 0.33, 0)))
# #print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method7, weights=(0.33, 0.33, 0.33, 0)))
# #print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method7, weights=(0.33, 0.33, 0.33, 0)))
# #print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method7, weights=(0.33, 0.33, 0.33, 0)))

print(sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(0.5, 0.5, 0, 0)))
print(sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))
# #print('ref1, hyp2', sentence_bleu([ref1], hyp2, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))
# #print('ref2, hyp1', sentence_bleu([ref2], hyp1, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))
# #print('ref2, hyp2', sentence_bleu([ref2], hyp2, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))

# print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(0.33, 0.33, 0.33, 0)))
# #print('ref1 ref2, hyp2', sentence_bleu([ref1, ref2], hyp2, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))
# print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(0.5, 0.5, 0, 0)))
# print('ref1 ref2, hyp1', sentence_bleu([ref1, ref2], hyp1, smoothing_function=sf.method7, weights=(1, 0, 0, 0)))


