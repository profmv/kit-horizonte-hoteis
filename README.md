# Horizonte Hotéis & Resorts — Desafio Power BI

Projeto educacional completo para conduzir alunos do dado bruto a um dashboard executivo de hotelaria no Power BI.

**Site publicado:** https://profmv.github.io/kit-horizonte-hoteis/

## Estrutura

- `index.html`, `styles.css`, `script.js`: site estático compatível com GitHub Pages.
- `gerador_hotelaria_horizonte.py`: fonte da verdade do dataset sintético.
- `nomes_data.py`: listas auxiliares usadas pelo gerador.
- `dataset_horizonte_hoteis/`: três versões da base e guia Power BI, criados pelo gerador.
- `PLANO_DE_AULA.md`: roteiro de condução para o professor.
- `GABARITO_VALIDACAO.md`: contagens e KPIs esperados para conferência.
- `requirements.txt`: dependências Python.

## Gerar os dados

```powershell
python -m pip install -r requirements.txt
python gerador_hotelaria_horizonte.py
```

O script é determinístico (`SEED=42`) e exporta CSV com separador `;` e codificação UTF-8 com BOM.

## Abrir o site localmente

O site não precisa de build. Abra `index.html` ou use um servidor local:

```powershell
python -m http.server 8000
```

Depois acesse `http://localhost:8000`.

## Publicar no GitHub Pages

Em **Settings → Pages**, selecione **Deploy from a branch**, branch `main` e pasta `/ (root)`. O arquivo `.nojekyll` evita processamento desnecessário.

## Entrega esperada do aluno

Um arquivo `.pbix` com quatro páginas, modelo validado, medidas DAX, pelo menos três insights e três recomendações executivas.
