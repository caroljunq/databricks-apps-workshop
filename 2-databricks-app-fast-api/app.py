import pandas as pd
from fastapi import FastAPI, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
import uvicorn

log = logging.getLogger('uvicorn')
log.setLevel(logging.ERROR)

app = FastAPI(
    title="AutoScore API",
    description="API de seleção de modelos de scoring para o setor automotivo",
    version="1.0.0"
)

# --- Catálogo simulado de modelos de ML disponíveis ---
MODELOS_DISPONIVEIS = {
    "score_credito_pf": {
        "nome": "Score de Crédito PF",
        "descricao": "Modelo de risco de crédito para pessoa física",
        "segmentos": ["pf"],
        "ticket_max": 150000,
        "categorias_veiculo": ["hatch", "sedan", "suv"]
    },
    "score_credito_pj": {
        "nome": "Score de Crédito PJ",
        "descricao": "Modelo de risco de crédito para pessoa jurídica e frotas",
        "segmentos": ["pj", "frota"],
        "ticket_max": 500000,
        "categorias_veiculo": ["suv", "pickup", "caminhao", "van"]
    },
    "score_fraude_identidade": {
        "nome": "Score Antifraude - Identidade",
        "descricao": "Modelo de detecção de fraude documental e identidade sintética",
        "segmentos": ["pf", "pj"],
        "ticket_max": 999999,
        "categorias_veiculo": ["hatch", "sedan", "suv", "pickup", "caminhao", "van"]
    },
    "score_propensao_premium": {
        "nome": "Score Propensão Premium",
        "descricao": "Modelo de propensão para veículos de alto valor",
        "segmentos": ["pf"],
        "ticket_max": 999999,
        "categorias_veiculo": ["suv", "sedan"]
    }
}


# --- Modelo Pydantic para request body ---
class SolicitacaoScore(BaseModel):
    cpf_cnpj: str = Field(
        ...,
        min_length=11,
        max_length=14,
        description="CPF (11 dígitos) ou CNPJ (14 dígitos) do solicitante",
        examples=["12345678901"]
    )
    valor_veiculo: float = Field(
        ...,
        gt=0,
        description="Valor do veículo em reais",
        examples=[85000.00]
    )
    categoria_veiculo: str = Field(
        ...,
        description="Categoria do veículo",
        examples=["suv"]
    )
    segmento: str = Field(
        default="pf",
        description="Segmento do cliente: pf, pj ou frota",
        examples=["pf"]
    )


# --- Rota 1: Hello World original ---
@app.get('/api', response_class=HTMLResponse, summary="Health Check", tags=["Geral"])
def hello_world():
    chart_data = pd.DataFrame({'Apps': [x for x in range(30)],
                               'Fun with data': [2 ** x for x in range(30)]})
    return f'<h1>Hello, World!</h1> {chart_data.to_html(index=False)}'


# --- Rota 2: Listar modelos disponíveis ---
@app.get(
    '/api/modelos',
    response_class=JSONResponse,
    summary="Listar modelos de scoring disponíveis",
    tags=["Modelos"]
)
def listar_modelos(
    segmento: Optional[str] = Query(
        default=None,
        description="Filtrar por segmento: pf, pj ou frota"
    )
):
    """
    Retorna o catálogo de modelos de ML disponíveis para scoring.

    Opcionalmente filtra por **segmento** do cliente.
    """
    if segmento:
        filtrado = {
            k: v for k, v in MODELOS_DISPONIVEIS.items()
            if segmento in v["segmentos"]
        }
        return {"modelos": filtrado, "filtro_aplicado": segmento}

    return {"modelos": MODELOS_DISPONIVEIS, "total": len(MODELOS_DISPONIVEIS)}


# --- Rota 3: Selecionar modelo ideal (POST com 2+ parâmetros no body) ---
@app.post(
    '/api/selecionar-modelo',
    response_class=JSONResponse,
    summary="Selecionar modelo de scoring ideal",
    tags=["Modelos"]
)
def selecionar_modelo(solicitacao: SolicitacaoScore):
    """
    Recebe os parâmetros do cliente e do veículo no **body** da requisição
    e retorna o(s) modelo(s) de scoring mais adequado(s).

    Lógica de seleção baseada em:
    - **segmento** do cliente (PF, PJ, frota)
    - **categoria** do veículo (hatch, sedan, suv, pickup, caminhao, van)
    - **valor** do veículo (ticket)

    Exemplo de body:
    ```json
    {
        "cpf_cnpj": "12345678901",
        "valor_veiculo": 85000.00,
        "categoria_veiculo": "suv",
        "segmento": "pf"
    }
    ```
    """
    modelos_selecionados = []

    for modelo_id, modelo in MODELOS_DISPONIVEIS.items():
        if (
            solicitacao.segmento in modelo["segmentos"]
            and solicitacao.categoria_veiculo in modelo["categorias_veiculo"]
            and solicitacao.valor_veiculo <= modelo["ticket_max"]
        ):
            modelos_selecionados.append({
                "modelo_id": modelo_id,
                "nome": modelo["nome"],
                "descricao": modelo["descricao"]
            })

    return {
        "cliente": solicitacao.cpf_cnpj,
        "parametros_recebidos": {
            "valor_veiculo": solicitacao.valor_veiculo,
            "categoria": solicitacao.categoria_veiculo,
            "segmento": solicitacao.segmento
        },
        "modelos_recomendados": modelos_selecionados,
        "total_modelos": len(modelos_selecionados)
    }


# --- Rota 4: Consultar score por modelo e CPF/CNPJ (path params) ---
@app.get(
    '/api/score/{modelo_id}/{cpf_cnpj}',
    response_class=JSONResponse,
    summary="Consultar score de um modelo específico",
    tags=["Scoring"]
)
def consultar_score(
    modelo_id: str = Path(
        ...,
        description="ID do modelo de scoring (ex: score_credito_pf)"
    ),
    cpf_cnpj: str = Path(
        ...,
        min_length=11,
        max_length=14,
        description="CPF ou CNPJ do solicitante"
    )
):
    """
    Recebe **2 parâmetros pela URL** (modelo + documento) e retorna o score simulado.

    Demonstra path parameters com validação.
    Em produção, aqui seria feita a chamada ao modelo servido no Databricks Model Serving.
    """
    if modelo_id not in MODELOS_DISPONIVEIS:
        return JSONResponse(
            status_code=404,
            content={"erro": f"Modelo '{modelo_id}' não encontrado",
                     "modelos_validos": list(MODELOS_DISPONIVEIS.keys())}
        )

    # Simulação de score — em produção, chamaria o endpoint do Model Serving
    import hashlib
    hash_val = int(hashlib.md5(f"{modelo_id}{cpf_cnpj}".encode()).hexdigest(), 16)
    score_simulado = (hash_val % 1000) / 10  # score entre 0 e 100

    faixa = "alto_risco" if score_simulado < 30 else "medio_risco" if score_simulado < 70 else "baixo_risco"

    return {
        "modelo": MODELOS_DISPONIVEIS[modelo_id]["nome"],
        "modelo_id": modelo_id,
        "documento": cpf_cnpj,
        "score": round(score_simulado, 1),
        "faixa_risco": faixa,
        "nota": "Score simulado para fins de demonstração"
    }


if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 8000))

    uvicorn.run(app, host=host, port=port)
    print(f"FastAPI app running on http://{host}:{port}")
