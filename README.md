# Mini-projeto 1 — Sistemas Distribuídos

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Repositório correspondente ao documento **[Miniprojeto1].docx**, com código e resultados da implementação.

**Status do Projeto:** Concluído ✔️

## 🚀 Conceitos Demonstrados

Este projeto foi dividido em 3 partes, cada uma focando em um conjunto de tecnologias e conceitos:

* **Parte 1:** 
    * Paralelismo com Threads para processamento de imagens.
* **Parte 2:**
    * Comunicação via Sockets (TCP).
    * Arquitetura Cliente-Servidor Multi-thread.
    * Arquitetura Peer-to-Peer (P2P) para um chat simples.
* **Parte 3:**
    * Criação de um sistema distribuído com múltiplos serviços.
    * Comunicação síncrona entre processos com **RPC (Remote Procedure Call)**.
    * Comunicação assíncrona e confiável com **Filas de Mensagens (RabbitMQ)**.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
    * `Pillow`: Para manipulação e processamento de imagens.
    * `pika`: Para a comunicação com o broker de mensagens RabbitMQ.
    * `socket`, `threading`, `xmlrpc`: Bibliotecas padrão do Python para redes, paralelismo e RPC.
* **Serviços:**
    * **Docker:** Para rodar o serviço do RabbitMQ de forma isolada e sem complicações.
    * **RabbitMQ:** Broker de mensagens utilizado na Parte 3.

## ⚙️ Pré-requisitos e Instalação

Antes de começar, garanta que você tem os seguintes softwares instalados:

1.  **Python 3.8+**
2.  **Git**
3.  **Docker Desktop** (ou Docker Engine no Linux)

Siga os passos abaixo para configurar o ambiente:

**1. Clone o Repositório:**
```bash
git clone <https://github.com/MikezinZ/projeto_sistemas_distribuidos.git>
cd projeto_sistemas_distribuidos
```

**2. Instale as Dependências do Python:**
Use o arquivo `requirements.txt` para instalar as bibliotecas necessárias.
```bash
pip install -r requirements.txt
```

**3. Inicie o Servidor RabbitMQ via Docker:**
Este comando irá baixar (apenas na primeira vez) e iniciar um container com o RabbitMQ.
```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
* Para verificar se o container está rodando, use `docker ps`.
* Você pode acessar a interface de gerenciamento do RabbitMQ em `http://localhost:15672` (login: `guest`, senha: `guest`).

## ▶️ Como Executar

Cada parte do projeto é executada de forma independente.

### Parte 1: Filtro de Imagens com Paralelismo

Este script aplica um filtro em duas imagens de forma paralela usando threads.

```bash
# Navegue até a pasta da Parte 1
cd parte1_paralelismo

# Execute o script
python processador_imagens.py
```
* As imagens processadas serão salvas na pasta `imagens_saida`.
* Os logs de execução, com os timestamps, serão salvos em `logs/processamento.log`.

### Parte 2: Modelos de Comunicação

#### 2.1: Cliente-Servidor

Você precisará de, no mínimo, dois terminais.

* **No Terminal 1 (Inicie o Servidor):**
    ```bash
    python parte2_comunicacao/cliente_servidor/servidor.py
    ```
* **No Terminal 2 (Execute o Cliente):**
    ```bash
    python parte2_comunicacao/cliente_servidor/cliente.py
    ```
    *Você pode abrir mais terminais e rodar o cliente várias vezes para ver o servidor lidando com múltiplas conexões.*

#### 2.2: Peer-to-Peer (P2P)

Você precisará de, no mínimo, dois terminais. Cada um rodará um "nó" em uma porta diferente.

* **No Terminal 1 (Inicie o Nó A):**
    ```bash
    python parte2_comunicacao/p2p/no_p2p.py 8080
    ```
* **No Terminal 2 (Inicie o Nó B):**
    ```bash
    python parte2_comunicacao/p2p/no_p2p.py 8081
    ```
* Para conectar os nós, digite no terminal do Nó B: `connect 127.0.0.1 8080`.
* Após a conexão, tudo que for digitado em um terminal aparecerá no outro.

### Parte 3: Sistema de Notificação Distribuída

Esta parte requer **três terminais**, e a ordem de execução é importante.

1.  **No Terminal 1 (Inicie o Serviço de Notificação):**
    *Este serviço precisa ser o primeiro a ser executado.*
    ```bash
    python parte3_notificacao/servico_notificacao.py
    ```

2.  **No Terminal 2 (Inicie o Servidor de Pedidos - A "Cozinha"):**
    ```bash
    python parte3_notificacao/servidor_pedidos.py
    ```

3.  **No Terminal 3 (Execute o Cliente para fazer um pedido):**
    ```bash
    python parte3_notificacao/cliente.py
    ```
* Observe os logs nos terminais 1 e 2 e a interface do RabbitMQ para ver o fluxo de mensagens acontecendo.

## 👥 Autores

* Miguel Melo
* Diogo Novaes
* Silvio Moreira

---
