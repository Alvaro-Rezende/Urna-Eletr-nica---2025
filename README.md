# 🗳️ Urna Eletrônica Simplificada

Projeto desenvolvido em Python para a disciplina de Algoritmos e Lógica de Programação. O sistema simula o funcionamento de uma urna eletrônica brasileira (modelo 2020), permitindo o cadastro de eleitores, candidatos e a realização de votos com persistência de dados.

## 👨‍💻 Autores
* **Álvaro Rezende**
* **Kevin Almeida**
* **João Luiz Rezende**

---

## 🚀 Funcionalidades

O sistema atende a todos os requisitos propostos, incluindo o desafio extra:

* **Leitura de Dados:** Carrega candidatos e eleitores a partir de arquivos de texto (`.txt`).
* **Processo de Votação Completo:**
    * Deputado Federal, Deputado Estadual, Senador, Governador e Presidente.
    * Votos em Branco e Nulo.
* **Regras de Negócio:**
    * Validação de Estado: Eleitores só podem votar em candidatos da sua UF (exceto para Presidente).
    * **Controle de Voto Único (Desafio Extra):** O sistema impede que o mesmo Título de Eleitor vote mais de uma vez.
* **Persistência:** Os votos são salvos sequencialmente em arquivo binário (`votos.bin`) utilizando a biblioteca `pickle`.
* **Apuração:** Leitura do arquivo binário e geração de um Boletim de Urna (`boletim.txt`) com a contagem e porcentagem dos votos.

---

## 📂 Estrutura de Arquivos

* `urna.py`: Código fonte principal.
* `candidatos.txt`: Base de dados dos candidatos (Formato: Nome,Numero,Partido,UF,Cargo).
* `eleitores.txt`: Base de dados dos eleitores (Formato: Nome,RG,Titulo,Cidade,UF).
* `votos.bin`: Arquivo gerado automaticamente contendo os votos criptografados/binários.
* `ja_votaram.txt`: Arquivo de controle para impedir votos duplicados.
* `boletim.txt`: Relatório final gerado após a apuração.

```bash
python urna.py
