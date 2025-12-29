# -*- coding: utf-8 -*-
import streamlit as st
from database import save_module_data, load_module_data

def run():
    st.title("HYPOTHÈSES D'ACTIVITÉ")
    st.subheader("Hypothèses de base – Année 1")

    # =========================
    # CHARGER LES DONNÉES EN SESSION
    # =========================
    saved_hyp = load_module_data(module="hypotheses", annee="1") or {}

    if "hypotheses" not in st.session_state:
        st.session_state["hypotheses"] = {
            "panier": saved_hyp.get("panier", 50.0),
            "clients": saved_hyp.get("clients", 20.0),
            "jours_an": saved_hyp.get("jours_an", 312.0),
            "ca_ht": saved_hyp.get("ca_ht", 0.0),
            "salaires_indiv": saved_hyp.get("salaires_indiv", 2000.0),
            "salaires_emp": saved_hyp.get("salaires_emp", 5000.0),
            "stock": saved_hyp.get("stock", 10000.0),
            "loyer": saved_hyp.get("loyer", 1500.0)
        }

    h = st.session_state["hypotheses"]

    with st.form("form_hypotheses"):
        st.header("Saisie des hypothèses")
        panier = st.number_input("Panier moyen / jour", value=h["panier"], format="%.3f")
        clients = st.number_input("Nombre de clients / jour", value=h["clients"], format="%.3f")
        jours_an = st.number_input("Nombre de jours d’ouverture / an", value=h["jours_an"], format="%.3f")
        ca_ht = panier * clients * jours_an
        st.number_input("Chiffre d'affaires HT annuel", value=ca_ht, format="%.3f", disabled=True)
        salaires_indiv = st.number_input("Salaires prélevés à titre individuel", value=h["salaires_indiv"], format="%.3f")
        salaires_emp = st.number_input("Salaires des salariés", value=h["salaires_emp"], format="%.3f")
        stock = st.number_input("Stock moyen", value=h["stock"], format="%.3f")
        loyer = st.number_input("Loyer annuel", value=h["loyer"], format="%.3f")

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            st.session_state["hypotheses"].update({
                "panier": panier,
                "clients": clients,
                "jours_an": jours_an,
                "ca_ht": ca_ht,
                "salaires_indiv": salaires_indiv,
                "salaires_emp": salaires_emp,
                "stock": stock,
                "loyer": loyer
            })

            # Sauvegarde en base
            save_module_data(module="hypotheses", annee="1", data=st.session_state["hypotheses"])
            # Sauvegarde en session pour interconnexion
            st.session_state["hypotheses_saved"] = st.session_state["hypotheses"]
            st.success("Hypothèses enregistrées avec succès")
