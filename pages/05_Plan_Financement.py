# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("Plan de financement")

    hyp = st.session_state.get("hypotheses_saved", {})
    bfr_module = st.session_state.get("bfr", {})
    cr_module = st.session_state.get("compte_resultat", {})
    plan_saved = st.session_state.get("plan_financement", {})

    annees = ["Année 1","Année 2","Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        st.markdown("**EMPLOIS**")
        immobilisations_incorporelles = st.number_input("Immobilisations incorporelles HT", value=plan_saved.get(annee, {}).get("Immobilisations_incorporelles",0.0), format="%.3f", key=f"immobilisations_incorp_{annee}")
        frais_etablissement = st.number_input("Frais de premier établissement", value=plan_saved.get(annee, {}).get("Frais_etablissement",0.0), format="%.3f", key=f"frais_etab_{annee}")
        recherche_dev = st.number_input("Recherche et développement", value=plan_saved.get(annee, {}).get("Recherche_dev",0.0), format="%.3f", key=f"rd_{annee}")
        fonds_commerce = st.number_input("Fonds de commerce", value=plan_saved.get(annee, {}).get("Fonds_commerce",0.0), format="%.3f", key=f"fonds_commerce_{annee}")
        droit_bail = st.number_input("Droit au bail", value=plan_saved.get(annee, {}).get("Droit_bail",0.0), format="%.3f", key=f"droit_bail_{annee}")
        immobilisations_corporelles = st.number_input("Immobilisations corporelles HT", value=plan_saved.get(annee, {}).get("Immobilisations_corporelles",0.0), format="%.3f", key=f"immobilisations_corp_{annee}")
        terrains = st.number_input("Terrains", value=plan_saved.get(annee, {}).get("Terrains",0.0), format="%.3f", key=f"terrains_{annee}")
        batiments = st.number_input("Bâtiments", value=plan_saved.get(annee, {}).get("Batiments",0.0), format="%.3f", key=f"batiments_{annee}")
        frais_installation = st.number_input("Frais d'installation et d'aménagements", value=plan_saved.get(annee, {}).get("Frais_installation",0.0), format="%.3f", key=f"frais_install_{annee}")
        materiel_info = st.number_input("Matériel informatique et outillage", value=plan_saved.get(annee, {}).get("Materiel_info",0.0), format="%.3f", key=f"materiel_info_{annee}")
        materiel_bureau = st.number_input("Matériel de bureau et mobilier", value=plan_saved.get(annee, {}).get("Materiel_bureau",0.0), format="%.3f", key=f"materiel_bureau_{annee}")

        bfr_val = st.number_input("Besoin en fonds de roulement", value=bfr_module.get(annee, {}).get("BFR",0.0) if bfr_module else 0.0, format="%.3f", key=f"bfr_{annee}")
        distribution_dividendes = st.number_input("Distribution de dividendes", value=plan_saved.get(annee, {}).get("Dividendes",0.0), format="%.3f", key=f"dividendes_{annee}")
        remboursement_emprunts = st.number_input("Remboursement emprunts (capital)", value=plan_saved.get(annee, {}).get("Remboursement_emprunts",0.0), format="%.3f", key=f"remb_emprunts_{annee}")

        total_emplois = sum([immobilisations_incorporelles,frais_etablissement,recherche_dev,fonds_commerce,droit_bail,
                             immobilisations_corporelles,terrains,batiments,frais_installation,materiel_info,materiel_bureau,
                             bfr_val,distribution_dividendes,remboursement_emprunts])

        st.markdown("**RESSOURCES**")
        capitaux_propres_nature = st.number_input("Capitaux propres en nature", value=plan_saved.get(annee, {}).get("Capitaux_nature",0.0), format="%.3f", key=f"capitaux_nature_{annee}")
        capitaux_propres_numeraire = st.number_input("Capitaux propres en numéraire", value=plan_saved.get(annee, {}).get("Capitaux_numeraire",0.0), format="%.3f", key=f"capitaux_num_{annee}")
        subventions = st.number_input("Subventions d'équipement", value=plan_saved.get(annee, {}).get("Subventions",0.0), format="%.3f", key=f"subventions_{annee}")
        comptes_associes = st.number_input("Comptes courants d'associés", value=plan_saved.get(annee, {}).get("Comptes_associes",0.0), format="%.3f", key=f"comptes_associes_{annee}")
        emprunts = st.number_input("Emprunts bancaires", value=plan_saved.get(annee, {}).get("Emprunts",0.0), format="%.3f", key=f"emprunts_{annee}")

        total_ressources = sum([capitaux_propres_nature,capitaux_propres_numeraire,subventions,comptes_associes,emprunts])

        resultats[annee] = {
            "Total_emplois": total_emplois,
            "Total_ressources": total_ressources,
            "Detail": {
                "Immobilisations_incorporelles": immobilisations_incorporelles,
                "Frais_etablissement": frais_etablissement,
                "Recherche_dev": recherche_dev,
                "Fonds_commerce": fonds_commerce,
                "Droit_bail": droit_bail,
                "Immobilisations_corporelles": immobilisations_corporelles,
                "Terrains": terrains,
                "Batiments": batiments,
                "Frais_installation": frais_installation,
                "Materiel_info": materiel_info,
                "Materiel_bureau": materiel_bureau,
                "BFR": bfr_val,
                "Dividendes": distribution_dividendes,
                "Remboursement_emprunts": remboursement_emprunts,
                "Capitaux_nature": capitaux_propres_nature,
                "Capitaux_numeraire": capitaux_propres_numeraire,
                "Subventions": subventions,
                "Comptes_associes": comptes_associes,
                "Emprunts": emprunts
            }
        }

    st.session_state["plan_financement"] = resultats
    st.success("Plan de financement enregistré et prêt à être utilisé dans toutes les autres pages.")
