"""
data_fetcher.py
---------------
Récupère automatiquement les données de marché pour un actif : prix spot, volatilité, rendement moyen, volume, taux sans risque.
Permet aussi de sauvegarder les résultats dans un fichier CSV.
"""

import yfinance as yf
import numpy as np
import pandas as pd
import logging

# Configuration du logger (en cas d'erreur réseau, API, etc.)
logging.basicConfig(filename='fetcher_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_RISK_FREE_RATE = 0.04  # Taux sans risque par défaut (4%) si non disponible

def get_stock_data(ticker, period='1y'):
    """
    Récupère les indicateurs de marché à partir de yFinance pour un actif donné.
    Retourne : prix spot, volatilité annualisée, rendement moyen, volume moyen, taux sans risque.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"Aucune donnée disponible pour {ticker} sur la période {period}")

        spot_price = hist['Close'].iloc[-1]
        returns = hist['Close'].pct_change().dropna()
        vol = returns.std() * np.sqrt(252) * 100
        avg_return = returns.mean() * 100
        avg_volume = hist['Volume'].mean()

        # Récupération du taux 10Y américain (^TNX)
        tnx = yf.Ticker("^TNX").history(period="1d")
        if tnx.empty:
            risk_free_rate = DEFAULT_RISK_FREE_RATE * 100
        else:
            risk_free_rate = tnx['Close'].iloc[-1] / 10  # Yahoo donne le taux multiplié par 10

        return {
            'Ticker': ticker,
            'Spot Price (USD)': round(spot_price, 2),
            'Volatility (%)': round(vol, 2),
            'Avg Daily Return (%)': round(avg_return, 4),
            'Avg Daily Volume': int(avg_volume),
            'Risk-Free Rate (%)': round(risk_free_rate, 2)
        }

    except Exception as e:
        logging.error(f"Erreur pour {ticker}: {e}")
        print(f"Erreur lors de la récupération des données : {e}")
        return None

def save_to_csv(data, filename='data_summary.csv'):
    """
    Sauvegarde les données dans un fichier CSV. Ajoute la ligne sans écraser les précédentes.
    """
    df = pd.DataFrame([data])
    try:
        df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
        print(f"Données sauvegardées dans {filename}")
    except Exception as e:
        logging.error(f"Erreur de sauvegarde dans {filename}: {e}")
        print(f"Erreur lors de la sauvegarde : {e}")

if __name__ == "__main__":
    ticker = input("Entrez le ticker (ex: AAPL, TSLA, MSFT, ^GSPC) : ").upper()
    period = input("Entrez la période (ex: 1mo, 3mo, 1y) : ").lower()

    result = get_stock_data(ticker, period)
    if result:
        print("\nRésultats :")
        for key, value in result.items():
            print(f"{key}: {value}")
        save_to_csv(result)
    else:
        print("Aucun résultat à afficher.")