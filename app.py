# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path
import importlib.util

from database import init_db

# Crée la base et la table si elles n'existent pas
init_db()


# ==============================
# CONFIGURATION PAGE
# ==============================
st.set_page_config(
    page_title="Application Financière – Planification Stratégique",
    layout="wide"
)

# ==============================
# BRANDING INVESTISSEUR – FINANCE EXECUTIVE
# ==============================
st.markdown(
    """
    <style>

    /* ===== PALETTE INVESTISSEUR ===== */
    :root {
        --gold: #C9A227;
        --gold-light: #FFF4CC;
        --ivory: #FAF9F6;
        --anthracite: #1C1C1C;
        --gray-soft: #6F6F6F;
        --shadow: 0 18px 40px rgba(0,0,0,0.10);
        --radius-xl: 18px;
    }

    /* ===== APP BACKGROUND ===== */
    .stApp {
        background: linear-gradient(
            180deg,
            #FAF9F6 0%,
            #FFFFFF 100%
        );
        color: var(--anthracite);
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    /* ===== SIDEBAR – INVESTOR NAV ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1C1C1C 0%,
            #2B2B2B 100%
        );
        box-shadow: var(--shadow);
        border-right: 4px solid var(--gold);
    }

    [data-testid="stSidebar"] * {
    color: #000000 !important;
    font-weight: 600;
}

    }

    /* ===== TITRES EXECUTIVE ===== */
    h1 {
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -0.8px;
        margin-bottom: 0.2em;
    }

    h2, h3 {
        font-weight: 800;
        letter-spacing: -0.4px;
    }

    /* ===== SOUS-TITRE / CAPTION ===== */
    .stCaption {
        color: var(--gray-soft);
        font-size: 0.95rem;
    }

    /* ===== CARTES FINANCIÈRES ===== */
    div[data-testid="stMetric"],
    div[data-testid="stDataFrame"],
    div.element-container {
        background: white;
        border-radius: var(--radius-xl);
        padding: 20px;
        box-shadow: var(--shadow);
        border-left: 5px solid var(--gold);
        margin-bottom: 20px;
    }

    /* ===== METRICS ===== */
    div[data-testid="stMetric"] label {
        color: var(--gray-soft);
        font-weight: 600;
    }

    div[data-testid="stMetric"] div {
        font-size: 1.4rem;
        font-weight: 800;
    }

    /* ===== BOUTONS EXECUTIVE ===== */
    .stButton>button {
        background: linear-gradient(
            135deg,
            #C9A227,
            #E5C867
        );
        color: #1C1C1C;
        border-radius: 14px;
        border: none;
        padding: 0.7em 1.6em;
        font-weight: 800;
        letter-spacing: 0.3px;
        box-shadow: 0 10px 25px rgba(201,162,39,0.45);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 40px rgba(201,162,39,0.65);
    }

    /* ===== INPUTS FINANCIERS ===== */
    input, textarea, select {
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 10px !important;
        font-weight: 600;
    }

    /* ===== SLIDERS ===== */
    .stSlider > div {
        padding-top: 12px;
    }

    /* ===== TABLES ===== */
    thead tr th {
        background-color: var(--gold-light) !important;
        color: var(--anthracite) !important;
        font-weight: 800;
    }

    /* ===== FOOTER ===== */
    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# SESSION STATE INIT
# ==============================
if "scenario" not in st.session_state:
    st.session_state.scenario = "Central"

# ==============================
# TITRE PRINCIPAL
# ==============================
st.title("Application Financière de Planification Stratégique et Comptable")
st.caption("Auteur : Mohamed Falilou Fall / Email : mff.falilou.fall@gmail.com / Téléphone : +221779141589 ")

# ==============================
# DICTIONNAIRE DES PAGES
# ==============================
pages = {
    "01_Hypothèses d’activité": "01_Hypotheses_Activite.py",
    "02_Compte de résultat": "02_Compte_Resultat_Previsionnel.py",
    "03_Seuil de rentabilité": "03_Seuil_Rentabilite.py",
    "04_BFR": "04_BFR.py",
    "05_Plan de financement": "05_Plan_Financement.py",
    "06_Plan de trésorerie": "06_Plan_Tresorerie.py",
    "07_Données financières clés": "07_Donnees_Financieres_Cles.py",
    "08_Scénarios": "08_Scenarios.py",
    "09_Export & reporting": "09_Export.py",
}

# ==============================
# SIDEBAR NAVIGATION
# ==============================
selection = st.sidebar.radio("Choisir un module", list(pages.keys()))

# ==============================
# CHARGEMENT SÉCURISÉ DU MODULE
# ==============================
BASE_DIR = Path(__file__).parent
PAGE_DIR = BASE_DIR / "pages"

page_path = PAGE_DIR / pages[selection]

if page_path.exists():
    spec = importlib.util.spec_from_file_location("page_module", page_path)
    page_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page_module)

    if hasattr(page_module, "run"):
        page_module.run()
    else:
        st.error(f"La page {page_path.name} ne contient pas de fonction run()")
else:
    st.error(f"Fichier introuvable : {page_path}")
