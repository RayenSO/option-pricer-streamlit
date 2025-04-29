import math
import datetime
import yfinance as yf

from black_scholes import BlackScholes
from binomial_tree import BinomialTree
from monte_carlo import MonteCarlo

def get_last_price(ticker):
    try:
        data = yf.Ticker(ticker)
        last_price = data.history(period="1d")['Close'].iloc[-1]
        return round(last_price, 2)
    except Exception as e:
        print(f"Erreur lors de la récupération du prix : {e}")
        return None

def calculate_T(maturity_date):
    try:
        today = datetime.datetime.today()
        maturity = datetime.datetime.strptime(maturity_date, "%Y-%m-%d")
        delta = maturity - today
        return max(delta.days / 365, 1/365)
    except ValueError:
        return None

def get_available_strikes(ticker, maturity_date):
    try:
        options = yf.Ticker(ticker).option_chain(maturity_date)
        return sorted(list(set(options.calls['strike'].tolist())))
    except Exception:
        return []

def ask_ticker():
    while True:
        ticker = input("Entrez le ticker (ex: AAPL, MSFT) : ").upper()
        price = get_last_price(ticker)
        if price:
            print(f"Prix spot récupéré : {price}")
            return ticker, price
        else:
            print("❌ Ticker invalide ou problème réseau. Réessayez.")

def ask_maturity_date(ticker):
    while True:
        date_str = input("Entrez la date d'échéance (format YYYY-MM-DD) : ")
        T = calculate_T(date_str)
        if T:
            strikes = get_available_strikes(ticker, date_str)
            if strikes:
                print(f"Strikes disponibles à cette date : {strikes[:10]}...")
            else:
                print("⚠️ Impossible de récupérer la chaîne d'options (strikes indisponibles).")
            return date_str, T
        else:
            print("❌ Format de date incorrect. Essayez : YYYY-MM-DD.")

def ask_option_type():
    while True:
        t = input("Type d'option ? (call/put) : ").lower()
        if t in ["call", "put"]:
            return t
        print("❌ Réponse invalide. Tapez 'call' ou 'put'.")

def ask_float(prompt, default=None):
    val = input(prompt)
    if val == "" and default is not None:
        print(f"--> [Valeur par défaut utilisée : {default}]")
        return default
    try:
        return float(val)
    except ValueError:
        print("❌ Entrée invalide.")
        return ask_float(prompt, default)

def main():
    print("📈 Outil de pricing d'options (Black-Scholes, Binomial, Monte Carlo)")

    # --- INPUT UTILISATEUR ---
    ticker, S = ask_ticker()
    K = ask_float("Entrez le prix d'exercice (strike) : ")
    maturity_date, T = ask_maturity_date(ticker)
    option_type = ask_option_type()
    r = ask_float("Entrez le taux sans risque (ex: 0.05 pour 5%) [Entrée pour 0.05] : ", default=0.05)
    sigma = ask_float("Entrez la volatilité (ex: 0.2 pour 20%) [Entrée pour 0.2] : ", default=0.2)

    # --- OBJETS MODELES ---
    bs = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type)
    bt = BinomialTree(S=S, K=K, T=T, r=r, sigma=sigma, N=100, option_type=option_type, american=False)
    mc = MonteCarlo(S=S, K=K, T=T, r=r, sigma=sigma, simulations=100000, option_type=option_type)

    # --- AFFICHAGE DES RÉSULTATS ---
    print("\n🧠 Résumé des paramètres")
    print(f"Ticker : {ticker}")
    print(f"Spot : {S}")
    print(f"Strike : {K}")
    print(f"Échéance : {maturity_date} | T = {T:.4f} ans")
    print(f"Taux sans risque : {r}")
    print(f"Volatilité : {sigma}")
    print(f"Type : {option_type}")

    print("\n🔍 Résultats (tous les modèles)\n")

    for name, model in [("Black-Scholes", bs), ("Binomial Tree", bt), ("Monte Carlo", mc)]:
        print(f"--- {name} ---")
        print(f"  Prix   : {model.price():.4f}")
        print(f"  Delta  : {model.delta():.4f}")
        print(f"  Gamma  : {model.gamma():.6f}")
        print(f"  Vega   : {model.vega():.4f}")
        print(f"  Theta  : {model.theta():.4f}")
        print(f"  Rho    : {model.rho():.4f}")
        print()

if __name__ == "__main__":
    main()
