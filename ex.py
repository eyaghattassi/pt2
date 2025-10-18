import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Configuration de la page ---
st.set_page_config(page_title="Maintenance Prédictive IA", layout="wide")

st.title("🤖 Tableau de Bord - Maintenance Prédictive par IA")
st.markdown("Suivi en temps réel des équipements, prédictions de pannes et indicateurs de performance.")

# --- Simulation de données capteurs ---
np.random.seed(42)
machines = [f"M-{i:02d}" for i in range(1, 11)]

data = pd.DataFrame({
    "Machine": machines,
    "Température (°C)": np.random.randint(60, 100, size=10),
    "Vibration (mm/s)": np.round(np.random.uniform(0.5, 3.5, size=10), 2),
    "Pression (bar)": np.round(np.random.uniform(2.5, 5.0, size=10), 2),
    "Risque de panne (%)": np.random.randint(5, 95, size=10)
})

# --- Statut machine ---
def get_status(risk):
    if risk < 30:
        return "🟢 Normal"
    elif risk < 70:
        return "🟠 Surveiller"
    else:
        return "🔴 Critique"

data["État"] = data["Risque de panne (%)"].apply(get_status)

# --- Section KPI ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Machines surveillées", len(machines))
col2.metric("Machines à risque", (data["Risque de panne (%)"] > 70).sum())
col3.metric("Taux de fiabilité global", f"{100 - data['Risque de panne (%)'].mean():.1f}%")
col4.metric("MTBF estimé", "118 h")

st.markdown("---")

# --- Tableau récapitulatif ---
st.subheader("📊 État des Machines")
st.dataframe(data, use_container_width=True)

# --- Graphique : Risque de panne ---
fig1 = px.bar(
    data.sort_values("Risque de panne (%)", ascending=False),
    x="Machine",
    y="Risque de panne (%)",
    color="État",
    color_discrete_map={"🟢 Normal": "green", "🟠 Surveiller": "orange", "🔴 Critique": "red"},
    title="Risque de panne par machine"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Analyse prédictive (simulée) ---
st.subheader("📈 Analyse Prédictive")
st.markdown("Probabilité de panne dans les prochaines 48 heures (simulation IA).")

time = np.arange(0, 48, 1)
failure_prob = np.exp(-time / np.random.randint(20, 40)) * np.random.uniform(0.8, 1.2, len(time))

fig2 = px.line(
    x=time,
    y=failure_prob,
    labels={"x": "Heures à venir", "y": "Probabilité de panne"},
    title="Évolution de la probabilité de panne (exemple de machine critique)"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Causes les plus fréquentes ---
st.subheader("🔍 Causes les plus probables de panne (selon l'IA)")
causes = pd.DataFrame({
    "Facteur": ["Température", "Vibration", "Pression", "Humidité", "Âge du moteur"],
    "Importance (%)": [42, 31, 15, 7, 5]
})
fig3 = px.pie(causes, names="Facteur", values="Importance (%)", title="Importance des facteurs dans la prédiction")
st.plotly_chart(fig3, use_container_width=True)

# --- Alertes récentes ---
st.subheader("🚨 Historique des alertes")
alertes = pd.DataFrame({
    "Date": ["2025-10-19", "2025-10-18", "2025-10-17"],
    "Machine": ["M-03", "M-07", "M-02"],
    "Type d'anomalie": ["Température élevée", "Vibration anormale", "Pression instable"],
    "Niveau": ["🔴 Urgent", "🟠 Moyen", "🟡 Faible"],
    "Action recommandée": ["Arrêt planifié", "Inspection prévue", "Surveillance"]
})
st.dataframe(alertes, use_container_width=True)

st.markdown("---")
st.caption("🧠 Démonstration : Tableau de bord de maintenance prédictive développé avec Streamlit & Python.")
