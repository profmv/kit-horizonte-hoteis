#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerador_hotelaria_horizonte.py  v1.0
=====================================
Gerador de dataset sintético para a rede fictícia "Horizonte Hotéis & Resorts"
— 10 hotéis em destinos brasileiros reais, 24 meses de operação.

REGRAS DE NEGÓCIO REAIS DO SETOR embutidas no gerador:
  • Bandeiras por segmento (inspirado em Accor/Marriott):
      Horizonte Express (3★ econômico) / Horizonte Plaza (4★ upscale) /
      Horizonte Grand Resort (5★ lazer).
  • Fidelidade por frequência (estilo ALL/Bonvoy): Bronze→Prata→Ouro→Diamante,
    com desconto crescente na diária — o nível é DERIVADO da frequência real
    de hospedagem do hóspede no dataset (top 5% = Diamante etc.).
  • Revenue management / tarifa dinâmica: a diária varia com sazonalidade do
    destino (praia no verão, serra no inverno, urbano em dias úteis), eventos
    (Réveillon, Carnaval, férias de julho), dia da semana, antecedência da
    reserva (booking curve) e canal de venda (paridade tarifária + walk-in).
  • Canais de venda com economics reais: OTAs cobram 15–18% de comissão
    (tabela de-para sugerida no MD → medida de Receita Líquida).
  • RESTRIÇÃO ESTRUTURAL: um mesmo quarto NUNCA tem reservas sobrepostas —
    a agenda de cada quarto é construída sequencialmente (check-out de uma
    reserva ≤ check-in da seguinte), validada ao final.
  • SLA de manutenção por prioridade (Alta 2h / Média 8h / Baixa 24h) com
    ~78% de cumprimento e avaliação do hóspede correlacionada ao atraso.

SEM CAMPOS VAZIOS: estados são expressos por Status_Reserva (Confirmada /
Hospedado / Check-out Realizado / Cancelada / No-Show), nunca por nulos.

7 TABELAS (6–10 campos cada):
  hoteis(10) · quartos(8) · hospedes(10) · funcionarios(8) ·
  reservas(10) · consumos_extras(7) · chamados_manutencao(8)

SAÍDAS (mesma base limpa → 3 versões comparáveis):
  v1_desnormalizada_com_erros/  → tabelão (grão = reserva, consumos agregados)
  v2_normalizada_com_erros/     → 7 CSVs com sujeira natural de PMS/OTA
  v3_normalizada_perfeita/      → 7 CSVs limpos (gabarito, validado)
  DICAS_POWERBI.md              → roteiro de limpeza, DAX (ADR/RevPAR/ocupação)

