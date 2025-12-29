# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def calcul_seuil_rentabilite(CA, charges_variables, charges_fixes):
    """
    Calcule tous les indicateurs du seuil de rentabilité
    en sécurisant les divisions.
    """
    marge = CA - (charges_variables + charges_fixes)
    mcv = CA - charges_variables
    taux_mcv = (mcv / CA) if CA != 0 else 0
    seuil = (charges_fixes / taux_mcv) if taux_mcv != 0 else 0

    return {
        "CA": CA,
        "CV": charges_variables,
        "CF": charges_fixes,
        "Charges_totales": charges_variables + charges_fixes,
        "Marge": marge,
        "MCV": mcv,
        "Taux_MCV": taux_mcv * 100,
        "Seuil": seuil
    }


def run():
    st.title("SEUIL DE RENTABILITÉ (3 ANS)")
    st.caption("Analyse du seuil de rentabilité basée sur les hypothèses et le compte de résultat")

    hyp = st.session_state.get("hypotheses_saved", {})
    sr_saved = st.session_state.get("seuil_rentabilite", {})

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        CA = st.number_input(
            "Chiffre d'affaires HT",
            value=sr_saved.get(annee, {}).get("CA", hyp.get("ca_ht", 0.0)) if annee=="Année 1" else sr_saved.get(annee, {}).get("CA", 0.0),
            format="%.3f",
            key=f"ca_sr_{annee}"
        )

        st.markdown("**Charges variables (CV)**")
        achats = st.number_input(
            "Achats / consommations variables",
            sr_saved.get(annee, {}).get("CV",0.0),
            format="%.3f",
            key=f"achats_cv_{annee}"
        )
        autres_cv = st.number_input(
            "Autres charges variables",
            sr_saved.get(annee, {}).get("Autres_CV",0.0),
            format="%.3f",
            key=f"autres_cv_{annee}"
        )
        charges_variables = achats + autres_cv

        st.markdown("**Charges fixes (CF)**")
        loyer = st.number_input(
            "Loyer",
            sr_saved.get(annee, {}).get("Loyer", hyp.get("loyer",0.0)),
            format="%.3f",
            key=f"loyer_cf_{annee}"
        )
        salaires = st.number_input(
            "Salaires",
            sr_saved.get(annee, {}).get("Salaires", hyp.get("salaires_indiv",0.0)+hyp.get("salaires_emp",0.0)),
            format="%.3f",
            key=f"salaires_cf_{annee}"
        )
        autres_cf = st.number_input(
            "Autres charges fixes",
            sr_saved.get(annee, {}).get("Autres_CF",0.0),
            format="%.3f",
            key=f"autres_cf_{annee}"
        )
        charges_fixes = loyer + salaires + autres_cf

        resultats[annee] = calcul_seuil_rentabilite(CA, charges_variables, charges_fixes)

    st.session_state["seuil_rentabilite"] = resultats  # ✅ Stockage inter-pages

    # =========================
    # Tableau récapitulatif
    # =========================
    df = pd.DataFrame({
        "Rubrique": [
            "Chiffre d'affaires HT (CA)",
            "Charges variables (CV)",
            "Charges fixes (CF)",
            "Charges totales (CV + CF)",
            "Marge",
            "Marge sur coût variable (MCV)",
            "Taux de MCV (%)",
            "Seuil de rentabilité (CA)"
        ],
        "Année 1": [resultats["Année 1"]["CA"], resultats["Année 1"]["CV"], resultats["Année 1"]["CF"],
                     resultats["Année 1"]["Charges_totales"], resultats["Année 1"]["Marge"], resultats["Année 1"]["MCV"],
                     resultats["Année 1"]["Taux_MCV"], resultats["Année 1"]["Seuil"]],
        "Année 2": [resultats["Année 2"]["CA"], resultats["Année 2"]["CV"], resultats["Année 2"]["CF"],
                     resultats["Année 2"]["Charges_totales"], resultats["Année 2"]["Marge"], resultats["Année 2"]["MCV"],
                     resultats["Année 2"]["Taux_MCV"], resultats["Année 2"]["Seuil"]],
        "Année 3": [resultats["Année 3"]["CA"], resultats["Année 3"]["CV"], resultats["Année 3"]["CF"],
                     resultats["Année 3"]["Charges_totales"], resultats["Année 3"]["Marge"], resultats["Année 3"]["MCV"],
                     resultats["Année 3"]["Taux_MCV"], resultats["Année 3"]["Seuil"]]
    })

    st.subheader("Tableau du Seuil de Rentabilité")
    st.dataframe(df.style.format({
        "Année 1": "{:,.3f} F CFA",
        "Année 2": "{:,.3f} F CFA",
        "Année 3": "{:,.3f} F CFA"
    }))
