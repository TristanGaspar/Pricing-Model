# Pricing Model – Valorisation d’options en Python

Le pricing d’options est au cœur de nombreux métiers de la finance de marché : structuration, trading, gestion des risques.  
Ce projet propose une suite de modules en Python permettant de valoriser des options européennes (call/put) à l’aide de différents modèles, tout en intégrant des fonctionnalités avancées comme le calcul des Greeks, l’estimation de la volatilité implicite ou encore la simulation Monte Carlo.

---

## 🔹 Fonctionnalités principales

- Pricing analytique via le modèle de Black-Scholes
- Calcul des Greeks : Delta, Gamma, Vega, Theta, Rho
- Estimation de la volatilité implicite (inversion de modèle)
- Simulation Monte Carlo (prix + analyse de convergence)
- Smile de volatilité (théorique et réel)
- Récupération automatisée des données de marché (spot, vol, taux)
- Interface CLI interactive

---

## 🔹 Vue d’ensemble des modules

| Fichier               | Rôle principal |
|----------------------|----------------|
| `black_scholes.py`   | Modèle de pricing Black-Scholes + Greeks + vol implicite |
| `monte_carlo.py`     | Simulation Monte Carlo + analyse de convergence |
| `plotter.py`         | Visualisation des Greeks en fonction du spot |
| `vol_smile.py`       | Smile de volatilité (théorique, modèle Black-Scholes) |
| `vol_smile_real.py`  | Smile de volatilité réel (données marché) |
| `dashboard.py`       | Interface utilisateur interactive |
| `data_fetcher.py`    | Extraction de données via yFinance |

---

## 🔍 Analyse détaillée des fichiers

### `black_scholes.py`

Implémente le modèle Black-Scholes pour valoriser une option européenne (call ou put).  
Inclut le calcul des principaux Greeks et une fonction d’inversion du modèle pour obtenir la volatilité implicite à partir d’un prix observé.

---

### `monte_carlo.py`

Permet de valoriser une option call via des simulations Monte Carlo.  
Affiche les trajectoires simulées, estime le prix moyen et permet une analyse de convergence vers le prix Black-Scholes.

---

### `plotter.py`

Produit des graphiques illustrant la variation du prix et des principaux Greeks (Delta, Gamma, Vega, Theta, Rho) en fonction du prix spot.  
Utile pour analyser la sensibilité des options aux mouvements du sous-jacent.

---

### `vol_smile.py`

Génère un smile de volatilité théorique à partir du modèle Black-Scholes en inversant la formule sur une plage de strikes, avec une volatilité constante en entrée.  
Permet de représenter graphiquement la courbe de volatilité implicite modélisée.

---

### `vol_smile_real.py`

Construit un smile de volatilité à partir de données de marché réelles, récupérées via yFinance.  
Utilise des prix d’options cotées pour reconstituer une courbe de volatilité implicite observable sur les marchés.

---

### `dashboard.py`

Interface en ligne de commande permettant de :
- Saisir un ticker, une période, un strike et une maturité ;
- Récupérer automatiquement les données nécessaires ;
- Obtenir le prix Black-Scholes et les Greeks correspondants.

---

### `data_fetcher.py`

Télécharge les données de marché (prix spot, volatilité historique, volume moyen, taux sans risque US 10Y) depuis yFinance.  
Gère les erreurs de récupération et assure une extraction exploitable pour les autres modules.

---

## 🔧 Installation

```bash
git clone https://github.com/TristanGaspar/Pricing-Model.git
cd Pricing-Model
pip install -r requirements.txt