Dependências : pandas, numpy (stdlib: random, datetime, unicodedata, os, time)
Dados externos: nomes_data.py (NOMES_MASCULINOS, NOMES_FEMININOS, SOBRENOMES)
Execução     : python gerador_hotelaria_horizonte.py
"""

# ── SEÇÃO 1: Imports e configuração global ───────────────────────────────────
import os
import random
import sys
import time
import unicodedata
from datetime import datetime, timedelta, date

import numpy as np
import pandas as pd

from nomes_data import NOMES_MASCULINOS, NOMES_FEMININOS, SOBRENOMES

# Evita falha com acentos e caracteres de moldura em consoles Windows cp1252.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ══════════════════════════════════════════════════════════════════════════════
N_HOSPEDES     = 4_000
N_FUNCIONARIOS = 180
N_CHAMADOS     = 5_000
SEED           = 42
PASTA_SAIDA    = "dataset_horizonte_hoteis"
# O nº de reservas emerge da agenda dos quartos (~30-40 mil) — não é fixado.
# ══════════════════════════════════════════════════════════════════════════════

random.seed(SEED)
np.random.seed(SEED)
DATA_REF    = datetime(2026, 6, 30)             # "hoje" — define os status
DATA_INICIO = DATA_REF - timedelta(days=730)    # 24 meses de operação
DATA_FIM    = DATA_REF + timedelta(days=90)     # reservas futuras confirmadas
t0 = time.time()
print("╔════════════════════════════════════════════════════════════════╗")
print("║  Horizonte Hotéis & Resorts — Gerador de dataset v1.0          ║")
print("╚════════════════════════════════════════════════════════════════╝")


# ── SEÇÃO 2: Listas base (combinação de sublistas — nada enumerado à mão) ────

# Destinos REAIS com perfil turístico real (define sazonalidade e passeios):
DESTINOS = [
    # (cidade, UF, perfil, bandeira, nº quartos)
    ("Gramado",           "RS", "serra",  "Horizonte Plaza",        44),
    ("Campos do Jordão",  "SP", "serra",  "Horizonte Grand Resort", 38),
    ("Porto de Galinhas", "PE", "praia",  "Horizonte Grand Resort", 52),
    ("Búzios",            "RJ", "praia",  "Horizonte Plaza",        36),
    ("Maceió",            "AL", "praia",  "Horizonte Plaza",        46),
    ("Florianópolis",     "SC", "praia",  "Horizonte Express",      40),
    ("Bonito",            "MS", "eco",    "Horizonte Plaza",        30),
    ("Foz do Iguaçu",     "PR", "eco",    "Horizonte Express",      42),
    ("São Paulo",         "SP", "urbano", "Horizonte Express",      58),
    ("Belo Horizonte",    "MG", "urbano", "Horizonte Plaza",        40),
]

# Sazonalidade mensal por perfil (a MESMA função alimenta demanda e tarifa —
# assim ocupação e ADR ficam correlacionados, e o RevPAR conta uma história):
PESO_MES = {
    "praia":  {1: 1.8, 2: 1.6, 3: 1.2, 4: 1.0, 5: .85, 6: .75, 7: 1.1,
               8: .8, 9: .9, 10: 1.0, 11: 1.15, 12: 1.7},
    "serra":  {1: 1.1, 2: .9, 3: .85, 4: .95, 5: 1.15, 6: 1.6, 7: 1.8,
               8: 1.5, 9: 1.0, 10: 1.05, 11: 1.25, 12: 1.6},   # Natal Luz!
    "eco":    {1: 1.4, 2: 1.1, 3: 1.0, 4: 1.05, 5: 1.0, 6: 1.1, 7: 1.5,
               8: 1.1, 9: 1.0, 10: 1.05, 11: 1.0, 12: 1.3},
    "urbano": {1: .8, 2: .95, 3: 1.1, 4: 1.1, 5: 1.15, 6: 1.05, 7: .9,
               8: 1.1, 9: 1.15, 10: 1.15, 11: 1.1, 12: .75},   # esvazia no fim de ano
}
# Dia da semana: lazer lota sex/sáb; urbano lota ter-qui (viagem corporativa):
PESO_DIA = {"lazer":  {0: .8, 1: .75, 2: .8, 3: 1.0, 4: 1.55, 5: 1.7, 6: 1.0},
            "urbano": {0: 1.15, 1: 1.35, 2: 1.35, 3: 1.25, 4: .85, 5: .6, 6: .75}}
# Eventos nacionais (datas reais aproximadas) que inflam demanda e tarifa:
EVENTOS = [((12, 27), (1, 2), 1.9, ("praia", "serra")),        # Réveillon
           ((2, 13), (2, 18), 1.7, ("praia", "urbano")),       # Carnaval 2026
           ((2, 28), (3, 5), 1.7, ("praia", "urbano")),        # Carnaval 2025
           ((7, 1), (7, 31), 1.35, ("serra", "eco"))]          # férias de julho

# Tipos de quarto: multiplicador de tarifa e capacidade (padrão do setor):
TIPOS_QUARTO = {"Standard": (1.00, 2), "Superior": (1.25, 3),
                "Luxo": (1.60, 3), "Suíte Master": (2.30, 4)}
TIPOS_QUARTO_P = {"Standard": 0.45, "Superior": 0.28, "Luxo": 0.18,
                  "Suíte Master": 0.09}
VISTAS_POR_PERFIL = {"praia": ["Mar", "Piscina", "Jardim"],
                     "serra": ["Montanha", "Jardim", "Vale"],
                     "eco": ["Mata", "Jardim", "Piscina"],
                     "urbano": ["Cidade", "Avenida", "Interna"]}
TARIFA_BASE_BANDEIRA = {"Horizonte Express": (180, 260),
                        "Horizonte Plaza": (330, 520),
                        "Horizonte Grand Resort": (680, 1300)}

CANAIS_P = {"OTA BookNow": 0.30, "Site Próprio": 0.26, "OTA ViajaMais": 0.16,
            "Balcão": 0.10, "Agência de Turismo": 0.10, "Central Telefônica": 0.08}
LEAD_POR_CANAL = {"OTA BookNow": (3, 120), "OTA ViajaMais": (3, 120),
                  "Site Próprio": (1, 90), "Balcão": (0, 0),
                  "Agência de Turismo": (10, 180), "Central Telefônica": (0, 30)}
FATOR_CANAL = {"Balcão": 1.05, "Site Próprio": 1.0, "OTA BookNow": 1.0,
               "OTA ViajaMais": 1.0, "Agência de Turismo": 0.97,
               "Central Telefônica": 1.0}
DESCONTO_FIDELIDADE = {"Bronze": 0.0, "Prata": 0.03, "Ouro": 0.06,
                       "Diamante": 0.10}

SETORES_CARGOS = {  # (setor, cargo, faixa salarial R$)
    "Recepção":   [("Recepcionista", 2100, 3200), ("Concierge", 2600, 4200),
                   ("Auditor Noturno", 2500, 3600)],
    "Governança": [("Camareira", 1700, 2400), ("Supervisora de Andar", 2400, 3400)],
    "Manutenção": [("Técnico de Manutenção", 2300, 3600),
                   ("Eletricista Predial", 2800, 4200)],
    "A&B":        [("Garçom", 1800, 2600), ("Cozinheiro", 2400, 3800),
                   ("Barman", 2000, 3000)],
    "Gestão":     [("Gerente Geral", 9000, 18000),
                   ("Gerente de Hospedagem", 6000, 10000)],
}
TURNOS = ["Manhã", "Tarde", "Noite"]
PROVEDORES = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br",
              "uol.com.br", "icloud.com"]

# Consumos extras: itens por combinação categoria × cardápio (passeios variam
# com o perfil real do destino — escuna na praia, vinícola na serra etc.):
CONSUMOS = {
    "Restaurante":    {"preco": (28, 140), "itens":
                       ["Jantar Executivo", "Almoço Buffet", "Risoto de Camarão",
                        "Pizza Margherita", "Taça de Vinho Tinto",
                        "Porção de Petiscos", "Sobremesa da Casa"]},
    "Frigobar":       {"preco": (6, 28), "itens":
                       ["Água Mineral 500 ml", "Refrigerante Lata",
                        "Cerveja Long Neck", "Chocolate", "Mix de Castanhas",
                        "Suco Natural"]},
    "Room Service":   {"preco": (24, 90), "itens":
                       ["Sanduíche Club", "Omelete com Salada", "Tábua de Frios",
                        "Café da Manhã no Quarto"]},
    "Spa":            {"preco": (120, 420), "itens":
                       ["Massagem Relaxante 50 min", "Day Use Spa",
                        "Circuito de Sauna", "Tratamento Facial"]},
    "Lavanderia":     {"preco": (12, 45), "itens":
                       ["Lavagem de Peça", "Passadoria Express",
                        "Lavagem a Seco"]},
    "Estacionamento": {"preco": (25, 60), "itens": ["Diária de Estacionamento",
                                                    "Valet"]},
    "Passeio":        {"preco": (90, 480), "itens": None},  # depende do destino
}
PASSEIOS_POR_PERFIL = {
    "praia":  ["Passeio de Escuna", "Mergulho com Cilindro", "Passeio de Buggy",
               "Aula de Stand-Up Paddle"],
    "serra":  ["Tour de Vinícolas", "Noite de Fondue", "Passeio de Teleférico",
               "Trilha ao Mirante"],
    "eco":    ["Flutuação em Rio Cristalino", "Trilha na Mata com Guia",
               "Rapel na Cachoeira", "Passeio de Barco no Rio"],
    "urbano": ["City Tour Histórico", "Tour Gastronômico", "Ingresso de Museu",
               "Transfer Aeroporto"],
}
# Peso das categorias de consumo por bandeira (resort vende spa; econômico não):
PESO_CONSUMO = {
    "Horizonte Express":      {"Frigobar": 3, "Estacionamento": 2.5,
                               "Restaurante": 1.5, "Lavanderia": 1,
                               "Room Service": 1, "Passeio": .5, "Spa": .1},
    "Horizonte Plaza":        {"Restaurante": 3, "Frigobar": 2.2,
                               "Room Service": 1.6, "Passeio": 1.4,
                               "Estacionamento": 1.4, "Spa": 1, "Lavanderia": .8},
    "Horizonte Grand Resort": {"Restaurante": 3.2, "Passeio": 2.6, "Spa": 2.4,
                               "Room Service": 1.8, "Frigobar": 1.6,
                               "Lavanderia": .7, "Estacionamento": .6},
}
FATOR_QTD_CONSUMO = {"Horizonte Express": 0.55, "Horizonte Plaza": 1.1,
                     "Horizonte Grand Resort": 2.1}

CHAMADOS_TIPOS_P = {"Ar-condicionado": 0.22, "Wi-Fi": 0.16, "Hidráulica": 0.14,
                    "Elétrica": 0.12, "TV / Controle": 0.10,
                    "Limpeza Extra": 0.14, "Fechadura Eletrônica": 0.07,
                    "Frigobar com Defeito": 0.05}
SLA_HORAS = {"Alta": 2, "Média": 8, "Baixa": 24}
PRIORIDADES_P = {"Alta": 0.22, "Média": 0.47, "Baixa": 0.31}


# ── SEÇÃO 3: Funções auxiliares ──────────────────────────────────────────────
_ids: set = set()

def gerar_id(pref: str, n: int) -> str:
    while True:
        _id = f"{pref}-{''.join(random.choices('0123456789', k=n))}"
        if _id not in _ids:
            _ids.add(_id)
            return _id


def gerar_cpf_valido() -> str:
    d = [random.randint(0, 9) for _ in range(9)]
    for k in (10, 11):
        s = sum(a * b for a, b in zip(d, range(k, 1, -1)))
        d.append((s * 10) % 11 % 10)
    return "{}{}{}.{}{}{}.{}{}{}-{}{}".format(*d)


def gerar_nome(genero=None):
    if genero is None:
        genero = random.choice(["M", "F"])
    prim = random.choice(NOMES_MASCULINOS if genero == "M" else NOMES_FEMININOS)
    return (f"{prim} {' '.join(random.sample(SOBRENOMES, random.choice([1, 2, 2])))}",
            genero)


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def gerar_email(nome: str) -> str:
    p = sem_acento(nome).lower().split()
    base = f"{p[0]}{random.choice(['.', '_', ''])}{p[-1]}"
    if random.random() < 0.35:
        base += str(random.randint(1, 99))
    return f"{base}@{random.choice(PROVEDORES)}"


def sortear(dic):
    return random.choices(list(dic), weights=list(dic.values()))[0]


def demanda(d: date, perfil: str) -> float:
    """Fator de demanda [≈0.4 – 2.2] — alimenta ocupação E tarifa dinâmica."""
    f = PESO_MES[perfil][d.month]
    grupo = "urbano" if perfil == "urbano" else "lazer"
    f *= PESO_DIA[grupo][d.weekday()]
    for (mi, di), (mf, df_), mult, perfis in EVENTOS:
        dentro = ((d.month, d.day) >= (mi, di)) if mi <= mf else False
        if mi > mf:  # evento que cruza o ano (Réveillon)
            dentro = (d.month, d.day) >= (mi, di) or (d.month, d.day) <= (mf, df_)
        else:
            dentro = (mi, di) <= (d.month, d.day) <= (mf, df_)
        if dentro and perfil in perfis:
            f *= mult
    return f


# ── SEÇÃO 4: Dimensões — HOTÉIS, QUARTOS, HÓSPEDES, FUNCIONÁRIOS ─────────────
print("[1/6] Gerando dimensões ...")

HOTEIS, QUARTOS = [], []
for cidade, uf, perfil, bandeira, n_qts in DESTINOS:
    hid = gerar_id("HTL", 3)
    estrelas = {"Horizonte Express": 3, "Horizonte Plaza": 4,
                "Horizonte Grand Resort": 5}[bandeira]
    HOTEIS.append({"Hotel_ID": hid, "Hotel_Nome": f"{bandeira} {cidade}",
                   "Bandeira": bandeira, "Cidade": cidade, "UF": uf,
                   "Perfil_Destino": perfil, "Categoria_Estrelas": estrelas,
                   "Qtd_Quartos": n_qts,
                   "Ano_Inauguracao": random.randint(1994, 2022),
                   "Nota_Media_Avaliacao": round(random.uniform(7.6, 9.6), 1)})
    base_lo, base_hi = TARIFA_BASE_BANDEIRA[bandeira]
    for i in range(n_qts):
        andar = i // 12 + 1
        tipo = sortear(TIPOS_QUARTO_P)
        mult, cap = TIPOS_QUARTO[tipo]
        vista = random.choice(VISTAS_POR_PERFIL[perfil])
        tarifa = random.uniform(base_lo, base_hi) * mult
        if vista in ("Mar", "Montanha"):        # vista premium (+15%)
            tarifa *= 1.15
        QUARTOS.append({"Quarto_ID": gerar_id("QRT", 5), "Hotel_ID": hid,
                        "Numero_Quarto": andar * 100 + (i % 12) + 1,
                        "Andar": andar, "Tipo_Quarto": tipo,
                        "Capacidade_Pessoas": cap, "Vista": vista,
                        "Tarifa_Base_Diaria": round(tarifa, 2)})
df_hoteis = pd.DataFrame(HOTEIS)
df_quartos = pd.DataFrame(QUARTOS)

# HÓSPEDES — o nível de fidelidade é DERIVADO da propensão a viajar (peso
# lognormal): quem mais se hospeda sobe de tier, como nos programas reais.
HOSPEDES = []
_pesos_hosp = np.random.lognormal(mean=0.0, sigma=1.0, size=N_HOSPEDES)
_quantis = np.quantile(_pesos_hosp, [0.70, 0.88, 0.96])
CIDADES_ORIGEM = [("São Paulo", "SP"), ("Campinas", "SP"), ("Rio de Janeiro", "RJ"),
                  ("Belo Horizonte", "MG"), ("Curitiba", "PR"),
                  ("Porto Alegre", "RS"), ("Brasília", "DF"), ("Salvador", "BA"),
                  ("Goiânia", "GO"), ("Recife", "PE"), ("Ribeirão Preto", "SP"),
                  ("Londrina", "PR"), ("Uberlândia", "MG"), ("Niterói", "RJ")]
for k in range(N_HOSPEDES):
    nome, gen = gerar_nome()
    cid, uf = random.choice(CIDADES_ORIGEM)
    w = _pesos_hosp[k]
    tier = ("Diamante" if w >= _quantis[2] else "Ouro" if w >= _quantis[1]
            else "Prata" if w >= _quantis[0] else "Bronze")
    nasc = DATA_REF - timedelta(days=random.randint(19 * 365, 78 * 365))
    HOSPEDES.append({"Hospede_ID": gerar_id("HSP", 6), "Hospede_Nome": nome,
                     "CPF": gerar_cpf_valido(), "Sexo": gen,
                     "Data_Nascimento": nasc.date().isoformat(),
                     "Cidade_Origem": cid, "UF_Origem": uf,
                     "Email": gerar_email(nome),
                     "Telefone": f"({random.choice(['11','21','31','41','51','61','19','16','62','81'])}) "
                                 f"9{random.randint(6000, 9999)}-{random.randint(1000, 9999)}",
                     "Nivel_Fidelidade": tier})
df_hosp = pd.DataFrame(HOSPEDES)
_hosp_ids = df_hosp["Hospede_ID"].tolist()
_hosp_tier = dict(zip(df_hosp["Hospede_ID"], df_hosp["Nivel_Fidelidade"]))
_hosp_pesos = list(_pesos_hosp)

# FUNCIONÁRIOS — todo hotel garante equipe mínima de Manutenção e Governança
FUNC = []
_hotel_ids = df_hoteis["Hotel_ID"].tolist()
for hid in _hotel_ids:                      # esqueleto mínimo por hotel
    for setor in ("Manutenção", "Governança", "Recepção"):
        cargo, lo, hi = random.choice(SETORES_CARGOS[setor])
        nome, gen = gerar_nome()
        FUNC.append({"Funcionario_ID": gerar_id("FUN", 5),
                     "Funcionario_Nome": nome, "Hotel_ID": hid,
                     "Setor": setor, "Cargo": cargo,
                     "Turno": random.choice(TURNOS),
                     "Data_Admissao": (DATA_REF - timedelta(
                         days=random.randint(120, 4000))).date().isoformat(),
                     "Salario_Mensal": round(random.uniform(lo, hi), 2)})
while len(FUNC) < N_FUNCIONARIOS:
    setor = random.choice(list(SETORES_CARGOS))
    cargo, lo, hi = random.choice(SETORES_CARGOS[setor])
    nome, gen = gerar_nome()
    FUNC.append({"Funcionario_ID": gerar_id("FUN", 5), "Funcionario_Nome": nome,
                 "Hotel_ID": random.choice(_hotel_ids), "Setor": setor,
                 "Cargo": cargo, "Turno": random.choice(TURNOS),
                 "Data_Admissao": (DATA_REF - timedelta(
                     days=random.randint(120, 4000))).date().isoformat(),
                 "Salario_Mensal": round(random.uniform(lo, hi), 2)})
df_func = pd.DataFrame(FUNC)
_manut_por_hotel = (df_func[df_func["Setor"].isin(["Manutenção", "Governança"])]
                    .groupby("Hotel_ID")["Funcionario_ID"].apply(list).to_dict())


# ── SEÇÃO 5: Fato RESERVAS — agenda sequencial por quarto (sem overlap) ──────
print("[2/6] Construindo a agenda de reservas quarto a quarto ...")

_hotel_por_id = df_hoteis.set_index("Hotel_ID").to_dict("index")
RESERVAS = []

for q in QUARTOS:
    hotel = _hotel_por_id[q["Hotel_ID"]]
    perfil, bandeira = hotel["Perfil_Destino"], hotel["Bandeira"]
    lazer = perfil != "urbano"
    cursor = DATA_INICIO.date() + timedelta(days=random.randint(0, 10))

    while cursor < DATA_FIM.date():
        f_dem = demanda(cursor, perfil)
        # em baixa demanda o quarto fica mais dias vazio; em alta, quase nada:
        gap = random.randint(0, max(1, int(7 / f_dem)))
        checkin = cursor + timedelta(days=gap)
        if lazer and random.random() < 0.45:      # lazer prefere entrar sex/sáb
            while checkin.weekday() not in (4, 5):
                checkin += timedelta(days=1)
        if checkin >= DATA_FIM.date():
            break
        # duração da estadia coerente com o perfil (urbano curto, praia longo):
        noites = (random.choices([1, 2, 3, 4], weights=[35, 35, 20, 10])[0]
                  if perfil == "urbano" else
                  random.choices([2, 3, 4, 5, 7], weights=[22, 28, 24, 16, 10])[0])
        checkout = checkin + timedelta(days=noites)

        canal = sortear(CANAIS_P)
        lead = random.randint(*LEAD_POR_CANAL[canal])
        data_reserva = checkin - timedelta(days=lead)
        hospede = random.choices(_hosp_ids, weights=_hosp_pesos)[0]
        tier = _hosp_tier[hospede]

        # ---- TARIFA DINÂMICA (revenue management) --------------------------
        f_tarifa = min(2.0, max(0.75, f_dem))            # clip do yield
        f_lead = (0.92 if lead > 60 else 0.97 if lead > 30
                  else 1.08 if lead < 7 else 1.0)        # booking curve
        diaria = (q["Tarifa_Base_Diaria"] * f_tarifa * f_lead
                  * FATOR_CANAL[canal] * (1 - DESCONTO_FIDELIDADE[tier])
                  * random.uniform(0.97, 1.03))

        # ---- STATUS coerente com a data de referência ----------------------
        r = random.random()
        if r < 0.075:
            status = "Cancelada"
        elif r < 0.095 and checkin < DATA_REF.date():
            status = "No-Show"
        elif checkout <= DATA_REF.date():
            status = "Check-out Realizado"
        elif checkin <= DATA_REF.date():
            status = "Hospedado"
        else:
            status = "Confirmada"

        RESERVAS.append({
            "Reserva_ID": gerar_id("RSV", 8),
            "Quarto_ID": q["Quarto_ID"],
            "Hospede_ID": hospede,
            "Canal_Venda": canal,
            "Data_Reserva": data_reserva.isoformat(),
            "Data_Checkin": checkin.isoformat(),
            "Data_Checkout": checkout.isoformat(),
            "Qtd_Hospedes": random.randint(1, q["Capacidade_Pessoas"]),
            "Diaria_Media_Cobrada": round(diaria, 2),
            "Status_Reserva": status,
        })
        cursor = checkout   # próxima reserva só após o checkout → sem overlap

df_reservas = pd.DataFrame(RESERVAS)
print(f"        → {len(df_reservas):,} reservas geradas "
      f"(agenda sem sobreposição por quarto)")
# Nota didática: Valor_Total = noites × diária foi deixado DE FORA de
# propósito — o aluno cria a coluna no Power Query / DAX.


# ── SEÇÃO 6: Fatos CONSUMOS_EXTRAS e CHAMADOS_MANUTENCAO ─────────────────────
print("[3/6] Gerando consumos extras e chamados de manutenção ...")

_quarto_hotel = dict(zip(df_quartos["Quarto_ID"], df_quartos["Hotel_ID"]))
CONSUMOS_ROWS = []
for r in RESERVAS:
    if r["Status_Reserva"] in ("Cancelada", "No-Show", "Confirmada"):
        continue                       # só consome quem de fato se hospedou
    hotel = _hotel_por_id[_quarto_hotel[r["Quarto_ID"]]]
    bandeira, perfil = hotel["Bandeira"], hotel["Perfil_Destino"]
    ci = date.fromisoformat(r["Data_Checkin"])
    co = min(date.fromisoformat(r["Data_Checkout"]), DATA_REF.date())
    noites = max((co - ci).days, 1)
    n = np.random.poisson(lam=noites * FATOR_QTD_CONSUMO[bandeira])
    for _ in range(n):
        cat = sortear(PESO_CONSUMO[bandeira])
        cfg = CONSUMOS[cat]
        item = (random.choice(PASSEIOS_POR_PERFIL[perfil]) if cat == "Passeio"
                else random.choice(cfg["itens"]))
        CONSUMOS_ROWS.append({
            "Consumo_ID": gerar_id("CNS", 8),
            "Reserva_ID": r["Reserva_ID"],
            "Data_Consumo": (ci + timedelta(
                days=random.randint(0, max(noites - 1, 0)))).isoformat(),
            "Categoria_Consumo": cat,
            "Item_Descricao": item,
            "Quantidade": random.choices([1, 2, 3, 4],
                                         weights=[55, 25, 12, 8])[0],
            "Valor_Unitario": round(random.uniform(*cfg["preco"]), 2),
        })
df_consumos = pd.DataFrame(CONSUMOS_ROWS)
print(f"        → {len(df_consumos):,} lançamentos de consumo")

CHAMADOS = []
for _ in range(N_CHAMADOS):
    q = random.choice(QUARTOS)
    prioridade = sortear(PRIORIDADES_P)
    sla = SLA_HORAS[prioridade]
    abertura = DATA_INICIO + timedelta(days=random.randint(0, 729),
                                       hours=random.randint(6, 23),
                                       minutes=random.randint(0, 59))
    # tempo de resolução lognormal calibrado p/ ~78% dentro do SLA:
    horas = float(np.random.lognormal(mean=np.log(sla * 0.55), sigma=0.75))
    dentro_sla = horas <= sla
    # avaliação do hóspede correlacionada ao cumprimento do SLA:
    aval = (random.choices([5, 4, 3], weights=[55, 35, 10])[0] if dentro_sla
            else random.choices([3, 2, 1], weights=[40, 35, 25])[0])
    CHAMADOS.append({
        "Chamado_ID": gerar_id("CHM", 7),
        "Quarto_ID": q["Quarto_ID"],
        "Funcionario_ID": random.choice(_manut_por_hotel[q["Hotel_ID"]]),
        "Tipo_Chamado": sortear(CHAMADOS_TIPOS_P),
        "Prioridade": prioridade,
        "Data_Abertura": abertura.strftime("%Y-%m-%d %H:%M:%S"),
        "Data_Fechamento": (abertura + timedelta(hours=horas)
                            ).strftime("%Y-%m-%d %H:%M:%S"),
        "Avaliacao_Atendimento": aval,
    })
df_chamados = pd.DataFrame(CHAMADOS)


# ── SEÇÃO 7: Validações de integridade (versão perfeita) ─────────────────────
print("[4/6] Validando integridade ...")
falhas = []
for nome, df, chave in [("hoteis", df_hoteis, "Hotel_ID"),
                        ("quartos", df_quartos, "Quarto_ID"),
                        ("hospedes", df_hosp, "Hospede_ID"),
                        ("funcionarios", df_func, "Funcionario_ID"),
                        ("reservas", df_reservas, "Reserva_ID"),
                        ("consumos_extras", df_consumos, "Consumo_ID"),
                        ("chamados_manutencao", df_chamados, "Chamado_ID")]:
    if not df[chave].is_unique:
        falhas.append(f"{nome}: {chave} duplicado")
    if df.isna().any().any():          # requisito: NENHUM campo vazio
        falhas.append(f"{nome}: contém valores nulos")

# sem sobreposição de reservas no mesmo quarto:
_r = df_reservas.sort_values(["Quarto_ID", "Data_Checkin"])
_overlap = (_r.groupby("Quarto_ID")["Data_Checkin"].shift(-1)
            < _r["Data_Checkout"]).sum()
if _overlap:
    falhas.append(f"{_overlap} reservas sobrepostas no mesmo quarto")
if (df_reservas["Data_Checkout"] <= df_reservas["Data_Checkin"]).any():
    falhas.append("Reserva com checkout ≤ checkin")
if (df_reservas["Data_Reserva"] > df_reservas["Data_Checkin"]).any():
    falhas.append("Reserva criada depois do check-in")
if not set(df_reservas["Quarto_ID"]) <= set(df_quartos["Quarto_ID"]):
    falhas.append("Reserva com Quarto_ID órfão")
if not set(df_consumos["Reserva_ID"]) <= set(df_reservas["Reserva_ID"]):
    falhas.append("Consumo com Reserva_ID órfão")
if (df_chamados["Data_Fechamento"] < df_chamados["Data_Abertura"]).any():
    falhas.append("Chamado fechado antes de abrir")

if falhas:
    print("!!! VIOLAÇÕES:", *["  ✗ " + f for f in falhas], sep="\n")
    raise AssertionError(f"{len(falhas)} validações falharam.")
print("        → Todas as validações PASSARAM")


# ── SEÇÃO 8: Injeção de erros propositais (sujeira natural de PMS/OTA) ───────
def _p(prob):
    return random.random() < prob

def sujar_texto(s, prob=0.05):
    if not isinstance(s, str) or not _p(prob):
        return s
    op = random.random()
    if op < 0.25: return s.upper()
    if op < 0.45: return s.lower()
    if op < 0.62: return f" {s}" if _p(0.5) else f"{s}  "
    if op < 0.80: return sem_acento(s)
    return s.replace(" ", "  ", 1)

def sujar_data(iso, prob_alt=0.30):
    dt = datetime.fromisoformat(iso)
    if not _p(prob_alt):
        return dt.strftime("%d/%m/%Y %H:%M" if (dt.hour or dt.minute)
                           else "%d/%m/%Y")
    return random.choice([dt.strftime("%Y-%m-%d"), dt.strftime("%d-%m-%Y"),
                          dt.strftime("%d.%m.%y")])

def valor_como_texto(v, prob_rs=0.03):
    txt = f"{v:.2f}".replace(".", ",")
    return f"R$ {txt}" if _p(prob_rs) else txt

def sujar_canal(c):
    if not _p(0.12):
        return c
    return random.choice({"OTA BookNow": ["BookNow", "OTA - BookNow", "booknow"],
                          "OTA ViajaMais": ["ViajaMais", "OTA VIAJAMAIS"],
                          "Site Próprio": ["Site", "site proprio", "WEB"],
                          "Balcão": ["Walk-in", "BALCAO", "balcão "],
                          "Agência de Turismo": ["Agência", "AGENCIA", "Agente"],
                          "Central Telefônica": ["Telefone", "CALL CENTER"],
                          }[c])

def sujar_tipo_quarto(t):
    if not _p(0.10):
        return t
    return random.choice({"Standard": ["STD", "standard", "Standard "],
                          "Superior": ["SUP", "superior", "SUPERIOR"],
                          "Luxo": ["LUXO", "luxo", "Lux"],
                          "Suíte Master": ["Suite Master", "SUÍTE MASTER",
                                           "Ste. Master"]}[t])

def sujar_estrelas(n):
    if not _p(0.20):
        return n
    return random.choice([f"{n} estrelas", "★" * int(n), str(n)])

def sujar_prioridade(p_):
    if not _p(0.10):
        return p_
    return random.choice({"Alta": ["ALTA", "alta", "P1"],
                          "Média": ["Media", "MÉDIA", "P2"],
                          "Baixa": ["baixa", "BAIXA", "P3"]}[p_])

def duplicar_linhas(df, n):
    dup = df.sample(n=n, random_state=random.randint(0, 9999))
    return (pd.concat([df, dup]).sample(frac=1, random_state=SEED)
            .reset_index(drop=True))


def aplicar_sujeira(t: dict) -> dict:
    """Sujeira de sistema real: integração de OTA que duplica reservas, chave
    com espaço, datas invertidas raras, formatos mistos — incidência baixa."""
    t["hoteis"]["Categoria_Estrelas"] = t["hoteis"]["Categoria_Estrelas"].map(sujar_estrelas)
    t["hoteis"]["Nota_Media_Avaliacao"] = t["hoteis"]["Nota_Media_Avaliacao"].map(
        lambda v: f"{v:.1f}".replace(".", ",") if _p(0.4) else v)
    t["hoteis"]["Cidade"] = t["hoteis"]["Cidade"].map(lambda s: sujar_texto(s, 0.15))

    t["quartos"]["Tipo_Quarto"] = t["quartos"]["Tipo_Quarto"].map(sujar_tipo_quarto)
    t["quartos"]["Vista"] = t["quartos"]["Vista"].map(lambda s: sujar_texto(s, 0.06))
    t["quartos"]["Tarifa_Base_Diaria"] = t["quartos"]["Tarifa_Base_Diaria"].map(
        valor_como_texto)

    t["hospedes"]["Hospede_Nome"] = t["hospedes"]["Hospede_Nome"].map(
        lambda s: sujar_texto(s, 0.06))
    t["hospedes"]["Cidade_Origem"] = t["hospedes"]["Cidade_Origem"].map(
        lambda s: sujar_texto(s, 0.05))
    t["hospedes"]["Data_Nascimento"] = t["hospedes"]["Data_Nascimento"].map(sujar_data)
    t["hospedes"]["Telefone"] = t["hospedes"]["Telefone"].map(
        lambda tel: "".join(c for c in tel if c.isdigit()) if _p(0.25) else tel)
    t["hospedes"]["Email"] = t["hospedes"]["Email"].map(
        lambda e: e.upper() if _p(0.05) else e)
    t["hospedes"]["Nivel_Fidelidade"] = t["hospedes"]["Nivel_Fidelidade"].map(
        lambda s: sujar_texto(s, 0.08))

    t["funcionarios"]["Funcionario_Nome"] = t["funcionarios"]["Funcionario_Nome"].map(
        lambda s: sujar_texto(s, 0.05))
    t["funcionarios"]["Cargo"] = t["funcionarios"]["Cargo"].map(
        lambda s: sujar_texto(s, 0.07))
    t["funcionarios"]["Data_Admissao"] = t["funcionarios"]["Data_Admissao"].map(sujar_data)

    rsv = t["reservas"]
    rsv["Canal_Venda"] = rsv["Canal_Venda"].map(sujar_canal)
    rsv["Data_Reserva"] = rsv["Data_Reserva"].map(sujar_data)
    rsv["Data_Checkin"] = rsv["Data_Checkin"].map(lambda d: sujar_data(d, 0.25))
    rsv["Data_Checkout"] = rsv["Data_Checkout"].map(lambda d: sujar_data(d, 0.25))
    rsv["Diaria_Media_Cobrada"] = rsv["Diaria_Media_Cobrada"].map(
        lambda v: valor_como_texto(v, 0.02))
    # ~0,4% com check-in/checkout INVERTIDOS (lançamento trocado no PMS):
    mask = np.random.random(len(rsv)) < 0.004
    rsv.loc[mask, ["Data_Checkin", "Data_Checkout"]] = (
        rsv.loc[mask, ["Data_Checkout", "Data_Checkin"]].values)
    # ~1% das chaves de quarto com espaço à direita (quebra relacionamento):
    mask2 = np.random.random(len(rsv)) < 0.01
    rsv.loc[mask2, "Quarto_ID"] = rsv.loc[mask2, "Quarto_ID"] + " "
    t["reservas"] = duplicar_linhas(rsv, 40)   # integração OTA duplicando

    cns = t["consumos_extras"]
    cns["Categoria_Consumo"] = cns["Categoria_Consumo"].map(
        lambda s: sujar_texto(s, 0.07))
    cns["Item_Descricao"] = cns["Item_Descricao"].map(lambda s: sujar_texto(s, 0.04))
    cns["Valor_Unitario"] = cns["Valor_Unitario"].map(lambda v: valor_como_texto(v, 0.02))
    cns["Data_Consumo"] = cns["Data_Consumo"].map(lambda d: sujar_data(d, 0.25))
    t["consumos_extras"] = duplicar_linhas(cns, 55)

    chm = t["chamados_manutencao"]
    chm["Prioridade"] = chm["Prioridade"].map(sujar_prioridade)
    chm["Tipo_Chamado"] = chm["Tipo_Chamado"].map(lambda s: sujar_texto(s, 0.06))
    chm["Data_Abertura"] = chm["Data_Abertura"].map(sujar_data)
    chm["Data_Fechamento"] = chm["Data_Fechamento"].map(sujar_data)
    return t


# ── SEÇÃO 9: Montagem das 3 versões ──────────────────────────────────────────
print("[5/6] Exportando as três versões ...")
os.makedirs(PASTA_SAIDA, exist_ok=True)
LIMPAS = {"hoteis": df_hoteis, "quartos": df_quartos, "hospedes": df_hosp,
          "funcionarios": df_func, "reservas": df_reservas,
          "consumos_extras": df_consumos, "chamados_manutencao": df_chamados}

def exportar(tabelas, subpasta):
    pasta = os.path.join(PASTA_SAIDA, subpasta)
    os.makedirs(pasta, exist_ok=True)
    for nome, df in tabelas.items():
        df.to_csv(os.path.join(pasta, f"{nome}.csv"), sep=";", index=False,
                  decimal=",", encoding="utf-8-sig")

exportar(LIMPAS, "v3_normalizada_perfeita")
SUJAS = aplicar_sujeira({k: v.copy(deep=True) for k, v in LIMPAS.items()})
exportar(SUJAS, "v2_normalizada_com_erros")

# v1 — tabelão no grão RESERVA, com consumos AGREGADOS (perda de grão
# proposital → discussão de modelagem no MD). fillna(0) garante zero nulos.
agg = (df_consumos.assign(Valor=lambda d: d["Quantidade"] * d["Valor_Unitario"])
       .groupby("Reserva_ID").agg(Qtd_Lancamentos_Extras=("Consumo_ID", "count"),
                                  Valor_Consumos_Extras=("Valor", "sum"))
       .round(2).reset_index())
tabelao = (df_reservas
           .merge(df_quartos, on="Quarto_ID", how="left")
           .merge(df_hoteis.drop(columns=["Qtd_Quartos"]), on="Hotel_ID",
                  how="left")
           .merge(df_hosp, on="Hospede_ID", how="left")
           .merge(agg, on="Reserva_ID", how="left"))
tabelao[["Qtd_Lancamentos_Extras", "Valor_Consumos_Extras"]] = (
    tabelao[["Qtd_Lancamentos_Extras", "Valor_Consumos_Extras"]].fillna(0))
# sujeira própria da v1 (padrão independente da v2):
tabelao["Canal_Venda"] = tabelao["Canal_Venda"].map(sujar_canal)
tabelao["Tipo_Quarto"] = tabelao["Tipo_Quarto"].map(sujar_tipo_quarto)
tabelao["Hospede_Nome"] = tabelao["Hospede_Nome"].map(lambda s: sujar_texto(s, 0.05))
tabelao["Cidade"] = tabelao["Cidade"].map(lambda s: sujar_texto(s, 0.06))
tabelao["Data_Checkin"] = tabelao["Data_Checkin"].map(lambda d: sujar_data(d, 0.25))
tabelao["Data_Checkout"] = tabelao["Data_Checkout"].map(lambda d: sujar_data(d, 0.25))
tabelao["Diaria_Media_Cobrada"] = tabelao["Diaria_Media_Cobrada"].map(
    lambda v: valor_como_texto(v, 0.02))
tabelao = duplicar_linhas(tabelao, 60)
_p1 = os.path.join(PASTA_SAIDA, "v1_desnormalizada_com_erros")
os.makedirs(_p1, exist_ok=True)
tabelao.to_csv(os.path.join(_p1, "reservas_desnormalizada.csv"), sep=";",
               index=False, decimal=",", encoding="utf-8-sig")


# ── SEÇÃO 10: DICAS_POWERBI.md ───────────────────────────────────────────────
print("[6/6] Escrevendo DICAS_POWERBI.md ...")
MD = f"""# Horizonte Hotéis & Resorts — Guia de estudo Power BI

