import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Tarifa Progressiva de Água", layout="wide")

# Logo e título
st.title("💧 Simulador de Tarifa Progressiva de Água")
st.markdown("""
Este aplicativo simula os efeitos de tarifas progressivas em três setores de uso da água: **urbano**, **irrigação** e **indústria**.
Ajuste os parâmetros e avalie a nova demanda, a receita gerada e o impacto da política tarifária.
""")

# Entradas
st.sidebar.header("⚙️ Parâmetros de Entrada")

setores = ["Urbano", "Irrigação", "Indústria"]
demanda_inicial = [1000, 2000, 1500]

tarifas = []
elasticidades = []

for i, setor in enumerate(setores):
    st.sidebar.subheader(f"🔹 {setor}")
    tarifa = st.sidebar.number_input(f"Tarifa base ({setor}) [R$/m³]", min_value=0.1, value=1.0 + i * 0.5, step=0.1, key=f"tarifa_{setor}")
    e = st.sidebar.number_input(f"Elasticidade-preço ({setor})", value=-0.2 - 0.1*i, step=0.05, key=f"elast_{setor}")
    tarifas.append(tarifa)
    elasticidades.append(e)

fator_prog = st.sidebar.slider("📈 Fator de Tarifa Progressiva", 1.0, 2.0, 1.25, step=0.05)

# Cálculos
nova_tarifa = [t * fator_prog for t in tarifas]
variacao_preco = [(nt - tb)/tb for nt, tb in zip(nova_tarifa, tarifas)]
nova_demanda = [d * (1 + e * vp) for d, e, vp in zip(demanda_inicial, elasticidades, variacao_preco)]
receita_inicial = [d * t for d, t in zip(demanda_inicial, tarifas)]
receita_final = [nd * nt for nd, nt in zip(nova_demanda, nova_tarifa)]
reducao = [d - nd for d, nd in zip(demanda_inicial, nova_demanda)]

# Tabela de resultados
df = pd.DataFrame({
    "Setor": setores,
    "Demanda Inicial (m³)": demanda_inicial,
    "Tarifa Base (R$)": tarifas,
    "Nova Tarifa (R$)": [round(t, 2) for t in nova_tarifa],
    "Elasticidade": elasticidades,
    "Nova Demanda (m³)": [round(d, 1) for d in nova_demanda],
    "Redução no Consumo (m³)": [round(r, 1) for r in reducao],
    "Receita Inicial (R$)": [round(r, 2) for r in receita_inicial],
    "Receita Final (R$)": [round(r, 2) for r in receita_final]
})

st.subheader("📊 Resultados da Simulação")
st.dataframe(df, use_container_width=True)

# Gráfico de barras
st.subheader("📈 Comparativo de Consumo por Setor")
fig, ax = plt.subplots()
x = range(len(setores))
ax.bar(x, demanda_inicial, label="Inicial", alpha=0.6)
ax.bar(x, nova_demanda, label="Com tarifa progressiva", alpha=0.6)
ax.set_xticks(x)
ax.set_xticklabels(setores)
ax.set_ylabel("Demanda (m³)")
ax.legend()
st.pyplot(fig)
