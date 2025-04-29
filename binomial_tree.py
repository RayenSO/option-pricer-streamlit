import math

class BinomialTree:
    def __init__(self, S, K, T, r, sigma, N, option_type="call", american=False):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.option_type = option_type.lower()
        self.american = american

        self.dt = T / N
        self.u = math.exp(sigma * math.sqrt(self.dt))
        self.d = 1 / self.u
        self.p = (math.exp(r * self.dt) - self.d) / (self.u - self.d)
        self.discount = math.exp(-r * self.dt)

    def price(self):
        asset_prices = [self.S * (self.u ** j) * (self.d ** (self.N - j)) for j in range(self.N + 1)]
        
        if self.option_type == "call":
            option_values = [max(price - self.K, 0) for price in asset_prices]
        elif self.option_type == "put":
            option_values = [max(self.K - price, 0) for price in asset_prices]
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        for i in range(self.N - 1, -1, -1):
            option_values = [
                self.discount * (self.p * option_values[j+1] + (1 - self.p) * option_values[j])
                for j in range(i + 1)
            ]
            if self.american:
                asset_prices = [self.S * (self.u ** j) * (self.d ** (i - j)) for j in range(i + 1)]
                if self.option_type == "call":
                    option_values = [max(option_values[j], asset_prices[j] - self.K) for j in range(i + 1)]
                else:
                    option_values = [max(option_values[j], self.K - asset_prices[j]) for j in range(i + 1)]

        return option_values[0]

    def delta(self):
        S_up = self.S * self.u
        S_down = self.S * self.d

        if self.option_type == "call":
            payoff_up = max(S_up - self.K, 0)
            payoff_down = max(S_down - self.K, 0)
        else:
            payoff_up = max(self.K - S_up, 0)
            payoff_down = max(self.K - S_down, 0)

        return (payoff_up - payoff_down) / (S_up - S_down)

    def gamma(self):
        S_upup = self.S * self.u * self.u
        S_updown = self.S * self.u * self.d
        S_downdown = self.S * self.d * self.d

        if self.option_type == "call":
            payoff_upup = max(S_upup - self.K, 0)
            payoff_updown = max(S_updown - self.K, 0)
            payoff_downdown = max(S_downdown - self.K, 0)
        else:
            payoff_upup = max(self.K - S_upup, 0)
            payoff_updown = max(self.K - S_updown, 0)
            payoff_downdown = max(self.K - S_downdown, 0)

        delta_up = (payoff_upup - payoff_updown) / (self.S * (self.u - self.d))
        delta_down = (payoff_updown - payoff_downdown) / (self.S * (self.u - self.d))

        return (delta_up - delta_down) / (0.5 * (S_upup - S_downdown))

    def theta(self):
        bt_now = self.price()
        bt_future = BinomialTree(S=self.S, K=self.K, T=self.T - 2*self.dt, r=self.r, sigma=self.sigma, N=self.N-2, option_type=self.option_type, american=self.american)
        bt_future_price = bt_future.price()
        theta_annual = (bt_future_price - bt_now) / (2 * self.dt)
        return theta_annual / 365  # normalisé par jour

    def vega(self):
        epsilon = 0.01  # 1% de volatilité
        bt_plus = BinomialTree(S=self.S, K=self.K, T=self.T, r=self.r, sigma=self.sigma + epsilon, N=self.N, option_type=self.option_type, american=self.american)
        bt_minus = BinomialTree(S=self.S, K=self.K, T=self.T, r=self.r, sigma=self.sigma - epsilon, N=self.N, option_type=self.option_type, american=self.american)

        vega_raw = (bt_plus.price() - bt_minus.price()) / (2 * epsilon)
        return vega_raw / 100  # normalisé par 1% de volatilité

    def rho(self):
        epsilon = 0.01  # 1% de taux
        bt_plus = BinomialTree(S=self.S, K=self.K, T=self.T, r=self.r + epsilon, sigma=self.sigma, N=self.N, option_type=self.option_type, american=self.american)
        bt_minus = BinomialTree(S=self.S, K=self.K, T=self.T, r=self.r - epsilon, sigma=self.sigma, N=self.N, option_type=self.option_type, american=self.american)

        rho_raw = (bt_plus.price() - bt_minus.price()) / (2 * epsilon)
        return rho_raw / 100  # normalisé par 1% de taux


# Option PUT Européenne
bt_european = BinomialTree(S=36, K=40, T=1, r=0.06, sigma=0.2, N=100, option_type="put", american=False)
price_european = bt_european.price()

# Option PUT Américaine
bt_american = BinomialTree(S=36, K=40, T=1, r=0.06, sigma=0.2, N=100, option_type="put", american=True)
price_american = bt_american.price()

print(f"Prix Put Européen : {price_european:.4f}")
print(f"Prix Put Américain : {price_american:.4f}")