Dataset sintético de hotelaria: **{len(df_reservas):,} reservas**,
{len(df_consumos):,} consumos extras e {len(df_chamados):,} chamados de
manutenção em {len(df_hoteis)} hotéis ({len(df_quartos)} quartos),
{DATA_INICIO:%m/%Y} a {DATA_FIM:%m/%Y}. Data de referência dos status:
**{DATA_REF:%d/%m/%Y}**. SEED={SEED} — reproduzível. Sem campos vazios:
estados são expressos em `Status_Reserva`.

## As três versões

| Pasta | Conteúdo | Objetivo |
|---|---|---|
| `v1_desnormalizada_com_erros/` | 1 CSV (grão = reserva; consumos agregados) | Limpar e normalizar no Power Query. Bônus: discutir a **perda de grão** dos consumos agregados |
| `v2_normalizada_com_erros/` | 7 CSVs sujos | Limpeza tabela a tabela + relacionamentos |
| `v3_normalizada_perfeita/` | 7 CSVs limpos | Gabarito validado (sem overlap de reservas, FKs íntegras) |

Modelo: `hoteis 1─N quartos 1─N reservas N─1 hospedes`;
`reservas 1─N consumos_extras`; `quartos 1─N chamados N─1 funcionarios`.
Duas tabelas fato com grãos diferentes (reserva × lançamento de consumo) —
exercício clássico de modelo com múltiplas fatos.

