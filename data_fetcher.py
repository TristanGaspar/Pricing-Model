import yfinance as yf
import numpy as np
import pandas as pd
import logging
import csv

# === Configuration du logger ===
logging.basicConfig(filename='fetcher_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# === Taux sans risque par défaut (si données indisponibles) ===
DEFAULT_RISK_FREE_RATE = 0.04

def get_stock_data(ticker, period='1y'):
    """
    Récupère le prix spot, la volatilité annualisée, le rendement moyen, le volume moyen d'un actif, et le taux sans risque (US 10 ans).
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"Aucune donnée disponible pour {ticker} sur la période {period}")

        # Prix spot = dernier prix de clôture
        spot_price = hist['Close'].iloc[-1]

        # Volatilité annualisée en %
        returns = hist['Close'].pct_change().dropna()
        vol = returns.std() * np.sqrt(252) * 100

        # Rendement moyen et volume moyen
        avg_return = returns.mean() * 100
        avg_volume = hist['Volume'].mean()

        # Taux sans risque (US 10Y Treasury via Yahoo Finance)
        tnx = yf.Ticker("^TNX")
        tnx_data = tnx.history(period="1d")

        if tnx_data.empty:
            risk_free_rate = DEFAULT_RISK_FREE_RATE * 100  # Par défaut
        else:
            tnx_value = tnx_data['Close'].iloc[-1]
            risk_free_rate = tnx_value / 10  # Yahoo donne le rendement *10

        risk_free_rate_decimal = risk_free_rate / 100

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
        print(f"Erreur : {e}")
        return None

def save_to_csv(data, filename='data_summary.csv'):
    """Ajoute les données à un fichier CSV."""
    df = pd.DataFrame([data])
    try:
        df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
        print(f"Données sauvegardées dans {filename}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde dans {filename}: {e}")
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