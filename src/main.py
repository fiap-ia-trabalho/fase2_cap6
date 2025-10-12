import os
import json
from datetime import datetime
from database import get_db_connection


colheitadeiras = []
caminhoes = []
talhoes = []

# === Funções de Cadastro ===

def cadastrar_colheitadeira():
    """Pede os dados de uma nova colheitadeira e a adiciona na lista."""
    print("\n--- Cadastro de Colheitadeira ---")
    identificacao = input("ID da Colheitadeira (ex: CH-01): ")
    
    # Validação da entrada da capacidade
    while True:
        try:
            capacidade = int(input("Capacidade de colheita (ton/hora): "))
            if capacidade > 0:
                break
            else:
                print("Por favor, digite um número positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    colheitadeiras.append({'id': identificacao, 'capacidade_colheita': capacidade})
    print(f"\nColheitadeira {identificacao} cadastrada com sucesso!")

def cadastrar_caminhao():
    """Pede os dados de um novo caminhão e o adiciona na lista."""
    print("\n--- Cadastro de Caminhão ---")
    identificacao = input("ID do Caminhão (ex: TR-01): ")
    
    # Validação da entrada da capacidade
    while True:
        try:
            capacidade = int(input("Capacidade de carga (toneladas): "))
            if capacidade > 0:
                break
            else:
                print("Por favor, digite um número positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            
    caminhoes.append({'id': identificacao, 'capacidade_carga': capacidade})
    print(f"\nCaminhão {identificacao} cadastrado com sucesso!")

def cadastrar_talhao():
    """Pede os dados de um novo talhão e o adiciona na lista."""
    print("\n--- Cadastro de Talhão ---")
    identificacao = input("ID do Talhão (ex: TALHAO-A): ")
    nome = input("Nome do Talhão (ex: Fazenda Boa Esperança): ")
    
    # Validação da entrada da distância
    while True:
        try:
            distancia = float(input("Distância até a usina (km): "))
            if distancia > 0:
                break
            else:
                print("Por favor, digite um número positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    talhoes.append({'id': identificacao, 'nome': nome, 'distancia_usina': distancia})
    print(f"\nTalhão {nome} cadastrado com sucesso!")

def menu_cadastro():
    """Exibe o menu de cadastro e gerencia a escolha do usuário."""
    while True:
        print("\n--- Menu de Cadastro ---")
        print("[1] Cadastrar Colheitadeira")
        print("[2] Cadastrar Caminhão")
        print("[3] Cadastrar Talhão")
        print("[4] Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastrar_colheitadeira()
        elif escolha == '2':
            cadastrar_caminhao()
        elif escolha == '3':
            cadastrar_talhao()
        elif escolha == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

# === Função de Simulação ===

def simular_operacao():
    """Realiza a simulação logística e exibe a recomendação."""
    print("\n--- Nova Simulação de Colheita ---")

    if not talhoes or not colheitadeiras or not caminhoes:
        print("\nAVISO: É necessário cadastrar pelo menos um Talhão, uma Colheitadeira e um Caminhão antes de simular.")
        return

    # Escolha do talhão
    print("Talhões disponíveis:")
    for i, talhao in enumerate(talhoes):
        print(f"[{i+1}] {talhao['nome']}")
    
    while True:
        try:
            escolha_talhao = int(input("Escolha o talhão para a simulação: ")) - 1
            if 0 <= escolha_talhao < len(talhoes):
                talhao_selecionado = talhoes[escolha_talhao]
                break
            else:
                print("Opção inválida.")
        except ValueError:
            print("Entrada inválida. Digite o número correspondente.")
    
    # Entrada de parâmetros da simulação com validação
    while True:
        try:
            num_colheitadeiras = int(input(f"Quantas colheitadeiras estão ativas no talhão '{talhao_selecionado['nome']}'? "))
            if num_colheitadeiras > 0: break
            else: print("Digite um número positivo.")
        except ValueError: print("Entrada inválida.")
            
    while True:
        try:
            velocidade_media = float(input("Qual a velocidade média dos caminhões (km/h)? "))
            if velocidade_media > 0: break
            else: print("Digite um número positivo.")
        except ValueError: print("Entrada inválida.")
    
    tempo_carga_descarga = 20 # Tempo fixo médio de carga e descarga em minutos

    # === Cálculos ===
    distancia = talhao_selecionado['distancia_usina']
    tempo_ida_volta_horas = (distancia * 2) / velocidade_media
    tempo_ida_volta_minutos = tempo_ida_volta_horas * 60
    
    tempo_ciclo_total_minutos = tempo_ida_volta_minutos + tempo_carga_descarga

    # Usando a capacidade média das colheitadeiras e caminhões cadastrados
    capacidade_media_colheita_th = sum(c['capacidade_colheita'] for c in colheitadeiras) / len(colheitadeiras)
    capacidade_media_caminhao_ton = sum(c['capacidade_carga'] for c in caminhoes) / len(caminhoes)

    producao_total_th = capacidade_media_colheita_th * num_colheitadeiras
    caminhoes_por_hora = producao_total_th / capacidade_media_caminhao_ton
    
    if caminhoes_por_hora == 0:
        print("Cálculo resultou em zero caminhões por hora, verifique os dados.")
        return

    intervalo_entre_caminhoes_min = 60 / caminhoes_por_hora
    
    caminhoes_recomendados = round(tempo_ciclo_total_minutos / intervalo_entre_caminhoes_min)
    if caminhoes_recomendados == 0:
        caminhoes_recomendados = 1

    # Exibição dos resultados
    print("\n-----------------------------------------")
    print("          PLANO DE OPERAÇÃO")
    print("-----------------------------------------")
    print(f"Talhão:             {talhao_selecionado['nome']}")
    print(f"Distância à Usina:  {distancia} km")
    print(f"Colheitadeiras:     {num_colheitadeiras}")
    print("-----------------------------------------")
    print("CÁLCULO LOGÍSTICO:")
    print(f"> Tempo de Ciclo por Caminhão: {tempo_ciclo_total_minutos:.2f} minutos")
    print(f"> Necessidade da Colheita:   1 caminhão a cada {intervalo_entre_caminhoes_min:.2f} minutos")
    print("-----------------------------------------")
    print("RECOMENDAÇÃO:")
    print(f"Para uma operação contínua, aloque [{caminhoes_recomendados}] caminhões para esta frente.")
    print("-----------------------------------------")

    # Salvar o plano
    salvar = input("\nDeseja salvar este plano? [S/N]: ").strip().upper()
    if salvar == 'S':
        dados_plano = {
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "talhao_selecionado": talhao_selecionado,
            "parametros_simulacao": {
                "num_colheitadeiras": num_colheitadeiras,
                "velocidade_media_caminhao_kmh": velocidade_media
            },
            "resultado": {
                "tempo_ciclo_minutos": round(tempo_ciclo_total_minutos, 2),
                "caminhoes_recomendados": caminhoes_recomendados
            }
        }
        salvar_relatorio_json(dados_plano)
        salvar_no_banco(dados_plano)

# --- FUNÇÕES DE ARQUIVO E BANCO DE DADOS ---

def salvar_relatorio_json(dados):
    """Salva o dicionário de dados em um arquivo JSON."""
    if not os.path.exists('relatorios'):
        os.makedirs('relatorios')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorios/plano_{timestamp}.json"

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    
    print(f"Plano salvo com sucesso em '{nome_arquivo}'")

def salvar_no_banco(dados):
    """Salva um resumo do plano no banco de dados Oracle."""
    conexao = get_db_connection()
    if not conexao:
        print("Não foi possível salvar no banco de dados devido a falha na conexão.")
        return

    cursor = None
    try:
        cursor = conexao.cursor()
        
        # SQL para inserção dos dados
        sql = """
            INSERT INTO HISTORICO_OPERACOES (
                ID_OPERACAO, DATA_OPERACAO, NOME_TALHAO, DISTANCIA_KM, 
                NUM_COLHEITADEIRAS, NUM_CAMINHOES_RECOMENDADOS, TEMPO_CICLO_MIN
            ) VALUES (
                SEQ_HISTORICO_OPERACOES.NEXTVAL, :data, :talhao, :distancia, 
                :num_colheitadeiras, :num_caminhoes, :tempo_ciclo
            )
        """
        
        # Executa o comando
        cursor.execute(sql, 
            data=datetime.strptime(dados['data_hora'], "%Y-%m-%d %H:%M:%S"),
            talhao=dados['talhao_selecionado']['nome'],
            distancia=dados['talhao_selecionado']['distancia_usina'],
            num_colheitadeiras=dados['parametros_simulacao']['num_colheitadeiras'],
            num_caminhoes=dados['resultado']['caminhoes_recomendados'],
            tempo_ciclo=dados['resultado']['tempo_ciclo_minutos']
        )
        
        conexao.commit()
        print("Histórico salvo com sucesso no banco de dados.")

    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def consultar_historico():
    """Consulta e exibe o histórico de operações do banco de dados."""
    print("\n--- Histórico de Simulações (Banco de Dados) ---")
    conexao = get_db_connection()
    if not conexao:
        print("Não foi possível consultar o histórico devido a falha na conexão.")
        return

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT ID_OPERACAO, DATA_OPERACAO, NOME_TALHAO, NUM_CAMINHOES_RECOMENDADOS FROM HISTORICO_OPERACOES ORDER BY DATA_OPERACAO DESC")
        
        # Cabeçalho da tabela
        print("\n{:<5} {:<20} {:<30} {:<10}".format("ID", "DATA", "TALHÃO", "CAMINHÕES"))
        print("-" * 70)

        # Exibe os resultados
        for row in cursor:
            # Formata a data para exibição
            data_formatada = row[1].strftime("%d/%m/%Y %H:%M")
            print("{:<5} {:<20} {:<30} {:<10}".format(row[0], data_formatada, row[2], row[3]))
        
        print("-" * 70)

    except Exception as e:
        print(f"Erro ao consultar o histórico: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def criar_tabela_se_nao_existir():
    """Verifica se a tabela e a sequence existem, e as cria caso contrário."""
    conexao = get_db_connection()
    if not conexao:
        print("Não foi possível inicializar o banco de dados. Verifique a conexão.")
        return

    cursor = None
    try:
        cursor = conexao.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("SELECT table_name FROM user_tables WHERE table_name = 'HISTORICO_OPERACOES'")
        if cursor.fetchone() is None:
            print("Tabela 'HISTORICO_OPERACOES' não encontrada. Criando...")
            cursor.execute("""
                CREATE TABLE HISTORICO_OPERACOES (
                    ID_OPERACAO NUMBER PRIMARY KEY,
                    DATA_OPERACAO DATE NOT NULL,
                    NOME_TALHAO VARCHAR2(100) NOT NULL,
                    DISTANCIA_KM NUMBER(5, 2) NOT NULL,
                    NUM_COLHEITADEIRAS NUMBER NOT NULL,
                    NUM_CAMINHOES_RECOMENDADOS NUMBER NOT NULL,
                    TEMPO_CICLO_MIN NUMBER(6, 2)
                )
            """)
            print("Tabela criada com sucesso.")
        
        
        cursor.execute("SELECT sequence_name FROM user_sequences WHERE sequence_name = 'SEQ_HISTORICO_OPERACOES'")
        if cursor.fetchone() is None:
            print("Sequence 'SEQ_HISTORICO_OPERACOES' não encontrada. Criando...")
            cursor.execute("CREATE SEQUENCE SEQ_HISTORICO_OPERACOES START WITH 1 INCREMENT BY 1")
            print("Sequence criada com sucesso.")

    except Exception as e:
        print(f"Erro durante a inicialização do banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

# === Função Principal ===

def main():
    """Função principal que executa o menu e o loop do programa."""
    
    
    criar_tabela_se_nao_existir() # Garante que a infraestrutura do banco de dados está pronta

    while True:
        print("\n=========================================")
        print("      AGROSYNC - Otimizador Logístico")
        print("=========================================")
        print("[1] Cadastrar Ativos")
        print("[2] Iniciar Nova Simulação de Colheita")
        print("[3] Consultar Histórico de Simulações")
        print("[4] Sair")
        print("=========================================")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_cadastro()
        elif opcao == '2':
            simular_operacao()
        elif opcao == '3':
            consultar_historico()
        elif opcao == '4':
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

# === Entrada no Programa ===

if __name__ == "__main__":
    main()