## Regras de negócio reais embutidas (explorem nas análises!)

* **Tarifa dinâmica**: a diária sobe com a demanda (verão na praia, inverno
  na serra, Réveillon, Carnaval, julho), com reserva de última hora (<7 dias)
  e no balcão; cai com antecedência >60 dias e agência. Ocupação e ADR são
  correlacionados — o RevPAR revela isso.
* **Perfis de destino**: hotéis urbanos lotam **terça a quinta** (corporativo);
  praia/serra lotam **sexta e sábado**. Compare os heatmaps!
* **Fidelidade por frequência**: Diamante/Ouro têm desconto (10%/6%) e são
  os hóspedes que mais repetem — analise receita por tier.
* **Comissão de OTA** (crie a tabela de-para): OTA BookNow 18%, OTA ViajaMais
  15%, Agência 10%, demais 0% → medida de **Receita Líquida de Canal**.
* **SLA de manutenção**: Alta 2 h, Média 8 h, Baixa 24 h (~78% cumprido);
  a avaliação do hóspede cai quando o SLA estoura.

## Erros plantados (incidência baixa e irregular)

1. Espaços perdidos, CAIXA alta/baixa e acentos removidos em nomes, cidades,
   tipos de quarto (`STD`/`Standard `/`LUXO`) e categorias de consumo.
