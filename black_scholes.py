import math
from scipy.stats import norm

class BlackScholes:
    def __init__(self, S, K, T, r, sigma, option_type="call"):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
        
        self.d1 = (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * math.sqrt(self.T)
        
    def price(self):
        if self.option_type == "call":
            return self.S * norm.cdf(self.d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif self.option_type == "put":
            return self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def delta(self):
        if self.option_type == "call":
            return norm.cdf(self.d1)
        elif self.option_type == "put":
            return norm.cdf(self.d1) - 1
    
    def gamma(self):
        return norm.pdf(self.d1) / (self.S * self.sigma * math.sqrt(self.T))
    
    def vega(self):
        return (self.S * norm.pdf(self.d1) * math.sqrt(self.T)) / 100  # Vega normalisé directement (par 1% de vol)
    
    def theta(self):
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * math.sqrt(self.T))
        if self.option_type == "call":
            term2 = -self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
            theta_annual = term1 + term2
        elif self.option_type == "put":
            term2 = self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2)
            theta_annual = term1 + term2
        
        return theta_annual / 365  # Theta normalisé directement (par jour)
    
    def rho(self):
        if self.option_type == "call":
            return self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(self.d2)/100
        elif self.option_type == "put":
            return -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-self.d2)/100

# Utilisation
bs = BlackScholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call")

print(f"Price: {bs.price():.4f}")
print(f"Delta: {bs.delta():.4f}")
print(f"Gamma: {bs.gamma():.4f}")
print(f"Vega: {bs.vega():.4f}")
print(f"Theta: {bs.theta():.4f}")
print(f"Rho: {bs.rho():.4f}")
