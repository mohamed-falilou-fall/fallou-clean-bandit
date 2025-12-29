# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

def run():
    st.title("Export & restitution professionnelle")

    st.markdown("### Synthèse financière")
    hyp = st.session_state.get("hypotheses", {})
    cr = st.session_state.get("compte_resultat", {}).get("Année 1", {})

    chiffre_affaires = hyp.get("Chiffre d'affaires HT (1 x 2 x 3)", 0.0)
    charges = cr.get("Charges totales", 0.0)
    RN = cr.get("Résultat net (RN)", 0.0)
    CAF = cr.get("Capacité d'autofinancement", 0.0)

    df_synthese = pd.DataFrame({
        "Indicateur": ["Chiffre d'affaires", "Charges totales", "Résultat net", "CAF"],
        "Valeur (F CFA)": [chiffre_affaires, charges, RN, CAF]
    })

    st.dataframe(df_synthese.style.format({"Valeur (F CFA)": "{:,.3f}"}))

    fig = px.bar(df_synthese, x="Indicateur", y="Valeur (F CFA)",
                 title="Synthèse financière – vue investisseur")
    st.plotly_chart(fig, use_container_width=True)

    # Export Excel
    st.markdown("### Export Excel")
    def export_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Synthèse")
        return output.getvalue()

    excel_data = export_excel(df_synthese)
    st.download_button(label="Télécharger le rapport Excel",
                       data=excel_data,
                       file_name="Synthese_Financiere.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Export PDF (structure)
    st.markdown("### Export PDF")
    st.info("Le PDF peut être généré à partir de cette synthèse via ReportLab ou WeasyPrint (HTML → PDF).")
    st.success("Module d’export prêt pour restitution investisseurs / banques")

    # Sauvegarde synthèse dans session_state
    st.session_state["synthese_financiere"] = {
        "Chiffre_affaires": chiffre_affaires,
        "Charges": charges,
        "RN": RN,
        "CAF": CAF
    }