2. Datas como texto em formatos mistos (`DD/MM/AAAA`, `AAAA-MM-DD`,
   `DD-MM-AAAA`, `DD.MM.AA`) em várias colunas.
3. Valores como texto com vírgula e alguns `R$ 1.234,56` (diárias, tarifas,
   consumos, nota de avaliação `8,7`).
4. `Categoria_Estrelas` ora número, ora `"4 estrelas"`, ora `"★★★★"`.
5. Canais ambíguos: `BookNow`/`OTA - BookNow`/`booknow`; `Walk-in`/`BALCAO`;
   prioridades `P1`/`ALTA`/`alta`.
6. Telefones com e sem máscara.
7. **Duplicatas** em reservas (integração da OTA lançou duas vezes — dor
   real de hotelaria), consumos e no tabelão.
8. **~1% dos `Quarto_ID` em reservas com espaço à direita** → o
   relacionamento com `quartos` perde linhas até aplicar `Text.Trim` na chave.
9. **~0,4% das reservas com check-in/checkout invertidos** — crie uma coluna
   de validação (`Data_Checkout > Data_Checkin?`) e decida o tratamento.

## Roteiro Power Query (estado ótimo)

1. Importar com `;`, desligar detecção automática de tipos.
2. `Text.Trim`/`Text.Clean` em textos **e nas chaves** (`Quarto_ID`!).
3. `Text.Proper` em nomes; de-para (Replace/coluna condicional) para canal,
   tipo de quarto, prioridade e nível de fidelidade.
