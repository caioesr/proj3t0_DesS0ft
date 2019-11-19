# IMPORTA BIBLIOTECAS
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import heapq
import os

# FUNCAO QUE RESUME
def get_summarized(article_text, formatted_article_text):
        # FILTRA AS stopwords
        # PALAVRAS 'IRRELEVANTES' (e.g. CONJUNÇÕES)
        nltk.download('punkt')
        nltk.download("stopwords")
        lista_sentencas = nltk.sent_tokenize(article_text)
        # ESTABELECE O IDIOMA DO TEXTO
        stopwords = nltk.corpus.stopwords.words('english')

        # DICIONÁRIO COM A FREQUENCIA DE APARIÇÕES DE UMA PALAVRA
        frequencia_palavras = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in frequencia_palavras.keys():
                    frequencia_palavras[word] = 1
                else:
                    frequencia_palavras[word] += 1
        frequencia_max = max(frequencia_palavras.values())

        # NORMALIZA A FREQUENCIA DAS PALAVRAS COM BASE NAQUELA QUE MAIS APARECE
        for word in frequencia_palavras.keys():
            frequencia_palavras[word] = (frequencia_palavras[word]/frequencia_max)

        # ATRIBUI NOTA À SENTENÇA BASEADO NA FREQUENCIA DAS PALAVRAS QUE A COMPÕE
        nota_frase = {}
        for sent in lista_sentencas:
            for word in nltk.word_tokenize(sent.lower()):
                if word in frequencia_palavras.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in nota_frase.keys():
                            nota_frase[sent] = frequencia_palavras[word]
                        else:
                            nota_frase[sent] += frequencia_palavras[word]

        # CRIA UM TEXTO COM AS TOP 10 SENTENÇAS
        top_sent = heapq.nlargest(10, nota_frase, key=nota_frase.get)
        summary = ' '.join(top_sent)
        return summary
