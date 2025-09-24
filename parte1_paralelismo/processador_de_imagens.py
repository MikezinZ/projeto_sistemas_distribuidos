#gerenciar as threads para execução de tarefas em pararelo
#registrar os acontecimento em um arquivo de log

import threading
import time
from PIL import Image, ImageFilter #Pillow para edição
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

def aplicar_filtro(entrada, saida):
    """
    Função que será responsável por carregar uma imagem, aplicar um filtro e salvar
    """
    nome_thread = threading.current_thread().name
    logging.info(f"Iniciando o processamento da imagem '{entrada}'.")

    try:

        inicio_tempo = time.time()
        with Image.open(entrada) as img:

            img_filtrada = img.filter(ImageFilter.EDGE_ENHANCE)

            img_filtrada.save(saida)

        fim_tempo = time.time()
        tempo_total = fim_tempo - inicio_tempo

        logging.info(f"Imagem '{entrada}' salva com sucesso. Tempo de execução: {tempo_total:.4f} segundos.")

    except FileNotFoundError:

        logging.error(f"O arquivo '{entrada}' não foi encontrado.")

    except Exception as e:

        logging.error(f"Ocorreu um erro ao processar a imagem '{entrada}': {e}")

# Execução Principal

if __name__ == "__main__":
    logging.info("Iniciando o processador de imagens paralelo!")
     
    imagens_para_processar = [
        ("imagens_entrada/detetive_pikachu.png", "imagens_saida/detetive_pikachu_enhance.png"),
        ("imagens_entrada/corra.png", "imagens_saida/corra_enhance.png")
    ]

    threads = []

    for entrada, saida in imagens_para_processar:
        thread = threading.Thread(target=aplicar_filtro, args=(entrada, saida))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logging.info("Todos os processamentos foram finalizados")