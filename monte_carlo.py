import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from black_scholes import black_scholes_price

def simulate_paths(S0, r, vol, T, n_steps=252, n_simulations=10000):
    """
    Simule des trajectoires de prix selon un mouvement Brownien géométrique.
    """
    dt = T / n_steps
    Z = np.random.standard_normal((n_simulations, n_steps))
    paths = np.zeros((n_simulations, n_steps + 1))
    paths[:, 0] = S0

    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * vol**2) * dt + vol * np.sqrt(dt) * Z[:, t-1])

    return paths

def monte_carlo_call_price(S0, K, r, vol, T, n_simulations=10000, n_steps=252, plot_paths=True):
    """
    Estime le prix d'un call européen par simulation Monte Carlo.
    Affiche éventuellement les trajectoires simulées et les sauvegarde.
    """
    paths = simulate_paths(S0, r, vol, T, n_steps, n_simulations)

    if plot_paths:
        plt.figure(figsize=(10, 5))
        for i in range(min(100, n_simulations)):
            plt.plot(paths[i], lw=0.5, alpha=0.6)
        plt.title("Trajectoires simulées de l'actif sous-jacent")
        plt.xlabel("Pas de temps")
        plt.ylabel("Prix")
        plt.grid(True)

        # 📸 Sauvegarde automatique
        plt.savefig("monte_carlo_paths.png")
        plt.tight_layout()
        plt.show()
        print("Graphique sauvegardé sous : monte_carlo_paths.png")

    payoffs = np.maximum(paths[:, -1] - K, 0)
    discounted = np.exp(-r * T) * payoffs
    estimated_price = discounted.mean()
    std_dev = discounted.std()

    return round(estimated_price, 4), round(std_dev, 4)

def convergence_analysis(S0, K, r, vol, T, n_steps=252, max_sim=10000):
    """
    Trace la convergence du prix simulé vers le prix théorique Black-Scholes.
    """
    from tqdm import tqdm  # Pour une barre de progression

    sim_counts = np.linspace(500, max_sim, 30, dtype=int)
    prices = []

    for n in tqdm(sim_counts, desc="Analyse de convergence"):
        price, _ = monte_carlo_call_price(S0, K, r, vol, T, n_simulations=n, n_steps=n_steps, plot_paths=False)
        prices.append(price)

    bs_price = black_scholes_price(S0, K, T, r, vol, option_type='call')

    plt.figure(figsize=(10, 5))
    plt.plot(sim_counts, prices, label='Monte Carlo Estimate')
    plt.axhline(bs_price, color='red', linestyle='--', label='Black-Scholes (analytique)')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Prix estimé')
    plt.title('Convergence vers le prix analytique')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def get_market_data(ticker, period='1y'):
    """
    Récupère les données de marché nécessaires au modèle.
    """
    try:
        data = yf.Ticker(ticker).history(period=period)
        if data.empty:
            raise ValueError(f"Aucune donnée disponible pour {ticker}")

        S0 = data['Close'].iloc[-1]
        returns = data['Close'].pct_change().dropna()
        vol = returns.std() * np.sqrt(252)

        taux = yf.Ticker("^TNX").history(period="1d")
        r = taux['Close'].iloc[-1] / 100 if not taux.empty else 0.044

        return S0, vol, r

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        raise

if __name__ == "__main__":
    print("=== Simulation Monte Carlo ===")
    ticker = input("Entrez le ticker (ex: AAPL, MSFT, ^GSPC) : ").upper()
    period = input("Période pour la volatilité (ex: 3mo, 1y) : ").lower()
    T = float(input("Maturité (en années, ex: 0.5 pour 6 mois) : "))
    K = float(input("Prix d'exercice (strike) : "))
    run_convergence = input("Afficher l'analyse de convergence ? (y/n) : ").lower() == 'y'

    try:
        S0, vol, r = get_market_data(ticker, period)
        print(f"\nPrix spot : {round(S0,2)} USD | Vol : {round(vol*100,2)} % | Taux sans risque : {round(r*100,2)} %")

        price, std_dev = monte_carlo_call_price(S0, K, r, vol, T)
        bs_price = black_scholes_price(S0, K, T, r, vol)

        abs_error = abs(price - bs_price)
        rel_error = abs_error / bs_price * 100

        print("\n=== Résultats ===")
        print(f"Monte Carlo : {price} USD ± {round(std_dev, 4)}")
        print(f"Black-Scholes : {round(bs_price, 4)} USD")
        print(f"Erreur absolue : {round(abs_error, 4)} USD")
        print(f"Erreur relative : {round(rel_error, 2)} %")

        if run_convergence:
            convergence_analysis(S0, K, r, vol, T)

    except Exception as e:
        print(f"Erreur : {e}")