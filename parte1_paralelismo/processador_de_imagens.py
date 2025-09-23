#gerenciar as threads para execução de tarefas em pararelo
#registrar os acontecimento em um arquivo de log

import threading
import time
from PIL import Image, ImageFilter #Pillow para edição
import logging # Registro mais sofisticado e prático
import os

os.makedirs("logs", exist_ok=True)

# ------    Configuração do Log     ------

logging.basicConfig(level=logging.INFO, #Apenas mensagens informativas
                    format='%(asctime)s - %(threadName)s - %(message)s',
                    handlers=[
                              logging.FileHandler("logs/processamento.log"), #Envio para a pasta de logs.
                              logging.StreamHandler() #Para que as mensagens do log apareçam no terminal também.
                              ]
                    )


# Função Principal

def aplicar_filtro(entrada, saida):
    """
    Função que será responsável por carregar uma imagem, aplicar um filtro e salvar
    """
    
    img = Image.open (entrada)

    img_filtrada = img.filter(ImageFilter.EDGE_ENHANCE)

    img_filtrada.save(saida)

    print(f"Filtro aplicado: {entrada} -> {saida}")

# Execução Principal

if __name__ == "__main__":
     
    aplicar_filtro("imagens_entrada/detetive_pikachu.png", "imagens_saida/detetive_pikachu_enhance.png")

    aplicar_filtro("imagens_entrada/corra.png", "imagens_saida/corra_enhance.png")
