#gerenciar as threads para execução de tarefas em pararelo
#registrar os acontecimento em um arquivo de log

import threading
import time
from PIL import image, ImageFilter #Pillow para edição
import logging # Registro mais sofisticado e prático


# ------    Configuração do Log     ------
logging.basicConfig(level=logging.INFO, #Apenas mensagens informativas
                    format='%(asctime)s - %(threadName)s - %(message)s',
                    handlers=[
                              logging.FileHandler("logs/processamento.log"), #Envio para a pasta de logs.
                              logging.StreamHandler() #Para que as mensagens do log apareçam no terminal também.
                              ]
                    )


# Função Principal
def aplicar_filtro():
    """
    Função que será responsável por carregar uma imagem, aplicar um filtro e salvar
    """
    pass



# Execução Principal

if __name__ == "__main__":
    pass


# Miguel Melo - 23/09