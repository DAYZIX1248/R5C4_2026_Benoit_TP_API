import streamlit as st
import fixtures

st.set_page_config(page_title="Riot Games - Analyse des files", layout="wide")

# ==========================================
# SIDEBAR : NAVIGATION & FILTRES
# ==========================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller vers :", ["Liste des parties", "Indicateurs"])

st.sidebar.markdown("---")
st.sidebar.subheader("Filtres")
# Les filtres utilisent les fixtures pour générer les options
annee = st.sidebar.selectbox("Année", ["Toutes", "2023", "2024"])
jeu = st.sidebar.selectbox("Jeu", ["Tous"] + [j["nom"] for j in fixtures.FILTRES_JEUX])
serveur = st.sidebar.selectbox("Serveur", ["Tous"] + [s["code"] for s in fixtures.FILTRES_SERVEURS])
file = st.sidebar.selectbox("File", ["Toutes"] + [f["file_nom"] for f in fixtures.FILTRES_FILES])

# ==========================================
# PAGE 1 : LISTE DES PARTIES
# ==========================================
if page == "Liste des parties":
    st.title("Historique des parties")

    # Récupération de la fixture
    data = fixtures.PARTIES_DATA

    # Affichage du tableau de bord
    st.dataframe(data["data"], use_container_width=True)

    # Simulation de la pagination
    st.markdown(f"**Total des résultats :** {data['total']} (Affichage de {data['limit']} éléments)")
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        st.button("Précédent", disabled=(data["offset"] == 0))
    with col2:
        st.button("Suivant")

# ==========================================
# PAGE 2 : INDICATEURS
# ==========================================
elif page == "Indicateurs":
    st.title("Indicateurs de performance")

    # Récupération de la fixture
    ind = fixtures.INDICATEURS_DATA["indicateurs"]
    comp = fixtures.INDICATEURS_DATA["comparaison_n_1"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Volume de parties",
        value=f"{ind['volume_parties']} parties",
        delta=f"{comp['evolution_volume_pct']}% vs N-1"
    )

    col2.metric(
        label="Attente Moyenne",
        value=f"{ind['attente_moyenne_sec']} s",
        delta=f"{comp['evolution_attente_pct']}% vs N-1",
        delta_color="inverse"  # Inverse les couleurs (une baisse d'attente est positive/verte)
    )

    col3.metric(
        label="Attente Maximale",
        value=f"{ind['attente_max_sec']} s",
        delta=None
    )