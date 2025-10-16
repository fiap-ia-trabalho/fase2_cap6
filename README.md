<div align="center">
<h1>FIAP - Faculdade de Informática e Administração Paulista</h1>
<img src="./assets/logo-fiap.png" alt="Logo da FIAP" width="400"/>
</div>


# Projeto AgroSync: Otimizador de Colheita de Cana-de-Açúcar


## Projeto acadêmico para a disciplina de Python da FIAP, focado em resolver um problema de logística no agronegócio da cana-de-Açúcar.


## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/cauanotto">CAUAN_OTTO_RODRIGUES_SOUSA_RM567940</a>
- <a href="https://www.linkedin.com/in/fernando-gurgel-75aa8369">FERNANDO_ARAUJO_GURGEL_RM567606</a>
- <a href="https://www.linkedin.com/in/iraci-souza-bab42034">IRACI_MONTEIRO_SOUZA_RM567544</a> 
- <a href="https://www.linkedin.com/in/malu-rodrigues-bb756b271">MARIA_LUISA_RODRIGUES_NASCIMENTO_RM567659</a> 
- <a href="https://www.linkedin.com/in/rafaela-torres222">RAFAELA_TORRES_MARTINS_RM567735</a>

## 👩‍🏫 Professores:
**Tutor(a):** [ANA CRISTINA DOS SANTOS](https://www.linkedin.com/company/inova-fusca)  
**Coordenador(a):** [ANDRÉ GODOI](https://www.linkedin.com/in/andregodoichiovato)

## 📜 Descrição
O agronegócio da cana-de-açúcar no Brasil enfrenta perdas significativas durante a colheita mecanizada. Um dos principais problemas é a falta de sincronia entre as colheitadeiras e os caminhões de transporte.


Este projeto visa resolver essa "dor" através de um software simples que calcula e sugere o número ideal de caminhões para uma frente de colheita, minimizando o tempo ocioso das máquinas e reduzindo perdas operacionais.


### 🛠️ Tecnologias Utilizadas
+ Linguagem: Python 3


+ Banco de Dados: Oracle


+ Biblioteca Python: oracledb

## Estrutura de Pastas
fase_2_cap_6_python_e_alem/    
│
├── .git/      (oculto)              
│
├── assets/                   
│   └── logo-fiap.png         
│
├── relatorios/             
│   ├── plano_20251015...json 
│   └── resumo_20251015...txt  
│
├── src/                      
│   ├── _init_.py           
│   ├── app.py              
│   ├── config.py      (ignorado)       
│   └── database.py         
│
├── .gitignore                
├── README.md                 
└── requirements.txt


## 🔧 Como executar o código
Para rodar este projeto, siga os passos abaixo.


*1. Clone o repositório:*


``` python
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```


*2. Instale as dependências:*
O projeto precisa da biblioteca do Oracle para Python. Use o ficheiro requirements.txt para instalar.


```python
pip install -r requirements.txt
```


*3. Configure o Banco de Dados:*
Crie a tabela HISTORICO_OPERACOES no seu banco de dados Oracle usando o script abaixo:


```SQL
CREATE TABLE HISTORICO_OPERACOES (
    ID_OPERACAO NUMBER PRIMARY KEY,
    DATA_OPERACAO DATE NOT NULL,
    NOME_TALHAO VARCHAR2(100) NOT NULL,
    DISTANCIA_KM NUMBER(5, 2) NOT NULL,
    NUM_COLHEITADEIRAS NUMBER NOT NULL,
    NUM_CAMINHOES_RECOMENDADOS NUMBER NOT NULL,
    TEMPO_CICLO_MIN NUMBER(6, 2)
);

CREATE SEQUENCE SEQ_HISTORICO_OPERACOES START WITH 1 INCREMENT BY 1;
````


*4. Crie o arquivo de configuração:*
Na pasta 'src', crie um arquivo chamado 'config.py'. Este arquivo não será enviado para o GitHub e conterá suas credenciais de acesso.


config.py:
```python
ORACLE_USER = "seu_rm_aqui"
ORACLE_PASSWORD = "sua_senha_aqui"
```


*5. Execute o programa:*

No terminal, a partir da pasta principal do projeto, execute o seguinte comando:

```python
python -m src.app
```
## 📋 Licença
MODELO GIT FIAP por Fiap está licenciado sobre Attribution 4.0 International.