4. Datas: tipo "Usando localidade → pt-BR"; tratar `DD.MM.AA` antes com
   Replace/coluna personalizada.
5. Valores: remover `R$ `, vírgula→ponto (ou localidade), tipar decimal;
   `Categoria_Estrelas` → extrair só o dígito (`Text.Select`).
6. Remover duplicatas por chave (`Reserva_ID`; `Consumo_ID`).
7. Coluna `Noites = Duration.Days([Data_Checkout] - [Data_Checkin])` e
   `Valor_Hospedagem = [Noites] * [Diaria_Media_Cobrada]` (deixado de fora
   de propósito!). Corrigir antes as datas invertidas (noites negativas).
8. Coluna `Lead_Time_Dias` (checkin − data da reserva) e faixas
   (`Última hora` <7, `Normal` 7-30, `Antecipada` 30-60, `Early bird` >60).
9. Coluna `Faixa_Etaria` do hóspede; `Fim_de_Semana?` do check-in.
10. Criar tabela **Comissao_Canal** manualmente (Inserir Dados) e mesclar.
11. Em `chamados_manutencao`, criar `Horas_Resolucao` com a diferença entre
    fechamento e abertura; criar `SLA_Horas` por prioridade (Alta=2,
    Média=8, Baixa=24). Essas colunas alimentam o KPI de SLA.
