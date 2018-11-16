import sent2vec
import scipy.spatial as spsp
import math
import re

remove_punctuation = re.compile(r'[\"\#\$\%\&\\\'\(\)\*\+\,\-\/\:\;\<\=\>\@\[\\\\\]\^\_\`\{\|\}\~]+')

#Includes periods, question marks and exclamations
remove_punctuation_2 = re.compile(r'[\"\#\$\%\&\\\'\(\)\*\+\,\-\/\:\;\<\=\>\@\[\\\\\]\^\_\`\{\|\}\~\.\?!]+')

#Does not remove periods, question marks and exclamations
def cleanSent(sent):
  return remove_punctuation.sub('', sent.lower())

#Also removes periods, question marks and exclamations
def cleanSent2(sent):
  return remove_punctuation_2.sub('', sent.lower())



# This class is used as an interface to sent2vec. It keeps the trained models on memory for use
# during contract processing and adds the distance functions for euclidean and cosine distance
# provided by scipy.
class SimilarityChecker:
  
  # Instanciate the Similarity Checker with some trained model
  def __init__(self, trainedModel='torontobooks_unigrams.bin'):
    print 'Creating empty sent2vec model...'
    self.model = sent2vec.Sent2vecModel() #keeps the trained model on memory
    print 'Loading trained model. This might take a while...'
    self.model.load_model(trainedModel)
    print 'Model %s loaded' % trainedModel
  
  #Embed 2 sentences and return their euclidean distance
  def similarityED(self, sent1, sent2):
    embs = self.embedSentences(sent1, sent2)
    return self.euclideanDistance(embs[0], embs[1])
    
  #Embed 2 sentences and return their cosine distances
  def similarityCD(self, sent1, sent2):
    embs = self.embedSentences(sent1, sent2)
    #if self.nullVector(embs[0]):
      #print 'Null vector found'
      #print sent1
      #exit()
    #if self.nullVector(embs[1]):
      #print 'Null vector found'
      #print sent2
      #exit()
    return self.cosineDistance(embs[0], embs[1])
    
  #Embed 2 sentences and return [their euclidean distance, their cosine distance]
  def similarityEDCD(self, sent1, sent2):
    embs = self.embedSentences(sent1, sent2)
    return [self.euclideanDistance(embs[0], embs[1]), self.cosineDistance(embs[0], embs[1])]
  
  #Returns a list containing two embedded sentences (700 floats each)
  def embedSentences(self, sent1, sent2):
    print '%s, %s' % (sent1, sent2)
    sent1 = cleanSent2(sent1)
    sent2 = cleanSent2(sent2)
    print '%s, %s' % (sent1, sent2)
    return self.model.embed_sentences([sent1, sent2])
    
  def euclideanDistance(self, emb1, emb2):
    return spsp.distance.euclidean(emb1, emb2)
  
  def cosineDistance(self, emb1, emb2):
    return spsp.distance.cosine(emb1, emb2)
  
  # Tests if a vector has nothing but zeroes
  def nullVector(self, vec):
    for n in vec:
      if not n == 0:
        return False
    
    return True
  
    
    
    
