"""
vol_smile.py
------------
Visualisation du smile de volatilité à partir de prix simulés par Black-Scholes.

Fonctionnalités :
- Génération de prix d'option pour plusieurs strikes
- Estimation de la volatilité implicite pour chaque strike
- Tracé du smile de volatilité
"""

import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_price, implied_volatility
from data_fetcher import get_stock_data

def generate_smile(S0, T, r, vol, option_type='call', n_points=20, spread=0.3):
    """Construit un smile de volatilité autour du spot."""
    strikes = np.linspace(S0 * (1 - spread), S0 * (1 + spread), n_points)
    iv_list = []

    for K in strikes:
        theo_price = black_scholes_price(S0, K, T, r, vol, option_type)
        iv = implied_volatility(S0, K, T, r, theo_price, option_type)
        iv_list.append(iv)

    return strikes, iv_list

def plot_smile(strikes, iv_list, ticker):
    """Trace le smile de volatilité."""
    plt.figure(figsize=(10, 6))
    plt.plot(strikes, np.array(iv_list) * 100, marker='o')
    plt.title(f"Smile de volatilité pour {ticker}")
    plt.xlabel("Strike")
    plt.ylabel("Volatilité implicite (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker = input("Entrez le ticker (ex: AAPL, MSFT, ^GSPC) : ").upper()
    period = input("Entrez la période pour la volatilité historique (ex: 1mo, 3mo, 1y) : ").lower()

    data = get_stock_data(ticker, period)

    if data:
        S0 = data['Spot Price (USD)']
        vol = data['Volatility (%)'] / 100
        r = data['Risk-Free Rate (%)'] / 100

        print(f"\nPrix spot : {S0} USD")
        print(f"Volatilité estimée : {round(vol * 100, 2)} %")
        print(f"Taux sans risque : {round(r * 100, 2)} %")

        T = float(input("Entrez la maturité (en années, ex: 0.5) : "))
        option_type = input("Type d'option (call ou put) : ").lower()

        strikes, ivs = generate_smile(S0, T, r, vol, option_type)
        plot_smile(strikes, ivs, ticker)
    else:
        print("Erreur lors de la récupération des données.")