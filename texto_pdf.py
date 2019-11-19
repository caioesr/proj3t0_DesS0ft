# IMPORTA BIBLIOTECAS
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

# FUNÇÃO PARA CONVERTER PDF
# EXTRAIDA DA PRÓPRIA DOCUMENTAÇÃO DO pdfminer
def converter_pdf(pdf_path):
    # VARIOS PASSOS NECESSÁRIOS PARA EXTRAIR O TEXTO
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()

    # CRIA ARQUIVO TXT E ESCREVE O CONTEÚDO NO MESMO
    i = 0
    name = ''
    for i in pdf_path:
        if i != '.':
            name += i
        else:
            break
    name += '.txt'
    with open(name, "w+", encoding="utf-8") as f:
        f.write(text)
