import math
import numpy as np

class MonteCarlo:
    def __init__(self, S, K, T, r, sigma, simulations=10000, option_type="call"):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.simulations = simulations
        self.option_type = option_type.lower()

    def simulate_ST(self):
        Z = np.random.standard_normal(self.simulations)
        ST = self.S * np.exp((self.r - 0.5 * self.sigma**2) * self.T + self.sigma * math.sqrt(self.T) * Z)
        return ST

    def price(self):
        ST = self.simulate_ST()
        if self.option_type == "call":
            payoffs = np.maximum(ST - self.K, 0)
        elif self.option_type == "put":
            payoffs = np.maximum(self.K - ST, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        return math.exp(-self.r * self.T) * np.mean(payoffs)

    def delta(self):
        bump = 0.01 * self.S  # Petit déplacement de 1%
        S_up = self.S + bump
        S_down = self.S - bump

        mc_up = MonteCarlo(S=S_up, K=self.K, T=self.T, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)
        mc_down = MonteCarlo(S=S_down, K=self.K, T=self.T, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)

        price_up = mc_up.price()
        price_down = mc_down.price()

        return (price_up - price_down) / (2 * bump)

    def gamma(self):
        bump = 0.01 * self.S
        S_up = self.S + bump
        S_down = self.S - bump

        mc_up = MonteCarlo(S=S_up, K=self.K, T=self.T, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)
        mc_down = MonteCarlo(S=S_down, K=self.K, T=self.T, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)
        mc_mid = MonteCarlo(S=self.S, K=self.K, T=self.T, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)

        price_up = mc_up.price()
        price_mid = mc_mid.price()
        price_down = mc_down.price()

        return (price_up - 2 * price_mid + price_down) / (bump ** 2)

    def vega(self):
        bump = 0.01  # +1% de volatilité
        sigma_up = self.sigma + bump
        sigma_down = self.sigma - bump

        mc_up = MonteCarlo(S=self.S, K=self.K, T=self.T, r=self.r, sigma=sigma_up, simulations=self.simulations, option_type=self.option_type)
        mc_down = MonteCarlo(S=self.S, K=self.K, T=self.T, r=self.r, sigma=sigma_down, simulations=self.simulations, option_type=self.option_type)

        price_up = mc_up.price()
        price_down = mc_down.price()

        vega_raw = (price_up - price_down) / (2 * bump)
        return vega_raw / 100  # Normalisé par 1% de volatilité

    def theta(self):
        epsilon = 1/365  # 1 jour en années
        T_minus = self.T - epsilon
        if T_minus <= 0:
            T_minus = 1/365  # éviter T=0

        mc_minus = MonteCarlo(S=self.S, K=self.K, T=T_minus, r=self.r, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)
        price_now = self.price()
        price_minus = mc_minus.price()

        theta_annual = (price_minus - price_now) / epsilon
        return theta_annual / 365  # Normalisé par jour

    def rho(self):
        bump = 0.01  # +1% taux sans risque
        r_up = self.r + bump
        r_down = self.r - bump

        mc_up = MonteCarlo(S=self.S, K=self.K, T=self.T, r=r_up, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)
        mc_down = MonteCarlo(S=self.S, K=self.K, T=self.T, r=r_down, sigma=self.sigma, simulations=self.simulations, option_type=self.option_type)

        price_up = mc_up.price()
        price_down = mc_down.price()

        rho_raw = (price_up - price_down) / (2 * bump)
        return rho_raw / 100  # Normalisé par 1% de taux

mc = MonteCarlo(S=100, K=100, T=1, r=0.05, sigma=0.2, simulations=100000, option_type="call")

print(f"Price: {mc.price():.4f}")
print(f"Delta: {mc.delta():.4f}")
print(f"Gamma: {mc.gamma():.6f}")
print(f"Vega: {mc.vega():.4f}")
print(f"Theta: {mc.theta():.4f}")
print(f"Rho: {mc.rho():.4f}")
