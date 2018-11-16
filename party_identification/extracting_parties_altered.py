# -*- coding: utf-8 -*-
#Algorithm to extract parties from contracts
import re
import os
import nltk
import hashlib
from nltk.corpus import stopwords
from copy import deepcopy


# Global variables.
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
entities_list = open('data/entities_list.txt', 'r').readlines()
dictionary = {}

for entity in entities_list:
    key = hashlib.md5(entity[:-1]).digest()
    dictionary[key] = entity

#unused function
def truecase_ner(stanfordCoreNLP, sentence):
  r_dict = stanfordCoreNLP._request('truecase,ner', sentence)
  words = []
  ner_tags = []
  for s in r_dict['sentences']:
    for token in s['tokens']:
      words.append(token['originalText'])
      ner_tags.append(token['ner'])
  return list(zip(words, ner_tags))

#altered to add stanfordCoreNLP
def find_entities(block_entities, stanfordCoreNLP):
    # Function that finds entities in the sentence and returns a list with them.

    entities  = []
    nicknames = ['', '']

    block_nick = re.compile(r'\(\"?.+?\"?\)')
    extract_nick = re.compile(r'[\'\`\(\"\"\)]|& quot ;|Hereinafter |hereinafter | referred | to | as ')

    if block_entities.__contains__('AND'):
        try:
            entities.append(' '.join(block_entities[1:block_entities.index('AND')]))
            entities.append(' '.join(block_entities[block_entities.index('AND')+1:]))
        except:
            pass
    else:
        try:
            entities.append(' '.join(block_entities[1:block_entities.index('and')]))
            entities.append(' '.join(block_entities[block_entities.index('and')+1:]))
        except:
            pass

    found = [False, False]
    #Code block that looks for the entities inside the wiki list
    for ind in range(len(entities)):
        entity = entities[ind].split()
        for index in range(len(entity)):
            counter = index
            while counter <= len(entity):
                key = hashlib.md5(' '.join(entity[index:counter])).digest()
                if dictionary.has_key(key):
                    found[ind] = True
                    block = block_nick.findall(entities[ind])
                    if block:
                        nick = extract_nick.sub("", block[0])
                    if nick:
                        nicknames[ind] = nick                        
                    entities[ind] = ' '.join(entity[index:counter])
                    break
                counter += 1
    #print entities
    #code block that looks for entities if they were not found in the wiki list
    for index in range(len(found)):
        if not found[index]:
            block = block_nick.findall(entities[index])
            if block:
                nick = extract_nick.sub("", block[0])
                if nick:
                    nicknames[index] = nick
                else:
                    nicknames[index] = ''                    
            #Altered to use StanfordCoreNLP
            taggedText = stanfordCoreNLP.ner(entities[index])
            # print taggedText
            contractParty = [name for (name, tag) in taggedText if tag == u'ORGANIZATION']
            
            # The ner function might be unable to detect some company names. In this case
            # a more generic approach is used, collecting the proper nouns (NNP) from a
            # part-of-speech tagged sentence
            if len(contractParty) == 0:
              taggedText = stanfordCoreNLP.pos_tag(entities[index])
              print taggedText
              contractParty = [name for (name, tag) in taggedText if tag == u'NNP' or tag == u'NN' ]
              
            entities[index] = ' '.join(contractParty)
            

    return entities, nicknames

#altered to add stanfordCoreNLP
def extract_parties(contract, stanfordCoreNLP):
    # Function that opens and process a contract in order to identify parties.

    entities = []

    regex = re.compile('BETWEEN[\r]*.+ AND.+', re.I)
    regex_2 = re.compile('AMONG[\r]*.+ AND.+', re.I)
    if type(contract) != str:
        return "You need to input a path in a string format."

    fileName, fileExtension = os.path.splitext(contract)        
    if fileExtension == '':
        return "You need to add a file path containing the file name.\nFor example: /path/to/file.txt"
            
    contract_text = ' '.join(open(contract, 'r').read().split())
    
    try:
        contract_sents = sent_tokenizer.tokenize(contract_text)
    except:
        print "I can't parse this file: ", contract_file
    
    for sentence in contract_sents:            
        list_tokens = nltk.word_tokenize(sentence)
        sentence = ' '.join(list_tokens)
        block = regex.findall(sentence)
        if block:
            block_entities = block[0].split()
            #altered to add stanfordCoreNLP
            entities = find_entities(block_entities, stanfordCoreNLP)
            break
        else:
            block = regex_2.findall(sentence)
            if block:
                block_entities = block[0].split()
                #altered to add stanfordCoreNLP
                entities = find_entities(block_entities, stanfordCoreNLP)
                break
    if entities:
        return entities
    else:
        print "No entity was found"
