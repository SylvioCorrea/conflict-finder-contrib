# Potential Conflict Finder -- Contribuição

Repositório de contribuição sobre o trabalho original Norm Conflict Identification in Contracts.

[Repositório da pesquisa original](https://github.com/JoaoPauloAires/potential-conflict-identifier)

O artigo que descreve esta contribuição pode ser lido no pdf Conflitos_em_Contratos_Contrib.pdf constante neste repositório

## Instalações necessárias

Recomenda-se o uso de uma máquina com pelo menos 5 GB de RAM e sistema operacional Linux.

É necessária a instalação de Python 2 e Java.

É necessário o download de algumas bibliotecas e modelos treinados entes da execução. Há vários downloads que podem ser feitos usando o pip do Python. Se Python 3 for a versão padrão da sua máquina, um comando ```pip intall``` deve ser substituido por ```py2 -m pip install```

Instale a biblioteca NLTK:

 - pip install nltk

Use o interpretador interativo do python para baixar bibliotecas adicionais do nltk:

 - ```python```
 - ```>>>import nltk```
 - ```>>>nltk.download('punkt')```
 - ```>>>nltk.download(‘averaged_perceptron_tagger’)```
 - ```>>>nltk.download(‘wordnet’)```

Instale também:

 - [sent2vec](https://github.com/epfml/sent2vec) (siga as instruções do repositório)
 - StanfordCoreNLP: baixe a biblioteca [aqui](https://stanfordnlp.github.io/CoreNLP/#download), descompactando o arquivo **dentro da pasta deste repositório**.
 - Wrapper de python para esta StanfordCoreNLP: ```pip install stanfordcorenlp```

Depois baixe o modelo toronto books unigrams de 2 GB da [área de modelos pré treinados](https://github.com/epfml/sent2vec#downloading-pre-trained-models) do repositório do sent2vec. Coloque este modelo **dentro da pasta deste repositório**

## Executando testes

O script test_conflict_finder_altered.py executa o conflict-finder com a nova função de sentence embedding e cálculo de similaridade baseado em distância euclidiana. Este mesmo script pode ser chamado com um argumento cosine para executar cálculo de similaridade baseado em distância de cosseno. Resultados são impressos em thr_tr_and_fl_positives.csv.

O script test_conflict_finder_altered_new_identification.py usa a nova função de reconhecimento das partes além do sentence embedding e de cálculo de similaridade baseado em distância euclidiana. Resultados são impressos em thr_tr_and_fl_positives(new_parties).csv

O script party_extractor_test.py testa a nova função de reconhecimento das partes e imprime os resultados em Identified_parties.txt
