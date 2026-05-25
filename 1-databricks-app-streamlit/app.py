import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoScore Pro",
    page_icon="🚗",
    layout="wide"
)

# ─── CSS Corporativo ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 2rem;
    }

    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #0F1B2D;
        text-align: left;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        text-align: left;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-card .metric-label {
        color: #64748B;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        color: #0F1B2D;
    }
    .metric-card .metric-delta {
        font-size: 0.75rem;
        color: #10B981;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .score-excellent { color: #059669; }
    .score-bom { color: #0284C7; }
    .score-regular { color: #D97706; }
    .score-baixo { color: #EA580C; }
    .score-muito-baixo { color: #DC2626; }
    .recommendation-card {
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
    }
    .rec-excellent { background-color: #F0FDF4; border-left: 4px solid #059669; }
    .rec-bom { background-color: #F0F9FF; border-left: 4px solid #0284C7; }
    .rec-regular { background-color: #FFFBEB; border-left: 4px solid #D97706; }
    .rec-baixo { background-color: #FFF7ED; border-left: 4px solid #EA580C; }
    .rec-muito-baixo { background-color: #FEF2F2; border-left: 4px solid #DC2626; }
    .sidebar-brand {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .sidebar-brand h1 {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0F1B2D;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .sidebar-brand p {
        font-size: 0.75rem;
        color: #64748B;
        margin: 0.25rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    .step-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #0F1B2D;
    }
    .step-card strong {
        color: #0F1B2D;
        font-size: 0.95rem;
    }
    .step-card br + * {
        color: #475569;
        font-size: 0.875rem;
    }
    .finance-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
    }
    .finance-card h4 {
        color: #0F1B2D;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .finance-card p {
        margin: 0.4rem 0;
        font-size: 0.9rem;
        color: #334155;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F1B2D;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-success { background: #DCFCE7; color: #166534; }
    .badge-info { background: #DBEAFE; color: #1E40AF; }
    .badge-warning { background: #FEF3C7; color: #92400E; }
    .badge-danger { background: #FEE2E2; color: #991B1B; }
    .badge-orange { background: #FFEDD5; color: #9A3412; }

    /* Streamlit overrides */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
        color: #334155;
    }
    .stDivider {
        border-color: #E2E8F0;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        box-shadow: none;
    }
    .stButton > button[kind="primary"] {
        background-color: #0F1B2D;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.3px;
        padding: 0.6rem 1.5rem;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1E3A5F;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>AutoScore Pro</h1>
        <p>Financiamento Automotivo</p>
    </div>
    """, unsafe_allow_html=True)
    pagina = st.radio(
        "Navegação",
        ["🏠 Home", "📋 Simulação de Score", "📊 Análise de Score"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("© 2025 AutoScore Pro · v1.0")


# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 - HOME
# ═══════════════════════════════════════════════════════════════════════════════
if pagina == "🏠 Home":
    st.markdown('<p class="main-header">Simulador de Financiamento Automotivo</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Plataforma de análise de crédito para o setor automotivo</p>', unsafe_allow_html=True)

    # Métricas em cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Simulações Hoje</div>
            <div class="metric-value">47</div>
            <div class="metric-delta">↑ 12% vs. ontem</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Taxa de Aprovação</div>
            <div class="metric-value">73%</div>
            <div class="metric-delta">↑ 3pp vs. semana anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Score Médio</div>
            <div class="metric-value">712</div>
            <div class="metric-delta">↑ 8 pts vs. mês anterior</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Gráfico de simulações dos últimos 7 dias
    st.markdown('<p class="section-title">Simulações — Últimos 7 Dias</p>', unsafe_allow_html=True)

    dias = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(6, -1, -1)]
    simulacoes = [32, 45, 38, 51, 42, 47, 39]

    fig, ax = plt.subplots(figsize=(10, 3.5))
    bars = ax.bar(dias, simulacoes, color="#0F1B2D", width=0.5, zorder=3)
    for bar, val in zip(bars, simulacoes):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.8,
                str(val), ha='center', va='bottom', fontweight='600',
                fontsize=10, color="#0F1B2D")
    ax.set_xlabel("")
    ax.set_ylabel("Simulações", fontsize=9, color="#64748B")
    ax.set_ylim(0, max(simulacoes) + 10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E2E8F0')
    ax.spines['bottom'].set_color('#E2E8F0')
    ax.tick_params(colors='#64748B', labelsize=9)
    ax.yaxis.grid(True, linestyle='-', alpha=0.3, color='#E2E8F0', zorder=0)
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.divider()

    # Como funciona
    with st.expander("Como Funciona", expanded=True):
        st.markdown("""
        <div class="step-card">
            <strong>1. Coleta de Dados</strong><br>
            <span style="color:#475569; font-size:0.875rem;">
            Preencha as informações pessoais, financeiras e do veículo desejado pelo cliente no formulário de simulação.
            </span>
        </div>
        <div class="step-card">
            <strong>2. Análise de Score</strong><br>
            <span style="color:#475569; font-size:0.875rem;">
            O algoritmo avalia múltiplos fatores para gerar um score de 0 a 1000, indicando a probabilidade de aprovação.
            </span>
        </div>
        <div class="step-card">
            <strong>3. Recomendações</strong><br>
            <span style="color:#475569; font-size:0.875rem;">
            Com base no score, são geradas sugestões de condições de financiamento, taxas estimadas e orientações de melhoria.
            </span>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 - SIMULAÇÃO DE SCORE
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "📋 Simulação de Score":
    st.markdown('<p class="main-header">Simulação de Score</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Preencha os dados abaixo para calcular o score de crédito do cliente</p>', unsafe_allow_html=True)

    # Seção 1 - Dados Pessoais
    with st.expander("Dados Pessoais", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo", placeholder="Ex: João da Silva")
            cpf = st.text_input("CPF", placeholder="000.000.000-00")
        with col2:
            idade = st.number_input("Idade", min_value=18, max_value=80, value=30)
            estado_civil = st.selectbox("Estado Civil", ["Solteiro", "Casado", "Divorciado", "Viúvo"])

    # Seção 2 - Dados Financeiros
    with st.expander("Dados Financeiros", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            renda = st.number_input("Renda Mensal (R$)", min_value=0.0, value=5000.0, step=500.0, format="%.2f")
            tempo_emprego = st.number_input("Tempo de Emprego (meses)", min_value=0, value=24, step=1)
        with col2:
            casa_propria = st.checkbox("Possui Casa Própria")
            valor_entrada = st.number_input("Valor de Entrada Disponível (R$)", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")

    # Seção 3 - Dados do Veículo
    with st.expander("Dados do Veículo", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            valor_veiculo = st.number_input("Valor do Veículo (R$)", min_value=0.0, value=60000.0, step=5000.0, format="%.2f")
            tipo_veiculo = st.radio("Tipo de Veículo", ["Novo", "Usado"], horizontal=True)
        with col2:
            prazo = st.selectbox("Prazo Desejado (meses)", [12, 24, 36, 48, 60], index=2)
            marca = st.selectbox("Marca", ["Toyota", "Honda", "Volkswagen", "Fiat", "Chevrolet", "Hyundai", "Jeep", "Nissan"])

    st.divider()

    # Botão Calcular
    if st.button("Calcular Score", type="primary", use_container_width=True):
        # ─── Cálculo do Score ─────────────────────────────────────────────────
        score = 0

        # Fator Idade (max 150 pts)
        if 25 <= idade <= 55:
            score_idade = 150
        elif 21 <= idade < 25 or 55 < idade <= 65:
            score_idade = 100
        else:
            score_idade = 60
        score += score_idade

        # Fator Renda vs Parcela (max 250 pts)
        valor_financiado = valor_veiculo - valor_entrada
        parcela_estimada = valor_financiado / prazo if prazo > 0 else valor_financiado
        comprometimento = parcela_estimada / renda if renda > 0 else 1.0
        if comprometimento <= 0.2:
            score_renda = 250
        elif comprometimento <= 0.3:
            score_renda = 200
        elif comprometimento <= 0.4:
            score_renda = 130
        else:
            score_renda = 50
        score += score_renda

        # Fator Estabilidade/Tempo de Emprego (max 200 pts)
        if tempo_emprego >= 60:
            score_estabilidade = 200
        elif tempo_emprego >= 36:
            score_estabilidade = 160
        elif tempo_emprego >= 24:
            score_estabilidade = 120
        elif tempo_emprego >= 12:
            score_estabilidade = 80
        else:
            score_estabilidade = 40
        score += score_estabilidade

        # Fator Entrada (max 200 pts)
        percentual_entrada = valor_entrada / valor_veiculo if valor_veiculo > 0 else 0
        if percentual_entrada >= 0.4:
            score_entrada = 200
        elif percentual_entrada >= 0.3:
            score_entrada = 160
        elif percentual_entrada >= 0.2:
            score_entrada = 120
        elif percentual_entrada >= 0.1:
            score_entrada = 70
        else:
            score_entrada = 30
        score += score_entrada

        # Fator Perfil (max 200 pts)
        score_perfil = 80
        if casa_propria:
            score_perfil += 60
        if estado_civil == "Casado":
            score_perfil += 30
        elif estado_civil == "Solteiro":
            score_perfil += 10
        if tipo_veiculo == "Novo":
            score_perfil += 20
        else:
            score_perfil += 10
        score_perfil = min(score_perfil, 200)
        score += score_perfil

        # Garantir limites
        score = max(0, min(1000, score))

        # Classificação
        if score >= 800:
            faixa = "Excelente"
            cor = "#059669"
            classe_css = "rec-excellent"
            badge_class = "badge-success"
        elif score >= 650:
            faixa = "Bom"
            cor = "#0284C7"
            classe_css = "rec-bom"
            badge_class = "badge-info"
        elif score >= 500:
            faixa = "Regular"
            cor = "#D97706"
            classe_css = "rec-regular"
            badge_class = "badge-warning"
        elif score >= 300:
            faixa = "Baixo"
            cor = "#EA580C"
            classe_css = "rec-baixo"
            badge_class = "badge-orange"
        else:
            faixa = "Muito Baixo"
            cor = "#DC2626"
            classe_css = "rec-muito-baixo"
            badge_class = "badge-danger"

        # Salvar em session_state
        st.session_state["resultado"] = {
            "nome": nome,
            "cpf": cpf,
            "idade": idade,
            "estado_civil": estado_civil,
            "renda": renda,
            "tempo_emprego": tempo_emprego,
            "casa_propria": casa_propria,
            "valor_entrada": valor_entrada,
            "valor_veiculo": valor_veiculo,
            "tipo_veiculo": tipo_veiculo,
            "prazo": prazo,
            "marca": marca,
            "score": score,
            "faixa": faixa,
            "cor": cor,
            "score_idade": score_idade,
            "score_renda": score_renda,
            "score_estabilidade": score_estabilidade,
            "score_entrada": score_entrada,
            "score_perfil": score_perfil,
            "parcela_estimada": parcela_estimada,
            "comprometimento": comprometimento,
            "percentual_entrada": percentual_entrada,
        }

        # ─── Exibição do Resultado ────────────────────────────────────────────
        st.divider()
        st.markdown('<p class="section-title">Resultado da Análise</p>', unsafe_allow_html=True)

        col_score, col_gauge = st.columns([1, 2])

        with col_score:
            st.metric(label="Score do Cliente", value=f"{score} pts", delta=faixa)
            st.markdown(f"""
            <div class="recommendation-card {classe_css}">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <span style="font-size:1.5rem; font-weight:700; color:{cor};">{score}</span>
                    <span class="badge {badge_class}">{faixa}</span>
                </div>
                <p style="margin-top:0.5rem; font-size:0.85rem; color:#475569;">de 1000 pontos possíveis</p>
            </div>
            """, unsafe_allow_html=True)

        with col_gauge:
            # Gauge chart (semicírculo)
            fig, ax = plt.subplots(figsize=(6, 3.5), subplot_kw={'projection': 'polar'})

            ax.set_thetamin(0)
            ax.set_thetamax(180)

            # Fundo do gauge
            theta_bg = np.linspace(0, np.pi, 100)
            ax.fill_between(theta_bg, 0.6, 1.0, alpha=0.05, color='#64748B')

            # Faixas coloridas
            faixas_cores = [
                (0, 0.3, '#DC2626'),
                (0.3, 0.5, '#EA580C'),
                (0.5, 0.65, '#D97706'),
                (0.65, 0.8, '#0284C7'),
                (0.8, 1.0, '#059669'),
            ]
            for start, end, color in faixas_cores:
                theta_section = np.linspace(start * np.pi, end * np.pi, 50)
                ax.fill_between(theta_section, 0.6, 1.0, alpha=0.2, color=color)

            # Ponteiro
            angulo = (score / 1000) * np.pi
            ax.annotate('', xy=(angulo, 0.95), xytext=(angulo, 0.2),
                        arrowprops=dict(arrowstyle='->', color=cor, lw=2.5))

            # Texto central
            ax.text(np.pi/2, 0.25, f"{score}", ha='center', va='center',
                    fontsize=26, fontweight='bold', color=cor,
                    fontfamily='sans-serif')
            ax.text(np.pi/2, 0.05, faixa.upper(), ha='center', va='center',
                    fontsize=9, color='#64748B', fontweight='600',
                    fontfamily='sans-serif')

            # Labels
            ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
            ax.set_xticklabels(['0', '250', '500', '750', '1000'],
                             fontsize=8, color='#64748B')
            ax.set_yticks([])
            ax.set_ylim(0, 1.05)
            ax.spines['polar'].set_visible(False)
            ax.grid(False)
            fig.patch.set_facecolor('#FFFFFF')

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        # Recomendações
        st.divider()
        st.markdown('<p class="section-title">Recomendações</p>', unsafe_allow_html=True)

        if faixa == "Excelente":
            st.markdown("""
            <div class="recommendation-card rec-excellent">
                <strong>Score Excelente</strong><br>
                <span style="font-size:0.875rem; color:#334155;">
                Alta probabilidade de aprovação. Condições preferenciais disponíveis —
                prazo de até 60 meses com taxas a partir de 0,89% a.m.
                </span>
            </div>
            """, unsafe_allow_html=True)
        elif faixa == "Bom":
            st.markdown("""
            <div class="recommendation-card rec-bom">
                <strong>Score Bom</strong><br>
                <span style="font-size:0.875rem; color:#334155;">
                Boa probabilidade de aprovação com condições competitivas.
                Recomende entrada de pelo menos 20% para melhores taxas. Prazo sugerido: até 48 meses.
                </span>
            </div>
            """, unsafe_allow_html=True)
        elif faixa == "Regular":
            st.markdown("""
            <div class="recommendation-card rec-regular">
                <strong>Score Regular</strong><br>
                <span style="font-size:0.875rem; color:#334155;">
                Aprovação possível com condições moderadas. Sugestão: aumentar valor de entrada
                ou reduzir prazo. Considerar veículo de menor valor para otimizar comprometimento de renda.
                </span>
            </div>
            """, unsafe_allow_html=True)
        elif faixa == "Baixo":
            st.markdown("""
            <div class="recommendation-card rec-baixo">
                <strong>Score Baixo</strong><br>
                <span style="font-size:0.875rem; color:#334155;">
                Aprovação difícil nas condições atuais. Recomendações: entrada mínima de 30%,
                buscar avalista, ou considerar veículos de menor valor. Prazo máximo: 36 meses.
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="recommendation-card rec-muito-baixo">
                <strong>Score Muito Baixo</strong><br>
                <span style="font-size:0.875rem; color:#334155;">
                Aprovação improvável no momento. Orientar o cliente a quitar pendências,
                aguardar estabilidade de emprego, aumentar entrada (mínimo 40%), ou avaliar consórcio.
                </span>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 - ANÁLISE DE SCORE
# ═══════════════════════════════════════════════════════════════════════════════
elif pagina == "📊 Análise de Score":
    st.markdown('<p class="main-header">Análise Detalhada</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Decomposição dos fatores e condições de financiamento</p>', unsafe_allow_html=True)

    if "resultado" not in st.session_state:
        st.info("Nenhuma simulação realizada. Acesse **Simulação de Score** para calcular o score de um cliente.")
    else:
        res = st.session_state["resultado"]

        # Resumo em 2 colunas
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="finance-card">
                <h4>Dados do Cliente</h4>
                <p><strong>Nome:</strong> {res['nome'] or '—'}</p>
                <p><strong>Idade:</strong> {res['idade']} anos</p>
                <p><strong>Estado Civil:</strong> {res['estado_civil']}</p>
                <p><strong>Renda:</strong> R$ {res['renda']:,.2f}</p>
                <p><strong>Tempo de Emprego:</strong> {res['tempo_emprego']} meses</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="finance-card">
                <h4>Dados do Financiamento</h4>
                <p><strong>Veículo:</strong> {res['marca']} ({res['tipo_veiculo']})</p>
                <p><strong>Valor:</strong> R$ {res['valor_veiculo']:,.2f}</p>
                <p><strong>Entrada:</strong> R$ {res['valor_entrada']:,.2f} ({res['percentual_entrada']*100:.1f}%)</p>
                <p><strong>Prazo:</strong> {res['prazo']} meses</p>
                <p><strong>Score:</strong> <span style="color:{res['cor']}; font-weight:700; font-size:1.1rem;">{res['score']} — {res['faixa']}</span></p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Gráfico Radar
        st.markdown('<p class="section-title">Composição do Score</p>', unsafe_allow_html=True)

        col_radar, col_table = st.columns([1, 1])

        with col_radar:
            categorias = ['Renda', 'Estabilidade', 'Entrada', 'Perfil', 'Idade']
            valores_max = [250, 200, 200, 200, 150]
            valores = [
                res['score_renda'],
                res['score_estabilidade'],
                res['score_entrada'],
                res['score_perfil'],
                res['score_idade']
            ]
            valores_norm = [v / m for v, m in zip(valores, valores_max)]
            valores_norm.append(valores_norm[0])

            angles = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            angles.append(angles[0])

            fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
            ax.fill(angles, valores_norm, color='#0F1B2D', alpha=0.15)
            ax.plot(angles, valores_norm, color='#0F1B2D', linewidth=2, marker='o',
                    markersize=5, markerfacecolor='#0F1B2D')

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categorias, fontsize=10, fontweight='600', color='#334155')
            ax.set_ylim(0, 1)
            ax.set_yticks([0.25, 0.5, 0.75, 1.0])
            ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=7, color='#94A3B8')
            ax.grid(color='#E2E8F0', linestyle='-', linewidth=0.8)
            ax.spines['polar'].set_color('#E2E8F0')
            fig.patch.set_facecolor('#FFFFFF')

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col_table:
            st.markdown("**Breakdown por Categoria**")
            df_breakdown = pd.DataFrame({
                "Categoria": ['Renda', 'Estabilidade', 'Entrada', 'Perfil', 'Idade'],
                "Obtido": [res['score_renda'], res['score_estabilidade'], res['score_entrada'], res['score_perfil'], res['score_idade']],
                "Máximo": [250, 200, 200, 200, 150],
                "Aproveitamento": [
                    f"{res['score_renda']/250*100:.0f}%",
                    f"{res['score_estabilidade']/200*100:.0f}%",
                    f"{res['score_entrada']/200*100:.0f}%",
                    f"{res['score_perfil']/200*100:.0f}%",
                    f"{res['score_idade']/150*100:.0f}%",
                ]
            })
            st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

            total = res['score']
            st.markdown(f"""
            <div style="background:#F8FAFC; border-radius:8px; padding:1rem; margin-top:1rem;
                        text-align:center; border:1px solid #E2E8F0;">
                <span style="font-size:0.8rem; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;">Score Total</span><br>
                <span style="font-size:1.75rem; color:{res['cor']}; font-weight:700;">{total}</span>
                <span style="font-size:1rem; color:#94A3B8;"> / 1000</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Condições de Financiamento Sugeridas
        st.markdown('<p class="section-title">Condições de Financiamento Sugeridas</p>', unsafe_allow_html=True)

        # Calcular taxas baseadas no score
        if res['score'] >= 800:
            taxa_mensal = 0.0089
        elif res['score'] >= 650:
            taxa_mensal = 0.0129
        elif res['score'] >= 500:
            taxa_mensal = 0.0169
        elif res['score'] >= 300:
            taxa_mensal = 0.0219
        else:
            taxa_mensal = 0.0279

        valor_financiado = res['valor_veiculo'] - res['valor_entrada']
        if taxa_mensal > 0 and res['prazo'] > 0:
            parcela = valor_financiado * (taxa_mensal * (1 + taxa_mensal)**res['prazo']) / ((1 + taxa_mensal)**res['prazo'] - 1)
        else:
            parcela = valor_financiado / res['prazo'] if res['prazo'] > 0 else 0

        cet_mensal = taxa_mensal + 0.003
        cet_anual = (1 + cet_mensal)**12 - 1

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="finance-card" style="text-align:center;">
                <h4>Taxa de Juros</h4>
                <p style="font-size:1.6rem; color:#0F1B2D; font-weight:700; margin:0.5rem 0;">{taxa_mensal*100:.2f}% a.m.</p>
                <p style="color:#64748B; font-size:0.8rem; margin:0;">{((1+taxa_mensal)**12 - 1)*100:.1f}% a.a.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="finance-card" style="text-align:center;">
                <h4>Valor da Parcela</h4>
                <p style="font-size:1.6rem; color:#0F1B2D; font-weight:700; margin:0.5rem 0;">R$ {parcela:,.2f}</p>
                <p style="color:#64748B; font-size:0.8rem; margin:0;">{res['prazo']}x · Financiado: R$ {valor_financiado:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="finance-card" style="text-align:center;">
                <h4>CET Estimado</h4>
                <p style="font-size:1.6rem; color:#0F1B2D; font-weight:700; margin:0.5rem 0;">{cet_anual*100:.1f}% a.a.</p>
                <p style="color:#64748B; font-size:0.8rem; margin:0;">{cet_mensal*100:.2f}% a.m.</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Exportar Relatório
        st.markdown('<p class="section-title">Exportar Relatório</p>', unsafe_allow_html=True)

        relatorio = f"""
AUTOSCORE PRO — RELATÓRIO DE SIMULAÇÃO
{'—' * 60}

Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}

DADOS DO CLIENTE
Nome: {res['nome'] or '—'}
CPF: {res['cpf'] or '—'}
Idade: {res['idade']} anos
Estado Civil: {res['estado_civil']}
Renda Mensal: R$ {res['renda']:,.2f}
Tempo de Emprego: {res['tempo_emprego']} meses
Casa Própria: {'Sim' if res['casa_propria'] else 'Não'}

DADOS DO VEÍCULO
Marca: {res['marca']}
Tipo: {res['tipo_veiculo']}
Valor: R$ {res['valor_veiculo']:,.2f}
Entrada: R$ {res['valor_entrada']:,.2f} ({res['percentual_entrada']*100:.1f}%)
Prazo: {res['prazo']} meses

RESULTADO DA ANÁLISE
Score: {res['score']} / 1000
Classificação: {res['faixa']}

Decomposição:
  Renda:         {res['score_renda']:>3}/250  ({res['score_renda']/250*100:.0f}%)
  Estabilidade:  {res['score_estabilidade']:>3}/200  ({res['score_estabilidade']/200*100:.0f}%)
  Entrada:       {res['score_entrada']:>3}/200  ({res['score_entrada']/200*100:.0f}%)
  Perfil:        {res['score_perfil']:>3}/200  ({res['score_perfil']/200*100:.0f}%)
  Idade:         {res['score_idade']:>3}/150  ({res['score_idade']/150*100:.0f}%)

CONDIÇÕES SUGERIDAS
Taxa de Juros: {taxa_mensal*100:.2f}% a.m. ({((1+taxa_mensal)**12 - 1)*100:.1f}% a.a.)
Valor Financiado: R$ {valor_financiado:,.2f}
Parcela Estimada: R$ {parcela:,.2f}
CET Estimado: {cet_anual*100:.1f}% a.a.

{'—' * 60}
Documento gerado automaticamente por AutoScore Pro v1.0
"""

        st.download_button(
            label="Exportar Relatório (.txt)",
            data=relatorio,
            file_name=f"relatorio_autoscore_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
