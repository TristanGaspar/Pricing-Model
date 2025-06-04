import numpy as np
from scipy.stats import norm

def black_scholes_price(S,K,T,r,vol,option_type='call'):
   
    """Calcule le prix d'une option européenne avec le modèle Black-Scholes.
    S : prix spot de l'actif
    K : prix d'exercice
    T : temps jusqu'à l'échéance (en années)
    r : taux sans risque
    vol: volatilité de l'actif
    option_type : 'call' ou 'put'"""

    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'")

    return price

def black_scholes_greeks(S, K, T, r, vol, option_type='call'):
   
    """Calcule les Greeks d'une option européenne avec Black-Scholes.
    Retourne Delta, Gamma, Vega, Theta, Rho."""

    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    delta = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * vol * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # Vega exprimé en pourcentage
    theta = (-S * norm.pdf(d1) * vol / (2 * np.sqrt(T))
             - r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'call' else -d2)) / 365
    rho = K * T * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'call' else -norm.cdf(-d2)) / 100

    return delta, gamma, vega, theta, rho

   
if __name__ == "__main__":
    S = 100
    K = 105
    T = 0.5
    r = 0.02
    vol = 0.25

    price = black_scholes_price(S, K, T, r, vol, option_type='call')
    print("Prix de l'option CALL : " + str(round(price, 2)) + " euros")

    delta, gamma, vega, theta, rho = black_scholes_greeks(S, K, T, r, vol, option_type='call')
    print("Delta : " + str(round(delta, 4)))
    print("Gamma : " + str(round(gamma, 4)))
    print("Vega : " + str(round(vega, 4)))
    print("Theta : " + str(round(theta, 4)))
    print("Rho : " + str(round(rho, 4)))

    