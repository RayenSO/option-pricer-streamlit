import math
import datetime
import yfinance as yf

from black_scholes import BlackScholes
from binomial_tree import BinomialTree
from monte_carlo import MonteCarlo

def get_last_price(ticker):
    data = yf.Ticker(ticker)
    last_price = data.history(period="1d")['Close'].iloc[-1]
    return last_price

def calculate_T(maturity_date):
    today = datetime.datetime.today()
    maturity = datetime.datetime.strptime(maturity_date, "%Y-%m-%d")
    delta = maturity - today
    return max(delta.days / 365, 1/365)  # Pour éviter T=0

def main():
    # --- Inputs utilisateur ---
    ticker = input("Entrez le ticker (ex: AAPL, MSFT) : ").upper()
    K = float(input("Entrez le prix d'exercice (strike) : "))
    maturity_date = input("Entrez la date d'échéance (format YYYY-MM-DD) : ")
    option_type = input("Call ou Put ? (call/put) : ").lower()
    r = float(input("Entrez le taux sans risque (ex: 0.05 pour 5%) : "))
    sigma = float(input("Entrez la volatilité (ex: 0.2 pour 20%) : "))

    # --- Données calculées ---
    S = get_last_price(ticker)
    T = calculate_T(maturity_date)

    print("\n--- Données récupérées ---")
    print(f"Ticker : {ticker}")
    print(f"Spot : {S:.2f}")
    print(f"Strike : {K:.2f}")
    print(f"Maturité (T en années) : {T:.4f}")
    print(f"Taux sans risque : {r}")
    print(f"Volatilité : {sigma}")
    print(f"Type d'option : {option_type}")

    # --- Modèles ---
    bs = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type)
    bt = BinomialTree(S=S, K=K, T=T, r=r, sigma=sigma, N=100, option_type=option_type, american=False)
    mc = MonteCarlo(S=S, K=K, T=T, r=r, sigma=sigma, simulations=100000, option_type=option_type)

    # --- Résultats ---
    print("\n--- Résultats ---")
    print("\nBlack-Scholes :")
    print(f"  Price : {bs.price():.4f}")
    print(f"  Delta : {bs.delta():.4f}")
    print(f"  Gamma : {bs.gamma():.6f}")
    print(f"  Vega  : {bs.vega():.4f}")
    print(f"  Theta : {bs.theta():.4f}")
    print(f"  Rho   : {bs.rho():.4f}")

    print("\nBinomial Tree :")
    print(f"  Price : {bt.price():.4f}")
    print(f"  Delta : {bt.delta():.4f}")
    print(f"  Gamma : {bt.gamma():.6f}")
    print(f"  Vega  : {bt.vega():.4f}")
    print(f"  Theta : {bt.theta():.4f}")
    print(f"  Rho   : {bt.rho():.4f}")

    print("\nMonte Carlo :")
    print(f"  Price : {mc.price():.4f}")
    print(f"  Delta : {mc.delta():.4f}")
    print(f"  Gamma : {mc.gamma():.6f}")
    print(f"  Vega  : {mc.vega():.4f}")
    print(f"  Theta : {mc.theta():.4f}")
    print(f"  Rho   : {mc.rho():.4f}")

if __name__ == "__main__":
    main()
