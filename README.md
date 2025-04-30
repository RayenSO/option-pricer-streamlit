# 📈 Option Pricer - Streamlit App

Cette application vous permet de calculer le prix théorique et les grecques d'une option **Call ou Put**, en utilisant trois modèles de pricing :

- **Black-Scholes**
- **Arbre Binomial de Cox-Ross-Rubinstein**
- **Méthode de Monte Carlo**

Vous pouvez choisir :
- Le **modèle de pricing**
- Le **type d'option** (européenne ou américaine)
- Les **paramètres de marché** : prix d’exercice (*Strike*), échéance, volatilité, taux sans risque, etc.

Le tout dans une interface interactive développée avec **Streamlit**.

---

## 🚀 Lancer l'application en local

### 1. Cloner le projet

```bash
git clone https://github.com/ton-username/option-pricer-streamlit.git
cd option-pricer-streamlit
```

### 2. Cloner le projet

```bash
python -m venv venv
source venv/bin/activate      # Sur macOS / Linux
venv\Scripts\activate.bat     # Sur Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
streamlit run app.py
```

## 🌐 Version en ligne

L'application est également accessible directement sur Streamlit Cloud à l'adresse suivante :
👉 option-pricer-app-rayen-and-eliasy.streamlit.app

# 📂 Contenu du projet

```bash
├── app.py                   # Interface Streamlit principale
├── black_scholes.py         # Modèle Black-Scholes
├── binomial_tree.py         # Modèle Binomial CRR
├── monte_carlo.py           # Modèle Monte Carlo
├── documentation.tex        # Documentation LaTeX complète
├── documentation.pdf        # Documentation PDF (LaTeX compilé)
├── main.py                  # Première version des modèles sans interface graphique et manuelle
├── main_v2.py               # Seconde version des modèles avec récupération des prix sur Yahoo Finance
├── documentation.tex        # Documentation LaTeX complète
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier
```

## 📄 Documentation technique

Une documentation détaillée au format LaTeX est disponible dans le fichier documentation.tex et documentation.pdf.
Elle inclut :

- Les formules des modèles de pricing
- Les définitions et interprétations des Greeks
- Les hypothèses et fondements de chaque approche

## 👨‍💻 Auteurs
Développé dans le cadre du cours Applied Mathematics for Finance du Master 2 Gestion de Portefeuille (IAE Paris-Est)
par :

Rayen SOLTANI

Ny Avotra ELIASY