#  Projet BI A nalyse Northwind

## Description

Ce projet présente un **dashboard BI interactif** permettant d’analyser les commandes à partir d’un **Data Warehouse** basé sur **SQL Server**.  
Le tableau de bord est développé avec **Python, Pandas et Streamlit** et permet de visualiser les **KPI clés** selon les dimensions **Temps, Client et Employé**.

Le modèle de données suit un **schéma en étoile (Star Schema)** avec une table de faits et plusieurs dimensions.

---

## Objectifs du projet

- Calculer les KPI des commandes livrées et non livrées
- Analyser les commandes par :
  - Temps (mois / année)
  - Client
  - Employé
- Réaliser des analyses croisées :
  - Client × Temps
  - Employé × Temps
  - Employé × Client
- Fournir un dashboard interactif avec filtres dynamiques

---

---

## Modèle de données

- **Table de faits** : `faitcommande`
- **Dimensions** :
  - `client`
  - `employee`
  - `temps`

La table `temps` permet une analyse temporelle par mois et par année.

---

##  Technologies utilisées

- Python
- Pandas
- SQLAlchemy
- PyODBC
- Streamlit
- SQL Server

---

## Prérequis

- Python 3.10+
- SQL Server
- ODBC Driver 17 for SQL Server

### Installation des dépendances

```bash
pip install pandas sqlalchemy pyodbc streamlit
```

##  Lancer le dashboard

### 1️- Cloner le dépôt

```bash
git clone
```
### 2-Lancer l’application Streamlit

```bash
streamlit run scripts\dashboard.py
```
Le dashboard s’ouvrira automatiquement dans le navigateur.

### Auteur

Anfal BOUCHAREB
Business Intelligence 


