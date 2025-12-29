# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("AUTRES DONNÉES FINANCIÈRES CLÉS")

    cr_module = st.session_state.get("compte_resultat", {})
    bfr_module = st.session_state.get("bfr", {})
    tresorerie_module = st.session_state.get("tresorerie", {})

    # Fonds de roulement (FR)
    financements_stables = st.number_input(
        "(1) Financements stables",
        value=st.session_state.get("donnees_financieres", {}).get("Financements_stables", 0.0),
        format="%.3f", key="financements_stables"
    )
    emplois_stables = st.number_input(
        "(2) Emplois stables",
        value=st.session_state.get("donnees_financieres", {}).get("Emplois_stables", 0.0),
        format="%.3f", key="emplois_stables"
    )

    FR = financements_stables - emplois_stables
    st.markdown(f"**Fonds de roulement (FR) = {FR:,.3f} F CFA**")

    # Trésorerie prévisionnelle
    BFR = bfr_module.get("BFR", 0.0)
    tresorerie_prev = FR - BFR
    st.markdown(f"**Trésorerie prévisionnelle = {tresorerie_prev:,.3f} F CFA**")

    # Capacité d'autofinancement (CAF)
    RN = cr_module.get("Année 1", {}).get("Résultat net (RN)", 0.0)
    amortissements = cr_module.get("Année 1", {}).get("Dotations aux amortissements", 0.0)
    provisions = cr_module.get("Année 1", {}).get("Dotations aux provisions", 0.0)
    reprises = st.number_input(
        "Reprises",
        value=st.session_state.get("donnees_financieres", {}).get("Reprises", 0.0),
        format="%.3f", key="reprises"
    )

    CAF = RN + amortissements + provisions - reprises
    st.markdown(f"**Capacité d'autofinancement (CAF) = {CAF:,.3f} F CFA**")

    # Rentabilité d'exploitation
    VA = cr_module.get("Année 1", {}).get("Valeur ajoutée (VA)", 0.0)
    rentabilite = RN / VA if VA != 0 else 0.0
    st.markdown(f"**Rentabilité d'exploitation = {rentabilite*100:.3f} %**")

    # DataFrame récapitulatif
    df = pd.DataFrame({
        "Indicateur": [
            "Fonds de roulement (FR)",
            "Besoin en fonds de roulement (BFR)",
            "Trésorerie prévisionnelle",
            "Résultat net (RN)",
            "Dotations aux amortissements et provisions",
            "Reprises",
            "Capacité d'autofinancement (CAF)",
            "Valeur ajoutée (VA)",
            "Rentabilité d'exploitation (%)"
        ],
        "Valeur (F CFA / %)": [
            FR, BFR, tresorerie_prev, RN, amortissements + provisions, reprises, CAF, VA, rentabilite*100
        ]
    })

    st.dataframe(df.style.format({"Valeur (F CFA / %)": "{:,.3f}"}))

    # Sauvegarde dans session_state
    st.session_state.setdefault("donnees_financieres", {})["Financements_stables"] = financements_stables
    st.session_state["donnees_financieres"]["Emplois_stables"] = emplois_stables
    st.session_state["donnees_financieres"]["Reprises"] = reprises
