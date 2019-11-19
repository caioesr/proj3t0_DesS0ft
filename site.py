# -*- coding: utf-8 -*-
# IMPORTANDO AS BIBLIOTECAS
import bs4 as bs
import urllib.request
import re
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import heapq
import os
from flask import Flask, render_template, request
from googletrans import Translator
from textsummarizer import generate_summary, read_article, sentence_similarity, build_similarity_matrix
from texto_pdf import converter_pdf
from resumidor import get_summarized
from translator import tradutor

# ISSO VAI PERMITIR RODAR O SITE
app = Flask(__name__)

# CRIA PÁGINA HOME DO SITE
@app.route('/')
def home():
    return render_template('home.html')

# ALGORITMO PARA RESUMIR TEXTOS DA WEB
@app.route('/summarized', methods=['POST'])
def summarized():
    # IMPORTAR TEXTO DA WEB
    target = request.form['url']
    scraped_data = urllib.request.urlopen(target)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    # FILTRAR SOMENTE AQUILO QUE FICA ENTRE A TAG <p>
    paragraphs = parsed_article.find_all('p')

    # MONTANDO TEXTO
    article_text = ""

    for p in paragraphs:
        article_text += p.text
    # LIMPANDO TEXTO
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    # CRIANDO ARQUIVO QUE PODE SER USADO PRA CONSULTA
    # OU PARA RESUMIR COM O ALGORITMO PARA FILES
    aux = target[::-1]
    name = ''
    for i in aux:
        if i == '/':
            break
        else:
            name += i
    name = name[::-1]
    name += '.txt'
    with open(name, "w+", encoding="utf-8") as f:
        f.write(article_text)

    # RESUMO
    return get_summarized(article_text, formatted_article_text)

# ALGORITMO PARA RESUMIR FILES
@app.route('/summarized_file', methods=['POST'])
def summarized_file():
    # PUXA O FILE DO HTML
    file_name = request.form['myfile']
    # TRATAMENTO PARA ARQUIVOS DO TIPO .pdf
    if file_name[len(file_name)-1] == 'f':
        new_file = converter_pdf(file_name)
        file_name = file_name[:len(file_name)-4] + '.txt'
    # LENDO E SALVANDO CONTEÚDO DO ARQUIVO
    with open(file_name, "r", encoding="utf-8") as file:
        filedata = file.readlines()
    article = filedata[0].split(". ")

    # CRIANDO TEXTO
    article_text = ''
    for p in article:
        article_text += (p + '. ')
    # FILTRANDO CARACTERES QUE NÃO SEJAM LETRA
    # IMPORTANTE POIS ALGUNS TEXTOS TEM NOTAÇÕES
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    # RESUMO
    # return get_summarized(article_text, formatted_article_text)
    texto = 'Algoritmo de ranqueamento:<br><br>'
    texto += get_summarized(article_text, formatted_article_text)
    texto += '<br><br>Algoritmo de vetores:<br><br>'
    # by: https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
    texto += generate_summary(file_name, 10)
    return texto

# FUNÇÃO PRA TRADUZIR ARQUIVOS
@app.route('/translated', methods=['POST'])
def translated():
    file_name = request.form['myfile3']
    tradutor(file_name)
    return 'Seu arquivo traduzido foi criado com sucesso!'

# INICIA O SITE
if __name__ == '__main__':
    app.run(debug=True)
