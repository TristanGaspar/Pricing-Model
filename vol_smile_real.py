"""
vol_smile_real.py
-----------------
Smile de volatilité implicite basé sur des prix d’options réels du marché via yFinance.

Fonctionnalités :
- Récupération des chaînes d’options (prix, strikes, bid/ask)
- Calcul de la volatilité implicite par strike
- Tracé du smile observé sur le marché
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from black_scholes import implied_volatility

def get_real_smile(ticker, option_type='call', maturity_days=30):
    """Construit un smile de volatilité implicite à partir des prix du marché."""
    try:
        tk = yf.Ticker(ticker)
        expirations = tk.options
        if not expirations:
            print("Aucune date d'expiration disponible.")
            return

        target_date = (datetime.today() + timedelta(days=maturity_days)).date()
        selected_date = min(expirations, key=lambda d: abs(datetime.strptime(d, "%Y-%m-%d").date() - target_date))
        chain = tk.option_chain(selected_date)
        options = chain.calls if option_type == 'call' else chain.puts

        spot = tk.history(period="1d")['Close'][-1]
        r = yf.Ticker("^TNX").history(period="1d")['Close'][-1] / 100 if not yf.Ticker("^TNX").history(period="1d").empty else 0.04
        T = (datetime.strptime(selected_date, "%Y-%m-%d") - datetime.today()).days / 365

        strikes, implied_vols = [], []

        for _, row in options.iterrows():
            K = row['strike']
            mid_price = (row['bid'] + row['ask']) / 2
            if mid_price > 0:
                try:
                    iv = implied_volatility(spot, K, T, r, mid_price, option_type)
                    if iv:
                        strikes.append(K)
                        implied_vols.append(iv * 100)
                except Exception:
                    continue

        if strikes:
            plt.figure(figsize=(10, 6))
            plt.plot(strikes, implied_vols, 'o-', label='Volatilité implicite (%)')
            plt.title(f"Smile de volatilité implicite ({ticker} - {option_type.upper()})\nÉchéance : {selected_date}")
            plt.xlabel("Prix d'exercice (Strike)")
            plt.ylabel("Volatilité implicite (%)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("Pas de volatilités implicites valides à tracer.")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    ticker = input("Ticker (ex: AAPL, MSFT) : ").upper()
    option_type = input("Type d'option (call ou put) : ").lower()
    maturity_days = int(input("Maturité approximative en jours (ex: 30) : "))
    get_real_smile(ticker, option_type, maturity_days)