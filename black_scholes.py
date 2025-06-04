"""
black_scholes.py
----------------
Modèle de pricing pour options européennes avec la formule de Black-Scholes.

Fonctionnalités :
- Calcul du prix (call/put)
- Calcul des Greeks (Delta, Gamma, Vega, Theta, Rho)
- Estimation de la volatilité implicite (méthode de Newton-Raphson)
"""

import numpy as np
from scipy.stats import norm

def black_scholes_price(S, K, T, r, vol, option_type='call'):
    """
    Prix théorique d'une option européenne avec Black-Scholes.
    """
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'.")

def black_scholes_greeks(S, K, T, r, vol, option_type='call'):
    """
    Calcul des principaux Greeks : Delta, Gamma, Vega, Theta, Rho.
    """
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    delta = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * vol * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # variation du prix pour 1% de vol
    theta = (-S * norm.pdf(d1) * vol / (2 * np.sqrt(T)) -
             r * K * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'call' else norm.cdf(-d2))) / 365
    rho = (K * T * np.exp(-r * T) * norm.cdf(d2) / 100) if option_type == 'call' \
          else (-K * T * np.exp(-r * T) * norm.cdf(-d2) / 100)

    return delta, gamma, vega, theta, rho

def implied_volatility(S, K, T, r, market_price, option_type='call', tol=1e-5, max_iter=100):
    """
    Estimation de la volatilité implicite à partir d'un prix de marché.
    Méthode : Newton-Raphson avec dérivée Vega.
    """
    vol = 0.2  # estimation initiale

    for i in range(max_iter):
        price = black_scholes_price(S, K, T, r, vol, option_type)
        vega = black_scholes_greeks(S, K, T, r, vol, option_type)[2] * 100

        if vega == 0:
            break

        diff = price - market_price
        if abs(diff) < tol:
            return round(vol, 6)

        vol -= diff / vega

    raise ValueError("Échec de convergence de la volatilité implicite.")

if __name__ == "__main__":
    S = 100
    K = 105
    T = 0.5
    r = 0.02
    vol = 0.25
    option_type = 'call'

    # Affichage du prix et des Greeks
    price = black_scholes_price(S, K, T, r, vol, option_type)
    delta, gamma, vega, theta, rho = black_scholes_greeks(S, K, T, r, vol, option_type)

    print(f"Prix de l'option {option_type.upper()} : {round(price, 2)} EUR")
    print(f"Delta : {round(delta, 4)}")
    print(f"Gamma : {round(gamma, 4)}")
    print(f"Vega  : {round(vega, 4)}")
    print(f"Theta : {round(theta, 4)}")
    print(f"Rho   : {round(rho, 4)}")

    # Estimation de la volatilité implicite
    try:
        market_price = float(input("\nEntrez un prix de marché pour calculer la volatilité implicite : "))
        imp_vol = implied_volatility(S, K, T, r, market_price, option_type)
        print(f"Volatilité implicite estimée : {round(imp_vol * 100, 2)} %")
    except ValueError as e:
        print(f"Erreur : {e}")