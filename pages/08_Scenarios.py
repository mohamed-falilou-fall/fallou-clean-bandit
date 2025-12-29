# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("Scénarios financiers & analyse de sensibilité")

    st.markdown("### Choix du scénario")
    scenario = st.radio("Sélectionner un scénario", ["Central", "Optimiste", "Pessimiste"], horizontal=True)

    CA_base = st.session_state.get("hypotheses", {}).get("Chiffre d'affaires HT (1 x 2 x 3)", 0.0)
    charges_base = st.session_state.get("compte_resultat", {}).get("Année 1", {}).get("Charges totales", 0.0)

    coefficients = {"Central": 1.0, "Optimiste": 1.15, "Pessimiste": 0.85}
    coef = coefficients[scenario]

    st.markdown("### Sensibilité des hypothèses")
    sens_CA = st.slider("Variation du CA (%)", -30, 30,
                        value=st.session_state.get("scenarios", {}).get("sens_CA", 0))
    sens_charges = st.slider("Variation des charges (%)", -20, 20,
                             value=st.session_state.get("scenarios", {}).get("sens_charges", 0))

    CA_scenario = CA_base * coef * (1 + sens_CA / 100)
    charges_scenario = charges_base * (1 + sens_charges / 100)
    resultat = CA_scenario - charges_scenario

    df_scenario = pd.DataFrame({
        "Indicateur": ["Chiffre d'affaires", "Charges", "Résultat"],
        "Montant (F CFA)": [CA_scenario, charges_scenario, resultat]
    })

    st.subheader(f"Résultats – Scénario {scenario}")
    st.dataframe(df_scenario.style.format({"Montant (F CFA)": "{:,.3f}"}))

    df_compare = pd.DataFrame({
        "Scénario": ["Pessimiste", "Central", "Optimiste"],
        "CA (F CFA)": [CA_base*coefficients["Pessimiste"], CA_base, CA_base*coefficients["Optimiste"]],
        "Résultat (F CFA)": [
            CA_base*coefficients["Pessimiste"]-charges_base,
            CA_base-charges_base,
            CA_base*coefficients["Optimiste"]-charges_base
        ]
    })

    fig = px.bar(df_compare, x="Scénario", y="Résultat (F CFA)", color="Scénario",
                 title="Comparaison des résultats par scénario")
    st.plotly_chart(fig, use_container_width=True)

    # Sauvegarde dans session_state
    st.session_state.setdefault("scenarios", {})["sens_CA"] = sens_CA
    st.session_state["scenarios"]["sens_charges"] = sens_charges