12. `Dim_Calendario` com `CALENDAR(DATE(2024,7,1), DATE(2026,9,30))`,
    marcar como tabela de datas.
13. Na v1: normalizar por referência (hoteis, quartos, hospedes) e discutir
    por que os consumos agregados impedem análise por categoria.

## Medidas DAX (das básicas às semi-aditivas de hotelaria)

```dax
Receita Hospedagem = SUMX(FILTER(reservas,
    reservas[Status_Reserva] IN {{"Check-out Realizado", "Hospedado"}}),
    reservas[Noites] * reservas[Diaria_Media_Cobrada])

Diárias Vendidas = SUMX(FILTER(reservas,
    reservas[Status_Reserva] IN {{"Check-out Realizado", "Hospedado"}}),
    reservas[Noites])

ADR = DIVIDE([Receita Hospedagem], [Diárias Vendidas])   -- diária média

Diárias Disponíveis =                                     -- semi-aditiva!
    DISTINCTCOUNT(quartos[Quarto_ID]) * COUNTROWS(Dim_Calendario)

Taxa de Ocupação = DIVIDE([Diárias Vendidas no Período], [Diárias Disponíveis])
-- versão por intervalo (quartos ocupados num dia qualquer do filtro):
Diárias Vendidas no Período =
VAR dMin = MIN(Dim_Calendario[Data])
VAR dMax = MAX(Dim_Calendario[Data]) + 1
RETURN SUMX(FILTER(reservas,
        reservas[Data_Checkin] < dMax && reservas[Data_Checkout] > dMin
        && reservas[Status_Reserva] IN {{"Check-out Realizado","Hospedado"}}),
    DATEDIFF(MAX(reservas[Data_Checkin], dMin),
             MIN(reservas[Data_Checkout], dMax), DAY))

RevPAR = DIVIDE([Receita Hospedagem], [Diárias Disponíveis])
Receita Extras = SUMX(consumos_extras,
    consumos_extras[Quantidade] * consumos_extras[Valor_Unitario])
Extras por Reserva = DIVIDE([Receita Extras],
    DISTINCTCOUNT(consumos_extras[Reserva_ID]))
Taxa de Cancelamento = DIVIDE(
    CALCULATE(COUNTROWS(reservas), reservas[Status_Reserva] = "Cancelada"),
    COUNTROWS(reservas))
% No-Show = DIVIDE(CALCULATE(COUNTROWS(reservas),
    reservas[Status_Reserva] = "No-Show"), COUNTROWS(reservas))
Receita Líquida = SUMX(reservas, reservas[Valor_Hospedagem]
    * (1 - RELATED(Comissao_Canal[Percentual])))
% SLA Cumprido = DIVIDE(CALCULATE(COUNTROWS(chamados_manutencao),
    chamados_manutencao[Horas_Resolucao] <= chamados_manutencao[SLA_Horas]),
    COUNTROWS(chamados_manutencao))
Lead Time Médio = AVERAGE(reservas[Lead_Time_Dias])
Receita YTD = TOTALYTD([Receita Hospedagem], Dim_Calendario[Data])
Var % YoY = VAR aa = CALCULATE([Receita Hospedagem],
    SAMEPERIODLASTYEAR(Dim_Calendario[Data]))
    RETURN DIVIDE([Receita Hospedagem] - aa, aa)
Ranking Hotéis = RANKX(ALL(hoteis[Hotel_Nome]), [RevPAR],, DESC, DENSE)
```

