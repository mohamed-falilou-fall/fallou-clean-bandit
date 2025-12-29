# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import altair as alt

def run():
    st.title("Besoin en Fonds de Roulement (BFR)")

    hyp = st.session_state.get("hypotheses_saved", {})
    bfr_saved = st.session_state.get("bfr", {})

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        CA = st.number_input(
            "Chiffre d'affaires HT",
            value=bfr_saved.get(annee, {}).get("CA", hyp.get("ca_ht",0.0)) if annee=="Année 1" else bfr_saved.get(annee, {}).get("CA",0.0),
            format="%.3f",
            key=f"ca_bfr_{annee}"
        )

        achats_pct_CA = st.number_input(
            "Achats consommés + sous-traitance (% du CA HT)",
            value=bfr_saved.get(annee, {}).get("Achats_pct",60.0) if annee=="Année 1" else bfr_saved.get(annee, {}).get("Achats_pct",0.0),
            format="%.3f",
            key=f"achats_pct_{annee}"
        ) / 100.0

        delai_fournisseurs = st.slider(
            "Délai moyen paiement fournisseurs (mois)",
            0.0, 12.0, bfr_saved.get(annee, {}).get("Delai_fournisseurs",1.5),
            key=f"delai_fournisseurs_{annee}"
        )

        stock_matieres = st.slider(
            "Stock matières premières (mois d'achat)",
            0.0, 12.0, bfr_saved.get(annee, {}).get("Stock_matieres",1.0),
            key=f"stock_matieres_{annee}"
        )

        stock_encours = st.slider(
            "Stock produits en cours (mois de cycle fabrication)",
            0.0, 12.0, bfr_saved.get(annee, {}).get("Stock_encours",0.5),
            key=f"stock_encours_{annee}"
        )

        stock_finis = st.slider(
            "Stock produits finis (mois de vente)",
            0.0, 12.0, bfr_saved.get(annee, {}).get("Stock_finis",0.5),
            key=f"stock_finis_{annee}"
        )

        delai_clients = st.slider(
            "Délai moyen règlement clients (mois)",
            0.0, 12.0, bfr_saved.get(annee, {}).get("Delai_clients",2.0),
            key=f"delai_clients_{annee}"
        )

        achats = CA * achats_pct_CA

        stock_montants = {
            "Stock matières": achats * stock_matieres / 12,
            "Produits en cours": achats * stock_encours / 12,
            "Produits finis": CA * stock_finis / 12
        }

        total_stock = sum(stock_montants.values())
        creances_clients = CA * delai_clients / 12
        dettes_fournisseurs = achats * delai_fournisseurs / 12

        total_emplois = total_stock + creances_clients
        total_ressources = dettes_fournisseurs
        BFR = total_emplois - total_ressources

        resultats[annee] = {
            "Stock matières": stock_montants["Stock matières"],
            "Produits en cours": stock_montants["Produits en cours"],
            "Produits finis": stock_montants["Produits finis"],
            "Total stock HT": total_stock,
            "Clients TTC": creances_clients,
            "Total emplois": total_emplois,
            "Fournisseurs TTC": dettes_fournisseurs,
            "Acomptes clients TTC": 0.0,
            "Total ressources": total_ressources,
            "BFR": BFR,
            "CA": CA,
            "Achats_pct": achats_pct_CA*100,
            "Delai_fournisseurs": delai_fournisseurs,
            "Stock_matieres": stock_matieres,
            "Stock_encours": stock_encours,
            "Stock_finis": stock_finis,
            "Delai_clients": delai_clients
        }

    st.session_state["bfr"] = resultats  # ✅ Stockage inter-pages

    df = pd.DataFrame({
        "Rubrique": [
            "Stock matières","Produits en cours","Produits finis","Total stock HT (encours moyen)","Clients TTC (encours moyen)",
            "(1) TOTAL EMPLOIS","Fournisseurs TTC","Acomptes clients TTC","(2) TOTAL RESSOURCES","BESOIN EN FONDS DE ROULEMENT (BFR)"
        ],
        "Année 1": [resultats["Année 1"][r] for r in [
            "Stock matières","Produits en cours","Produits finis","Total stock HT","Clients TTC","Total emplois",
            "Fournisseurs TTC","Acomptes clients TTC","Total ressources","BFR"
        ]],
        "Année 2": [resultats["Année 2"][r] for r in [
            "Stock matières","Produits en cours","Produits finis","Total stock HT","Clients TTC","Total emplois",
            "Fournisseurs TTC","Acomptes clients TTC","Total ressources","BFR"
        ]],
        "Année 3": [resultats["Année 3"][r] for r in [
            "Stock matières","Produits en cours","Produits finis","Total stock HT","Clients TTC","Total emplois",
            "Fournisseurs TTC","Acomptes clients TTC","Total ressources","BFR"
        ]]
    })

    st.subheader("Tableau BFR")
    st.dataframe(df.style.format({
        "Année 1":"{:,.3f} F CFA","Année 2":"{:,.3f} F CFA","Année 3":"{:,.3f} F CFA"
    }))

    df_bfr = df[df["Rubrique"]=="BESOIN EN FONDS DE ROULEMENT (BFR)"]\
        .melt(id_vars="Rubrique", var_name="Année", value_name="Montant")

    chart = alt.Chart(df_bfr).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X("Année:N", title="Année"),
        y=alt.Y("Montant:Q", title="BFR (F CFA)"),
        tooltip=[alt.Tooltip("Année:N"), alt.Tooltip("Montant:Q", format=",.3f")]
    ).properties(title="BFR par année", height=350)

    st.altair_chart(chart, use_container_width=True)
