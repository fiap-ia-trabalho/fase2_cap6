import oracledb
import sys

# === Importação das Credenciais ===
try:
    from .config import ORACLE_USER, ORACLE_PASSWORD
except ImportError:
    print("\nERRO: Arquivo 'config.py' não encontrado.")
    print("Por favor, crie o arquivo 'config.py' com suas credenciais ORACLE_USER e ORACLE_PASSWORD.")
    sys.exit() 

# === Configurações do Banco de Dados ===

ORACLE_DSN = "oracle.fiap.com.br:1521/ORCL"

def get_db_connection():
    """
    Tenta estabelecer e retornar uma conexão com o banco de dados Oracle.
    Retorna None se a conexão falhar.
    """
    if ORACLE_USER == "seu_rm_aqui" or ORACLE_PASSWORD == "sua_senha_aqui":
        print("\nALERTA: Suas credenciais no arquivo 'config.py' parecem ser as padrão.")
        print("Por favor, edite o arquivo 'config.py' com seu usuário e senha reais.")
        return None
        
    try:
        conexao = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        return conexao
    except oracledb.Error as e:
        print(f"\n[ERRO DE BANCO DE DADOS]: Não foi possível conectar ao Oracle.")
        error_obj, = e.args
        print(f"Código do Erro: {error_obj.code}")
        print(f"Mensagem: {error_obj.message}")
        print("Verifique se as credenciais e a string de conexão (DSN) estão corretas.")
        return None

# === Bloco de Teste ===

if __name__ == '__main__':
    print("Testando a conexão com o banco de dados...")
    conn = get_db_connection()
    if conn:
        print("Conexão bem-sucedida!")
        print("Versão do Oracle Database:", conn.version)
        conn.close()
        print("Conexão fechada.")
    else:
        print("\nFalha na conexão. Verifique o arquivo config.py e suas credenciais.")

