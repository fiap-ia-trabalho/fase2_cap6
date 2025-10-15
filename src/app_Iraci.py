from __future__ import annotations
import json, os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Protocol, TypedDict

# -----------------------------
# 🌾 Domínio & Tabela de Memória
# -----------------------------
CULTURAS_SUPORTADAS: tuple[str, ...] = ("cana-de-açúcar",)

class Simulacao(TypedDict):
    id: int
    data_iso: str
    cultura: str
    n_colheitadeiras: int
    distancia_km: float
    velocidade_kmh: float
    tempo_descarga_min: float
    tempo_ciclo_min: float
    caminhoes_ideais: int

SIMULACOES: List[Simulacao] = []

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
ARQ_JSON = os.path.join(DATA_DIR, "simulacoes.json")
ARQ_TXT  = os.path.join(DATA_DIR, "relatorio.txt")
ARQ_LOG  = os.path.join(DATA_DIR, "app.log")

# -----------------------------
# 🏛️ Repositórios (opcional)
# -----------------------------
class Repository(Protocol):
    def salvar(self, s: Simulacao) -> None: ...
    def listar(self) -> List[Simulacao]: ...
    def limpar(self) -> None: ...

class MockRepository:
    def __init__(self, mem: List[Simulacao]) -> None:
        self._mem = mem
    def salvar(self, s: Simulacao) -> None:
        self._mem.append(s)
    def listar(self) -> List[Simulacao]:
        return list(self._mem)
    def limpar(self) -> None:
        self._mem.clear()

@dataclass
class OracleConfig:
    dsn: str
    user: str
    password: str

class OracleRepository:
    """Stub — implemente se for usar Oracle de verdade."""
    def __init__(self, cfg: OracleConfig) -> None:
        self.cfg = cfg
        try:
            import oracledb  # noqa
            self._ok = True
        except Exception:
            self._ok = False
    def salvar(self, s: Simulacao) -> None:
        if not self._ok:
            raise RuntimeError("oracledb não disponível. Use MockRepository ou instale dependências.")
        # TODO: INSERT em HISTORICO_OPERACOES
        # with oracledb.connect(user=self.cfg.user, password=self.cfg.password, dsn=self.cfg.dsn) as conn: ...
    def listar(self) -> List[Simulacao]:
        if not self._ok:
            raise RuntimeError("oracledb não disponível.")
        # TODO: SELECT e mapear para List[Simulacao]
        return []
    def limpar(self) -> None:
        if not self._ok:
            raise RuntimeError("oracledb não disponível.")
        # TODO: TRUNCATE/DELETE

# -----------------------------
# 🧩 Regras de negócio (funções)
# -----------------------------
def proximo_id(mem: List[Simulacao]) -> int:
    return (max((x["id"] for x in mem), default=0) + 1) if mem else 1

def calcular_tempo_ciclo(distancia_km: float, velocidade_kmh: float, tempo_descarga_min: float, tempo_carreg_min: float) -> float:
    """Tempo de ciclo do caminhão (min): ida + descarga + volta + carregamento."""
    if distancia_km <= 0 or velocidade_kmh <= 0 or tempo_descarga_min <= 0 or tempo_carreg_min <= 0:
        raise ValueError("Parâmetros do ciclo devem ser > 0.")
    tempo_ida_min = (distancia_km / velocidade_kmh) * 60.0
    tempo_volta_min = tempo_ida_min
    return tempo_ida_min + tempo_descarga_min + tempo_volta_min + tempo_carreg_min

def calcular_caminhoes_ideais(n_colheitadeiras: int, tempo_ciclo_min: float, tempo_carreg_min: float) -> int:
    """Heurística: Caminhões Ideais = (Tempo Ciclo / Tempo Carregamento) * Nº Colheitadeiras"""
    if n_colheitadeiras <= 0 or tempo_ciclo_min <= 0 or tempo_carreg_min <= 0:
        raise ValueError("Parâmetros devem ser > 0.")
    from math import ceil
    return int(ceil((tempo_ciclo_min / tempo_carreg_min) * n_colheitadeiras))

