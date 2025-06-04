import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_price, black_scholes_greeks
from data_fetcher import get_stock_data

def plot_greeks_vs_spot(S0, K, T, r, vol, option_type='call', spread=0.3):
    """
    Trace le prix et les greeks d'une option en fonction du prix spot S.
    La grille S est centrée autour de S0.
    """
    S_min = S0 * (1 - spread)
    S_max = S0 * (1 + spread)
    S = np.linspace(S_min, S_max, 200)

    prices, deltas, gammas, vegas, thetas, rhos = [], [], [], [], [], []

    for s in S:
        prices.append(black_scholes_price(s, K, T, r, vol, option_type))
        d, g, v, t, rho = black_scholes_greeks(s, K, T, r, vol, option_type)
        deltas.append(d)
        gammas.append(g)
        vegas.append(v)
        thetas.append(t)
        rhos.append(rho)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 3, 1)
    plt.plot(S, prices)
    plt.title('Prix de l\'option')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Prix')

    plt.subplot(2, 3, 2)
    plt.plot(S, deltas)
    plt.title('Delta')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Delta')

    plt.subplot(2, 3, 3)
    plt.plot(S, gammas)
    plt.title('Gamma')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Gamma')

    plt.subplot(2, 3, 4)
    plt.plot(S, vegas)
    plt.title('Vega')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Vega')

    plt.subplot(2, 3, 5)
    plt.plot(S, thetas)
    plt.title('Theta')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Theta')

    plt.subplot(2, 3, 6)
    plt.plot(S, rhos)
    plt.title('Rho')
    plt.xlabel('Prix spot (S)')
    plt.ylabel('Rho')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker = input("Entrez le ticker (ex: AAPL, MSFT, ^GSPC) : ").upper()
    period = input("Entrez la période (ex: 1mo, 3mo, 1y) : ").lower()

    try:
        data = get_stock_data(ticker, period)

        if data:
            S0 = data['Spot Price (USD)']
            vol = data['Volatility (%)'] / 100
            r = data['Risk-Free Rate (%)'] / 100

            print(f"\n--- Données de marché pour {ticker} ---")
            print(f"Prix spot : {S0} USD")
            print(f"Volatilité annualisée : {round(vol * 100, 2)} %")
            print(f"Taux sans risque : {round(r * 100, 2)} %")

            K = float(input("Entrez le prix d'exercice (strike) : "))
            T = float(input("Entrez la maturité en années (ex: 0.5 = 6 mois) : "))
            option_type = input("Type d'option (call ou put) : ").lower()

            plot_greeks_vs_spot(S0, K, T, r, vol, option_type)

        else:
            print("Erreur : impossible de récupérer les données du marché.")
    except Exception as e:
        print(f"Erreur : {e}")