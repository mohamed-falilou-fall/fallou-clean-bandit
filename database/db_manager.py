# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path

# ==============================
# CHEMIN BASE DE DONNÉES
# ==============================
DB_PATH = Path("database/falilou_finance.db")

# ==============================
# CONNEXION
# ==============================
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ==============================
# INITIALISATION BASE
# ==============================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donnees_financieres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module TEXT NOT NULL,
        annee TEXT NOT NULL,
        cle TEXT NOT NULL,
        valeur REAL,
        date_sauvegarde TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# ==============================
# SAUVEGARDE DONNÉES MODULE
# ==============================
def save_module_data(module: str, annee: str, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Supprimer les anciennes données du module / année
    cursor.execute("""
        DELETE FROM donnees_financieres
        WHERE module = ? AND annee = ?
    """, (module, annee))

    # Insérer les nouvelles valeurs
    for cle, valeur in data.items():
        cursor.execute("""
            INSERT INTO donnees_financieres (module, annee, cle, valeur)
            VALUES (?, ?, ?, ?)
        """, (module, annee, cle, float(valeur)))

    conn.commit()
    conn.close()

# ==============================
# LECTURE DONNÉES MODULE
# ==============================
def load_module_data(module: str, annee: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cle, valeur
        FROM donnees_financieres
        WHERE module = ? AND annee = ?
    """, (module, annee))

    data = {cle: valeur for cle, valeur in cursor.fetchall()}
    conn.close()
    return data

# ==============================
# LECTURE TOUTES DONNÉES
# ==============================
def load_all_data() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT module, annee, cle, valeur
        FROM donnees_financieres
        ORDER BY module, annee
    """)

    result = {}
    for module, annee, cle, valeur in cursor.fetchall():
        result.setdefault(module, {}).setdefault(annee, {})[cle] = valeur

    conn.close()
    return result

# ==============================
# SUPPRESSION MODULE / ANNÉE
# ==============================
def delete_module_data(module: str, annee: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM donnees_financieres
        WHERE module = ? AND annee = ?
    """, (module, annee))

    conn.commit()
    conn.close()