def adicionar_simulacao(repo: Repository, cultura: str, n_colheitadeiras: int, distancia_km: float, velocidade_kmh: float, tempo_descarga_min: float, tempo_carreg_min: float) -> Simulacao:
    cultura_norm = cultura.strip().lower()
    if cultura_norm not in (c.lower() for c in CULTURAS_SUPORTADAS):
        raise ValueError(f"Cultura inválida: {cultura}. Suportadas: {', '.join(CULTURAS_SUPORTADAS)}")
    tempo_ciclo = calcular_tempo_ciclo(distancia_km, velocidade_kmh, tempo_descarga_min, tempo_carreg_min)
    n_caminhoes = calcular_caminhoes_ideais(n_colheitadeiras, tempo_ciclo, tempo_carreg_min)
    s: Simulacao = {
        "id": proximo_id(SIMULACOES),
        "data_iso": datetime.now().isoformat(timespec="seconds"),
        "cultura": cultura_norm,
        "n_colheitadeiras": int(n_colheitadeiras),
        "distancia_km": float(distancia_km),
        "velocidade_kmh": float(velocidade_kmh),
        "tempo_descarga_min": float(tempo_descarga_min),
        "tempo_ciclo_min": float(tempo_ciclo),
        "caminhoes_ideais": int(n_caminhoes),
    }
    repo.salvar(s)
    log_texto(f"Simulação #{s['id']} | {s['cultura']} | colh:{s['n_colheitadeiras']} | dist:{s['distancia_km']}km | vel:{s['velocidade_kmh']}km/h | caminhões:{s['caminhoes_ideais']}")
    return s

# -----------------------------
# 🗃️ Arquivos (JSON/TXT) + Log
# -----------------------------
def salvar_json(mem: List[Simulacao], caminho: str = ARQ_JSON) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)
    log_texto(f"JSON salvo: {caminho}")

def carregar_json(destino: List[Simulacao], caminho: str = ARQ_JSON) -> None:
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    destino.clear()
    for d in dados:
        destino.append(Simulacao(
            id=int(d["id"]),
            data_iso=str(d["data_iso"]),
            cultura=str(d["cultura"]),
            n_colheitadeiras=int(d["n_colheitadeiras"]),
            distancia_km=float(d["distancia_km"]),
            velocidade_kmh=float(d["velocidade_kmh"]),
            tempo_descarga_min=float(d["tempo_descarga_min"]),
            tempo_ciclo_min=float(d["tempo_ciclo_min"]),
            caminhoes_ideais=int(d.get("caminhoes_ideais", 0)),
        ))
    log_texto(f"JSON carregado: {caminho} ({len(destino)} simulação(ões))")

def gerar_relatorio_txt(vs: List[Simulacao], caminho: str = ARQ_TXT) -> None:
    linhas: List[str] = []
    linhas.append("RELATÓRIO – AgroSync (cana-de-açúcar)\n")
    linhas.append(f"Gerado em: {datetime.now().isoformat(timespec='seconds')}\n")
    linhas.append("-" * 72 + "\n")
    if not vs:
        linhas.append("Nenhuma simulação.\n")
    else:
        for v in vs:
            linhas.append(f"#{v['id']:03d} {v['data_iso']} | colh:{v['n_colheitadeiras']:>2} | dist:{v['distancia_km']:>5.1f}km | vel:{v['velocidade_kmh']:>5.1f}km/h | desc:{v['tempo_descarga_min']:>5.1f}min | ciclo:{v['tempo_ciclo_min']:>6.1f}min | caminhões:{v['caminhoes_ideais']:>3}\n")
    with open(caminho, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    log_texto(f"Relatório TXT gerado: {caminho}")

def log_texto(msg: str) -> None:
    with open(ARQ_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")

# -----------------------------
# 🖥️ CLI simples
# -----------------------------
def menu() -> str:
    print("\n=== AgroSync (Cap 6) ===")
    print("1) Nova simulação (caminhões ideais)")
    print("2) Listar simulações")
    print("3) Salvar JSON")
    print("4) Carregar JSON")
    print("5) Gerar relatório TXT")
    print("0) Sair")
    return input("Opção: ").strip()

def main() -> None:
    repo: Repository = MockRepository(SIMULACOES)
    while True:
        op = menu()
        try:
            if op == "1":
                cultura = "cana-de-açúcar"
                n_colh = int(input("Nº colheitadeiras: ").strip())
                dist = float(input("Distância campo-usina (km): ").strip())
                vel = float(input("Velocidade média caminhão (km/h): ").strip())
                t_desc = float(input("Tempo de descarga (min): ").strip())
                t_carr = float(input("Tempo de carregamento por caminhão (min): ").strip())
                s = adicionar_simulacao(repo, cultura, n_colh, dist, vel, t_desc, t_carr)
                print(f"🚜 Caminhões ideais sugeridos: {s['caminhoes_ideais']}")
            elif op == "2":
                for s in repo.listar():
                    print(s)
            elif op == "3":
                salvar_json(SIMULACOES, ARQ_JSON)
                print(f"✅ JSON salvo em {ARQ_JSON}")
            elif op == "4":
                carregar_json(SIMULACOES, ARQ_JSON)
                print(f"✅ JSON carregado de {ARQ_JSON}")
            elif op == "5":
                gerar_relatorio_txt(SIMULACOES, ARQ_TXT)
                print(f"✅ Relatório gerado em {ARQ_TXT}")
            elif op == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print(f"❌ Erro: {e}")
            log_texto(f"ERRO: {e}")

if __name__ == "__main__":
    main()
