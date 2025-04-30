import streamlit as st
import yfinance as yf
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from black_scholes import BlackScholes
from binomial_tree import BinomialTree
from monte_carlo import MonteCarlo

def get_last_price(ticker):
    try:
        data = yf.Ticker(ticker)
        last_price = data.history(period="1d")['Close'].iloc[-1]
        return round(last_price, 2)
    except:
        return -1

def calculate_T(maturity_date):
    today = datetime.datetime.today()
    maturity = datetime.datetime.strptime(maturity_date, "%Y-%m-%d")
    delta = maturity - today
    return max(delta.days / 365, 1/365)

st.set_page_config(page_title="Option Pricing App", page_icon="📈", layout="wide")
st.title("📈 Outil de Pricing d'Options")

st.sidebar.header("Paramètres")

method = st.sidebar.selectbox("Méthode de Pricing", ("Black-Scholes", "Binomial Tree", "Monte Carlo"))
type_option = st.sidebar.selectbox("Type d'Option", ("Européenne", "Américaine"))
ticker = st.sidebar.text_input("Ticker (ex: AAPL)", value="AAPL").upper()
spot_price = get_last_price(ticker)
if spot_price:
    st.sidebar.success(f"Prix spot actuel : {spot_price} USD")
else:
    st.sidebar.error("Impossible de récupérer le prix spot.")

K = st.sidebar.number_input("Strike (prix d'exercice)", value=spot_price if spot_price else 100.0)
maturity_date = st.sidebar.date_input("Échéance", value=datetime.date.today() + datetime.timedelta(days=90))
T = calculate_T(maturity_date.strftime("%Y-%m-%d"))
sigma = st.sidebar.number_input("Volatilite (ex: 0.2 pour 20%)", value=0.2, step=0.01)
r = st.sidebar.number_input("Taux sans risque (ex: 0.05 pour 5%)", value=0.05, step=0.01)

if method == "Black-Scholes":
    if type_option == "Américaine":
        st.warning("Black-Scholes ne supporte que les options européennes. Pricing en européen forcé.")
    model_call = BlackScholes(S=spot_price, K=K, T=T, r=r, sigma=sigma, option_type="call")
    model_put = BlackScholes(S=spot_price, K=K, T=T, r=r, sigma=sigma, option_type="put")
elif method == "Binomial Tree":
    model_call = BinomialTree(S=spot_price, K=K, T=T, r=r, sigma=sigma, N=100, option_type="call", american=(type_option=="Américaine"))
    model_put = BinomialTree(S=spot_price, K=K, T=T, r=r, sigma=sigma, N=100, option_type="put", american=(type_option=="Américaine"))
elif method == "Monte Carlo":
    if type_option == "Américaine":
        st.warning("Monte Carlo standard ne supporte que les options européennes. Pricing en européen forcé.")
    model_call = MonteCarlo(S=spot_price, K=K, T=T, r=r, sigma=sigma, simulations=100000, option_type="call")
    model_put = MonteCarlo(S=spot_price, K=K, T=T, r=r, sigma=sigma, simulations=100000, option_type="put")

# --- Cartes Stylées pour Prix ---
st.markdown("""
<style>
.card {
    padding: 1rem;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
}
.card-blue {
    background-color: #007BFF;
}
.card-green {
    background-color: #28A745;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class='card card-blue'>
        Prix Call : {model_call.price():.4f} USD
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card card-green'>
        Prix Put : {model_put.price():.4f} USD
    </div>
    """, unsafe_allow_html=True)

# --- Tableau des Greeks ---

greeks_data = {
    "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
    "Call": [
        round(model_call.delta(), 4),
        round(model_call.gamma(), 6),
        round(model_call.vega(), 4),
        round(model_call.theta(), 4),
        round(model_call.rho(), 4),
    ],
    "Put": [
        round(model_put.delta(), 4),
        round(model_put.gamma(), 6),
        round(model_put.vega(), 4),
        round(model_put.theta(), 4),
        round(model_put.rho(), 4),
    ]
}

df_greeks = pd.DataFrame(greeks_data)
st.subheader("Greeks")
st.table(df_greeks.set_index("Greek"))

# --- Graphiques interactifs avec Plotly ---

st.subheader("📊 Evolution Prix et Greeks selon le Spot")

S_range = np.linspace(0.5 * spot_price, 1.5 * spot_price, 50)
prices_call, prices_put, deltas, gammas, vegas, thetas, rhos = [], [], [], [], [], [], []

for S in S_range:
    if method == "Black-Scholes":
        temp_call = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma, option_type="call")
        temp_put = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma, option_type="put")
    elif method == "Binomial Tree":
        temp_call = BinomialTree(S=S, K=K, T=T, r=r, sigma=sigma, N=100, option_type="call", american=(type_option=="Américaine"))
        temp_put = BinomialTree(S=S, K=K, T=T, r=r, sigma=sigma, N=100, option_type="put", american=(type_option=="Américaine"))
    else:
        temp_call = MonteCarlo(S=S, K=K, T=T, r=r, sigma=sigma, simulations=3000, option_type="call")
        temp_put = MonteCarlo(S=S, K=K, T=T, r=r, sigma=sigma, simulations=3000, option_type="put")

    prices_call.append(temp_call.price())
    prices_put.append(temp_put.price())
    deltas.append(temp_call.delta())
    gammas.append(temp_call.gamma())
    vegas.append(temp_call.vega())
    thetas.append(temp_call.theta())
    rhos.append(temp_call.rho())

fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=S_range, y=prices_call, mode='lines', name='Call Price'))
fig_price.add_trace(go.Scatter(x=S_range, y=prices_put, mode='lines', name='Put Price'))
fig_price.update_layout(title="Évolution des prix des options", xaxis_title="Prix Spot", yaxis_title="Prix de l'option")
st.plotly_chart(fig_price, use_container_width=True)

fig_greeks = go.Figure()
fig_greeks.add_trace(go.Scatter(x=S_range, y=deltas, mode='lines', name='Delta'))
fig_greeks.add_trace(go.Scatter(x=S_range, y=gammas, mode='lines', name='Gamma'))
fig_greeks.add_trace(go.Scatter(x=S_range, y=vegas, mode='lines', name='Vega'))
fig_greeks.add_trace(go.Scatter(x=S_range, y=thetas, mode='lines', name='Theta'))
fig_greeks.add_trace(go.Scatter(x=S_range, y=rhos, mode='lines', name='Rho'))
fig_greeks.update_layout(title="Greeks selon le prix spot", xaxis_title="Prix Spot", yaxis_title="Valeur")
st.plotly_chart(fig_greeks, use_container_width=True)



# Pied de page
st.markdown("---")
st.caption("📌 Développé avec ❤️ par Rayen & Eliasy | Modèles Black-Scholes/CRR/Monte-Carlo pour le pricing des options")
