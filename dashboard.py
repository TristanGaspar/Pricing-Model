"""
dashboard.py
------------
Interface terminale permettant d'utiliser le modèle Black-Scholes avec des données de marché.

Fonctionnalités :
- Récupération automatique des données (prix spot, volatilité, taux sans risque)
- Calcul du prix théorique d'une option européenne
- Calcul des Greeks
"""

from black_scholes import black_scholes_price, black_scholes_greeks
from data_fetcher import get_stock_data
import sys

def run_dashboard():
    print("=== DASHBOARD OPTIONS ===")

    # Saisie des paramètres de marché
    ticker = input("Entrez le ticker de l'actif (ex: AAPL, MSFT, ^GSPC) : ").upper()
    period = input("Entrez la période d'analyse (ex: 1mo, 3mo, 1y) : ").lower()

    result = get_stock_data(ticker, period)
    if not result:
        print("Aucune donnée récupérée. Fin du programme.")
        sys.exit(1)

    spot = result['Spot Price (USD)']
    vol = result['Volatility (%)'] / 100
    r = result['Risk-Free Rate (%)'] / 100

    print(f"\nPrix spot : {spot} USD")
    print(f"Volatilité annualisée : {round(vol * 100, 2)} %")
    print(f"Taux sans risque : {round(r * 100, 2)} %")

    # Paramètres de l'option
    try:
        K = float(input("Entrez le strike : "))
        T = float(input("Entrez la maturité en années (ex: 0.5 pour 6 mois) : "))
        option_type = input("Entrez le type d'option (call ou put) : ").lower()

        if option_type not in ['call', 'put']:
            raise ValueError("Type d'option invalide.")

    except ValueError as e:
        print(f"Erreur : {e}")
        sys.exit(1)

    # Calculs Black-Scholes
    price = black_scholes_price(spot, K, T, r, vol, option_type)
    delta, gamma, vega, theta, rho = black_scholes_greeks(spot, K, T, r, vol, option_type)

    # Résultats
    print("\n=== Résultats du modèle Black-Scholes ===")
    print(f"Prix théorique de l'option {option_type.upper()} : {round(price, 2)} USD")
    print(f"Delta  : {round(delta, 4)}")
    print(f"Gamma  : {round(gamma, 4)}")
    print(f"Vega   : {round(vega, 4)}")
    print(f"Theta  : {round(theta, 4)}")
    print(f"Rho    : {round(rho, 4)}")

if __name__ == "__main__":
    run_dashboard()