"""Utilitários de acesso ao banco Oracle utilizados pelo AgroSync.

Este módulo foi adaptado para permitir que o restante da aplicação seja
executado mesmo quando o ambiente não possui o pacote ``oracledb`` ou o
arquivo ``config.py`` com as credenciais.  Nas avaliações realizadas em sala
de aula nem sempre é possível instalar dependências externas, portanto é
importante que o programa funcione de forma degradada.
"""

from __future__ import annotations

from typing import Optional

try:  # pragma: no cover - apenas confirma a disponibilidade do driver
    import oracledb  # type: ignore
except Exception:  # noqa: BLE001 - qualquer erro ao importar deve ser tratado
    oracledb = None
    print(
        "\n[AVISO] O pacote 'oracledb' não está instalado. "
        "Operações com banco de dados serão ignoradas."
    )


def _carregar_credenciais() -> tuple[Optional[str], Optional[str]]:
    """Tenta importar as credenciais do arquivo ``config.py``.

    Retorna uma tupla ``(usuario, senha)``. Quando o arquivo não existe,
    valores ``None`` são retornados para que o restante do código decida como
    proceder.
    """

    try:
        from config import ORACLE_PASSWORD, ORACLE_USER  # type: ignore

        return ORACLE_USER, ORACLE_PASSWORD
    except ImportError:
        print(
            "\n[AVISO] Arquivo 'config.py' não encontrado. "
            "Crie o arquivo com as constantes ORACLE_USER e ORACLE_PASSWORD "
            "para habilitar o registro no banco de dados."
        )
    except Exception as exc:  # noqa: BLE001 - qualquer erro deve ser relatado
        print(
            "\n[AVISO] Não foi possível carregar as credenciais do banco: "
            f"{exc}"
        )

    return None, None


ORACLE_USER, ORACLE_PASSWORD = _carregar_credenciais()

# === Configurações do Banco de Dados ===

ORACLE_DSN = "oracle.fiap.com.br:1521/ORCL"

def _credenciais_validas() -> bool:
    """Confere se o usuário possui um par de credenciais configurado."""

    if ORACLE_USER is None or ORACLE_PASSWORD is None:
        return False

   if ORACLE_USER == "seu_rm_aqui" or ORACLE_PASSWORD == "sua_senha_aqui":
       print(
            "\nALERTA: As credenciais no arquivo 'config.py' parecem ser as de "
            "exemplo. Atualize o arquivo com seu usuário e senha reais para "
            "ativar a persistência no banco."
        )
        return False

    return True


def get_db_connection():
    """Retorna uma conexão com o banco Oracle, quando disponível."""

    if oracledb is None:
        return None

    if not _credenciais_validas():
        return None

    try:
              conexao = oracledb.connect(  # type: ignore[call-arg]
                  user=ORACLE_USER,
                  password=ORACLE_PASSWORD,
                  dsn=ORACLE_DSN,
              )
              return conexao
     except Exception as e:  # noqa: BLE001 - queremos mostrar o erro ao usuário
        print("\n[ERRO DE BANCO DE DADOS]: Não foi possível conectar ao Oracle.")
        print(e)
        print(
            "Verifique se as credenciais e a string de conexão (DSN) estão corretas."
        )
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