## Sugestões de visuais

* **Cartões**: Ocupação %, ADR, RevPAR, Taxa de Cancelamento, % SLA.
* **Linha com 2 eixos**: Ocupação % × ADR por mês — a essência do revenue
  management num único gráfico.
* **Heatmap (matriz)**: dia da semana × hotel com ocupação — compare o
  padrão urbano (ter-qui) com o de lazer (sex-sáb).
* **Dispersão**: ADR × Ocupação por hotel, tamanho = RevPAR (quadrantes de
  performance).
* **Colunas empilhadas**: receita por canal × bandeira; funil de status
  (Confirmada → Hospedado → Check-out / Cancelada / No-Show).
* **Barra**: Ranking de hotéis por RevPAR; top categorias de consumo.
* **Decomposition Tree**: Receita → Bandeira → Hotel → Tipo de Quarto.
* **Mapa**: RevPAR por cidade/UF.
* **Segmentações**: período, bandeira, canal, nível de fidelidade, perfil
  de destino.

## Checagens contra a v3

* Nenhum quarto com reservas sobrepostas (após remover duplicatas!).
* `Data_Checkout > Data_Checkin` em 100% das linhas (após corrigir invertidas).
* Após `Text.Trim`, 100% das reservas casam com `quartos`.
* Dezembro/janeiro nos hotéis de praia e junho/julho nos de serra devem
  liderar ocupação e ADR — se não liderarem, algo se perdeu na limpeza.
"""
with open(os.path.join(PASTA_SAIDA, "DICAS_POWERBI.md"), "w",
          encoding="utf-8") as f:
    f.write(MD)

# ── SEÇÃO 11: Resumo ─────────────────────────────────────────────────────────
print(f"\n{'='*66}\nRESUMO\n{'='*66}")
print(f"• Hotéis: {len(df_hoteis)} | Quartos: {len(df_quartos)} | "
      f"Hóspedes: {len(df_hosp):,} | Funcionários: {len(df_func)}")
print(f"• Reservas: {len(df_reservas):,} | Consumos: {len(df_consumos):,} | "
      f"Chamados: {len(df_chamados):,}")
print(f"• Tabelão v1: {len(tabelao):,} linhas × {len(tabelao.columns)} colunas")
print(f"• Distribuição de status:\n"
      f"{(df_reservas['Status_Reserva'].value_counts(normalize=True) * 100).round(1).to_string()}")
print(f"• Estrutura em ./{PASTA_SAIDA}/ (v1, v2, v3 + DICAS_POWERBI.md)")
print(f"• Tempo total: {time.time() - t0:.1f} s — Concluído! 🏨")
