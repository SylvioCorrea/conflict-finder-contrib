import os
from party_identification.extracting_parties_altered import extract_parties as ep_altered
from party_identification.extracting_parties import extract_parties as ep_original
from stanfordcorenlp import StanfordCoreNLP

def test():
  scnlp = StanfordCoreNLP('stanford-corenlp-full-2018-10-05')
  filepath = 'data/conflicting_contracts/Dani3-22_06_2015-23:46:24/chiron.mfg.2003.10.02.shtml'
  print "Processing contract " +filepath
  entities_alt, nicknames_alt = ep_altered(filepath, scnlp)
  print entities_alt
  scnlp.close()
  
def main():
  output = open('Identified_parties.txt', 'w')
  output.write('Original,StanfordCoreNLP\n')
  
  scnlp = StanfordCoreNLP('stanford-corenlp-full-2018-10-05')
  folders_path = 'data/conflicting_contracts/'
  folders_list = os.listdir(folders_path)

  for folder in folders_list:
    folder_files = os.listdir(folders_path + folder)
    file = folder_files[0]
    if 'new_norms' in file:
      file = folder_files[1]
    filepath = folders_path + folder + "/" + file
    print "Processing contract " +filepath
    entities_alt, nicknames_alt = ep_altered(filepath, scnlp)
    entities, nicknames = ep_original(filepath)
    output.write('Contract: '+filepath+'\n')
    output.write('Party names: '+entities[0]+';'+entities_alt[0]+'\nParty nicknames'+nicknames[0]+';'+nicknames_alt[0]+'\n')
    output.write('Party names: '+entities[1]+';'+entities_alt[1]+'\nParty nicknames'+nicknames[1]+';'+nicknames_alt[1]+'\n\n')
    
  scnlp.close()
  
if __name__=="__main__":
  main()
  #test()
