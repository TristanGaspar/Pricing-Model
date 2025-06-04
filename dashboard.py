from black_scholes import black_scholes_price, black_scholes_greeks
from data_fetcher import get_stock_data
import sys

def run_dashboard():
    print("=== DASHBOARD OPTIONS ===")

    # Ticker et période
    ticker = input("Entrez le ticker de l'actif (ex: AAPL, MSFT, ^GSPC) : ").upper()
    period = input("Entrez la période d'analyse pour la volatilité (ex: 1mo, 3mo, 1y) : ").lower()

    # Récupérer le spot et la volatilité via get_stock_data
    spot, vol = None, None
    result = get_stock_data(ticker, period)

    if result:
        spot = result['Spot Price (USD)']
        vol = result['Volatility (%)'] / 100  # Convertir en décimal
        print(f"\nPrix spot de {ticker} : {spot} USD")
        print(f"Volatilité annualisée estimée : {round(vol*100, 2)} %")
    else:
        print("Aucune donnée récupérée. Fin du programme.")
        sys.exit(1)

    # Inputs manuels
    try:
        K = float(input("Entrez le prix d'exercice (strike) de l'option : "))
        T = float(input("Entrez la maturité en années (ex: 0.5 = 6 mois) : "))
        option_type = input("Entrez le type d'option (call ou put) : ").lower()

        if option_type not in ['call', 'put']:
            print("Type d'option invalide. Veuillez entrer 'call' ou 'put'.")
            sys.exit(1)

    except ValueError:
        print("Entrée invalide. Veuillez entrer des nombres valides.")
        sys.exit(1)

    # Calculs Black-Scholes
    r = result['Risk-Free Rate (%)'] / 100  # Taux sans risque
    price = black_scholes_price(spot, K, T, r, vol, option_type)
    delta, gamma, vega, theta, rho = black_scholes_greeks(spot, K, T, r, vol, option_type)

    # Affichage des résultats
    print("\n=== Résultats du modèle Black-Scholes ===")
    print(f"Prix théorique de l'option {option_type.upper()} : {round(price, 2)} USD")
    print(f"Delta : {round(delta, 4)}")
    print(f"Gamma : {round(gamma, 4)}")
    print(f"Vega : {round(vega, 4)}")
    print(f"Theta : {round(theta, 4)}")
    print(f"Rho : {round(rho, 4)}")

if __name__ == "__main__":
    run_dashboard()