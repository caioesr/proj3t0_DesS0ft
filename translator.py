# IMPORTANDO AS BIBLIOTECAS
from googletrans import Translator

# CRIA FUNÇÃO
def tradutor(file_name):
    translator = Translator()

    # CRIA TEXTO PARA SER TRADUZIDO
    with open(file_name,'r', encoding="utf-8") as file:
        filedata = file.readlines()
    article = filedata[0].split(". ")

    article_text = ''
    for p in article:
        article_text += (p + '. ')

    # TRADUZ
    traduzido = translator.translate(article_text).text

    # SALVA EM UM ARQUIVO
    with open('traduzido.txt','w+',encoding='utf-8') as file:
        file.write(traduzido)
