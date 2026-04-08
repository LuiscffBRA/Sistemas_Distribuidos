# 🌐 Sistemas Distribuídos - UFRN / EAJ

Este repositório contém as implementações práticas dos **Trabalhos 2 e 3** da disciplina de Sistemas Distribuídos (Curso de Análise e Desenvolvimento de Sistemas - UFRN/EAJ), ministrada pelo Professor Taniro Rodrigues.

O foco principal destes projetos é a aplicação prática de comunicação entre processos utilizando a abstração de *Sockets* (TCP e UDP), explorando técnicas de sincronização de estado, mitigação de perda de pacotes e análise de desempenho de rede.

---

## 🎮 Trabalho 2: Ping Pong Multiplayer (Sincronização e Predição de Estado)

Desenvolvimento de um jogo multiplayer 2D (Ping Pong) rodando em janelas independentes, focado na diferença de experiência do usuário ao utilizar protocolos orientados e não-orientados a conexão.

### 🛠️ Conceitos Aplicados:
* **Modo TCP:** Implementa um túnel seguro e confiável. Garante 100% da entrega na ordem correta. No entanto, em caso de oscilação na rede, o bloqueio do protocolo (esperando confirmação) gera **Input Delay**, travando o jogo.
* **Modo UDP:** Focado em velocidade e tempo real (padrão da indústria de games). Arremessa datagramas sem garantia de entrega.
* **Técnica de Extrapolação (Predição de Estado):** Para mitigar o *Jitter* (teletransporte) causado pela perda de pacotes no UDP, o cliente simula um ambiente de internet instável (20% de perda induzida) e utiliza a matemática para prever o futuro. Ao perder um pacote, o jogo continua desenhando a trajetória da bola baseado em sua última velocidade conhecida, garantindo uma movimentação visualmente suave.

### 🚀 Como executar (Trabalho 2)
1. Instale a biblioteca gráfica: `pip install pygame`
2. Navegue até a pasta do Trabalho 2.
3. **Para testar o TCP:**
   * Abra um terminal e inicie o juiz: `python servidor.py`
   * Abra dois terminais independentes e inicie os clientes: `python jogo.py`
4. **Para testar o UDP:**
   * Abra um terminal e inicie o servidor caótico: `python servidor_udp.py`
   * Abra dois terminais e inicie os clientes: `python jogo_udp.py`

---

## 📊 Trabalho 3: Análise de Desempenho (TCP vs UDP)

Um ambiente de teste de estresse massivo de rede para mensurar a taxa de transmissão (Throughput em Mbps), perda de pacotes e ordem de entrega enviando rajadas de pacotes variando de **1KB a 60KB**.

### 🛠️ Conceitos Aplicados:
* **Métricas Coletadas:** Tempo de transmissão, Throughput (Mbps), Porcentagem de Perda e Pacotes fora de ordem (utilizando cabeçalhos customizados com números de sequência no UDP).
* **Análise de *Overhead* em Loopback (Localhost):** O experimento provou na prática que, em ambientes locais sem gargalos de hardware de rede (roteadores), o TCP supera o UDP de forma colossal. 
* **Justificativa Técnica:** O fluxo contínuo e o controle de fluxo do TCP permitem que o SO otimize a transferência de dados na RAM. Já o UDP, orientado a datagramas isolados, sofre com o gargalo de processamento (*overhead* de chamadas de sistema) ao ter que processar o cabeçalho de milhares de pacotes individualmente, impedindo-o de alcançar as taxas extremas do TCP no *localhost*.

### 🚀 Como executar (Trabalho 3)
1. Navegue até a pasta do Trabalho 3.
2. **Para rodar a bateria TCP:**
   * Inicie o servidor: `python servidor_tcp.py`
   * Inicie o metralhador de pacotes: `python cliente_tcp.py`
3. **Para rodar a bateria UDP:**
   * Inicie o servidor: `python servidor_udp.py`
   * Inicie o cliente: `python cliente_udp.py`

---

## 👨‍💻 Autor

**Luis Carlos Firmino Façanha** *Estudante de Análise e Desenvolvimento de Sistemas - UFRN / EAJ*
