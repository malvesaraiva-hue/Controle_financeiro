import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Controle Financeiro — Início", page_icon="💸", layout="wide")


def load_sample_data():
    """Gera dados de exemplo para a página inicial."""
    hoje = datetime.today().date()
    dates = [hoje - timedelta(days=i) for i in range(90)]
    categories = ["Salário", "Alimentação", "Transporte", "Lazer", "Investimentos", "Outros"]
    rng = np.random.default_rng(42)

    data = []
    for d in dates:
        # simula 0-3 transações por dia
        for _ in range(rng.integers(0, 3)):
            cat = rng.choice(categories, p=[0.15, 0.25, 0.15, 0.15, 0.15, 0.15])
            amount = float(round(rng.normal(200 if cat == "Salário" else -50, 120), 2))
            # garantir valores plausíveis
            if cat == "Salário":
                amount = abs(amount) + 1000
            else:
                amount = -abs(amount)
            data.append({"date": d, "category": cat, "amount": amount, "description": f"Exemplo: {cat}"})

    df = pd.DataFrame(data).sort_values("date", ascending=False).reset_index(drop=True)
    return df


def resumo_mensal(df):
    df_month = df.copy()
    df_month["month"] = df_month["date"].apply(lambda d: d.replace(day=1))
    summary = df_month.groupby("month")["amount"].sum().sort_index()
    return summary


def indicadores(df):
    total_in = df[df["amount"] > 0]["amount"].sum()
    total_out = -df[df["amount"] < 0]["amount"].sum()
    balance = total_in - total_out
    return total_in, total_out, balance


def pagina_inicio(df):
    st.header("Bem-vindo ao Controle Financeiro")
    st.write("Visão geral rápida das suas finanças. Use a barra lateral para navegar entre telas.")

    # indicadores principais
    in_, out_, bal = indicadores(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Entradas (Últimos 90 dias)", f"R$ {in_:,.2f}")
    c2.metric("Saídas (Últimos 90 dias)", f"R$ {out_:,.2f}")
    c3.metric("Saldo (Últimos 90 dias)", f"R$ {bal:,.2f}", delta=f"R$ {in_ - out_:,.2f}")

    st.markdown("---")

    # gráficos
    st.subheader("Tendência mensal")
    summary = resumo_mensal(df)
    # transformar para DataFrame para os gráficos do streamlit
    df_summary = summary.reset_index().rename(columns={"month": "Mês", "amount": "Saldo"})
    df_summary["Mês"] = df_summary["Mês"].dt.strftime("%Y-%m")
    st.line_chart(df_summary.set_index("Mês")["Saldo"])

    st.subheader("Despesas por categoria (10 últimas transações)")
    cat_summary = (
        df[df["amount"] < 0].groupby("category")["amount"].sum().abs().sort_values(ascending=False)
    )
    if not cat_summary.empty:
        st.bar_chart(cat_summary)
    else:
        st.info("Sem despesas para mostrar por categoria.")

    st.markdown("---")

    # transações recentes
    st.subheader("Transações recentes")
    st.dataframe(df.head(10), use_container_width=True)

    # ações rápidas
    st.markdown("")
    col_a, col_b, _ = st.columns([1, 1, 2])
    if col_a.button("➕ Adicionar transação"):
        st.info("Abra a tela de 'Transações' na barra lateral para adicionar.")
    if col_b.button("📥 Importar CSV"):
        st.info("Funcionalidade de importação ainda não implementada (exemplo).")

    st.markdown("---")
    st.caption("Página inicial gerada automaticamente — altere os dados de exemplo em load_sample_data() para conectar ao seu backend.")


def main():
    # carregar dados (substituir pela fonte real em produção)
    df = load_sample_data()

    # sidebar / navegação
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para", ["Início", "Transações", "Relatórios", "Configurações"])

    if page == "Início":
        pagina_inicio(df)
    elif page == "Transações":
        st.header("Transações")
        st.write("Aqui você pode visualizar, filtrar e adicionar transações.")
        # filtros simples
        cat = st.multiselect("Categoria", options=sorted(df["category"].unique()), default=None)
        if cat:
            st.dataframe(df[df["category"].isin(cat)].reset_index(drop=True), use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    elif page == "Relatórios":
        st.header("Relatórios")
        st.write("Relatórios e gráficos detalhados serão implementados aqui.")
    else:
        st.header("Configurações")
        st.write("Preferências do usuário e integração com contas bancárias.")

if __name__ == "__main__":
    main()