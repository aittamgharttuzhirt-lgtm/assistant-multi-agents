"""
FreelanceAI Assistant - Interface Streamlit
Application d'accompagnement des freelances avec système multi-agent
"""

import streamlit as st
import os
import sys
from datetime import datetime
import json
from dotenv import load_dotenv
import re

# Fix pour l'encodage UTF-8 sur Windows
if sys.platform == 'win32':
    import locale
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

# Import du backend CrewAI
from agents_crew import execute_crew

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="FreelanceAI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E40AF;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E3A8A;
        transform: translateY(-2px);
    }
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #1E40AF;
    }
    .result-section {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .header-title {
        color: #1E40AF;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        color: #64748B;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation du session state
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}

if 'results' not in st.session_state:
    st.session_state.results = {
        'positioning': None,
        'finance': None,
        'marketing': None
    }

if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'positioning': 'ready',  # ready, running, completed
        'finance': 'ready',
        'marketing': 'ready'
    }

# Fonction pour sauvegarder les résultats
def save_results(agent_type, content):
    """Sauvegarde les résultats d'un agent"""
    # Nettoyer le contenu avant de le sauvegarder
    cleaned_content = clean_text(content) if content else content
    st.session_state.results[agent_type] = cleaned_content
    st.session_state.agent_status[agent_type] = 'completed'

# Fonction pour nettoyer le texte des caractères problématiques
def clean_text(text):
    """Nettoie le texte des caractères Unicode problématiques"""
    if text is None:
        return ""
    # Remplacer les caractères Unicode problématiques
    text = str(text)
    # Remplacer certains emojis problématiques par des équivalents ASCII
    replacements = {
        '\U0001f539': '•',  # Blue diamond
        '\U0001f538': '◆',  # Orange diamond
        '\U0001f537': '◇',  # Blue diamond outline
        '\U0001f536': '▪',  # Large orange diamond
        '\u2022': '•',      # Bullet point
        '\u2023': '‣',      # Triangular bullet
        '\u25aa': '▪',      # Small black square
        '\u25ab': '▫',      # Small white square
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Encoder en UTF-8 et décoder pour gérer les caractères restants
    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    except:
        text = text.encode('ascii', errors='ignore').decode('ascii')
    return text

# Fonction pour formater les résultats
def format_results(content):
    """Formate les résultats pour un meilleur affichage"""
    if content:
        # Nettoyer le texte d'abord
        content = clean_text(content)
        # Diviser le contenu en sections si possible
        sections = content.split('\n\n')
        formatted = ""
        for section in sections:
            if section.strip():
                formatted += f"{section}\n\n"
        return formatted
    return "Aucun résultat disponible"

# SIDEBAR - Formulaire de profil
with st.sidebar:
    st.markdown("## 📝 Profil Freelance")

    # Mode demo
    demo_mode = st.checkbox("🎭 Mode Démo (données pré-remplies)")

    if demo_mode:
        nom_default = "Sophie Martin"
        competences_default = "Développement web, React, Node.js, UX/UI Design"
        experience_default = "5 ans en tant que développeuse full-stack dans une startup"
        objectif_default = "Lancer mon activité freelance"
        revenu_default = 5000
        secteur_default = "Tech & Digital"
    else:
        nom_default = ""
        competences_default = ""
        experience_default = ""
        objectif_default = "Lancer mon activité"
        revenu_default = 4000
        secteur_default = "Tech & Digital"

    # Formulaire
    with st.form("profile_form"):
        nom = st.text_input("👤 Nom", value=nom_default)

        competences = st.text_area(
            "💡 Compétences (séparées par des virgules)",
            value=competences_default,
            help="Ex: Développement web, Python, Data Science"
        )

        experience = st.text_area(
            "🎓 Expérience",
            value=experience_default,
            help="Décrivez votre parcours professionnel"
        )

        objectif = st.selectbox(
            "🎯 Objectif principal",
            ["Lancer mon activité", "Trouver mes premiers clients", "Augmenter mon CA", "Me spécialiser"],
            index=0 if not demo_mode else 0
        )

        revenu_cible = st.number_input(
            "💰 Revenu cible mensuel (€)",
            min_value=1000,
            max_value=20000,
            value=revenu_default,
            step=500
        )

        secteur = st.selectbox(
            "🏢 Secteur d'activité",
            ["Tech & Digital", "Marketing & Communication", "Conseil & Formation", "Design & Créatif", "Autre"],
            index=0
        )

        submitted = st.form_submit_button("💾 Sauvegarder le profil")

        if submitted:
            st.session_state.profile_data = {
                'nom': nom,
                'competences': [c.strip() for c in competences.split(',')],
                'experience': experience,
                'objectif': objectif,
                'revenu_cible': revenu_cible,
                'secteur': secteur
            }
            st.success("✅ Profil sauvegardé!")

# MAIN CONTENT
# Header
st.markdown('<h1 class="header-title">🚀 FreelanceAI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Votre copilote IA pour réussir en freelance</p>', unsafe_allow_html=True)

# Vérification du profil
if not st.session_state.profile_data:
    st.warning("⚠️ Veuillez d'abord remplir votre profil dans la barre latérale")
    st.stop()

# Affichage du profil actuel
with st.expander("👤 Profil actuel", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Nom:** {st.session_state.profile_data.get('nom', 'N/A')}")
        st.markdown(f"**Secteur:** {st.session_state.profile_data.get('secteur', 'N/A')}")
    with col2:
        st.markdown(f"**Objectif:** {st.session_state.profile_data.get('objectif', 'N/A')}")
        st.markdown(f"**Revenu cible:** {st.session_state.profile_data.get('revenu_cible', 0)}€/mois")
    with col3:
        competences_str = ', '.join(st.session_state.profile_data.get('competences', [])[:3])
        if len(st.session_state.profile_data.get('competences', [])) > 3:
            competences_str += '...'
        st.markdown(f"**Compétences:** {competences_str}")

# Séparateur
st.markdown("---")

# Dashboard des agents
st.markdown("## 🤖 Agents IA Disponibles")

# Création des 3 colonnes pour les agents
col1, col2, col3 = st.columns(3)

# Agent 1: Positionnement & Offre
with col1:
    st.markdown("""
    <div class="agent-card">
        <h3>🎯 Positionnement & Offre</h3>
        <p>Clarifiez votre positionnement et créez une offre irrésistible</p>
    </div>
    """, unsafe_allow_html=True)

    # Status
    status = st.session_state.agent_status['positioning']
    if status == 'ready':
        status_text = "🟢 Prêt"
    elif status == 'running':
        status_text = "🔄 En cours..."
    else:
        status_text = "✅ Terminé"

    st.markdown(f"**Status:** {status_text}")

    # Bouton d'exécution
    if st.button("🚀 Lancer l'analyse", key="btn_positioning", disabled=(status == 'running')):
        with st.spinner("🔄 L'agent analyse votre profil et le marché..."):
            st.session_state.agent_status['positioning'] = 'running'

            # Appel au backend
            result = execute_crew(st.session_state.profile_data, 'positioning')

            # Sauvegarde des résultats
            save_results('positioning', result)
            st.success("✅ Analyse terminée!")
            st.rerun()

# Agent 2: Fiscalité & Trésorerie
with col2:
    st.markdown("""
    <div class="agent-card">
        <h3>💼 Fiscalité & Trésorerie</h3>
        <p>Optimisez votre statut et sécurisez votre trésorerie</p>
    </div>
    """, unsafe_allow_html=True)

    # Status
    status = st.session_state.agent_status['finance']
    if status == 'ready':
        status_text = "🟢 Prêt"
    elif status == 'running':
        status_text = "🔄 En cours..."
    else:
        status_text = "✅ Terminé"

    st.markdown(f"**Status:** {status_text}")

    # Bouton d'exécution
    if st.button("🚀 Analyser ma situation", key="btn_finance", disabled=(status == 'running')):
        with st.spinner("🔄 L'agent analyse votre situation fiscale..."):
            st.session_state.agent_status['finance'] = 'running'

            # Appel au backend
            result = execute_crew(st.session_state.profile_data, 'finance')

            # Sauvegarde des résultats
            save_results('finance', result)
            st.success("✅ Analyse fiscale terminée!")
            st.rerun()

# Agent 3: Visibilité & Prospection
with col3:
    st.markdown("""
    <div class="agent-card">
        <h3>📢 Visibilité & Prospection</h3>
        <p>Développez votre visibilité et trouvez vos clients</p>
    </div>
    """, unsafe_allow_html=True)

    # Status
    status = st.session_state.agent_status['marketing']
    if status == 'ready':
        status_text = "🟢 Prêt"
    elif status == 'running':
        status_text = "🔄 En cours..."
    else:
        status_text = "✅ Terminé"

    st.markdown(f"**Status:** {status_text}")

    # Bouton d'exécution
    if st.button("🚀 Créer ma stratégie", key="btn_marketing", disabled=(status == 'running')):
        with st.spinner("🔄 L'agent prépare votre stratégie marketing..."):
            st.session_state.agent_status['marketing'] = 'running'

            # Appel au backend
            result = execute_crew(st.session_state.profile_data, 'marketing')

            # Sauvegarde des résultats
            save_results('marketing', result)
            st.success("✅ Stratégie marketing créée!")
            st.rerun()

# Bouton pour lancer tous les agents
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Lancer tous les agents", type="primary"):
        with st.spinner("🔄 Analyse complète en cours... (peut prendre 2-3 minutes)"):
            # Exécuter chaque agent séparément pour avoir des résultats distincts
            agents_to_run = ['positioning', 'finance', 'marketing']
            progress_text = st.empty()

            for i, agent in enumerate(agents_to_run):
                progress_text.text(f"Agent {i+1}/3: {agent.capitalize()}...")
                st.session_state.agent_status[agent] = 'running'

                # Appel au backend pour chaque agent individuellement
                result = execute_crew(st.session_state.profile_data, agent)

                # Sauvegarder le résultat spécifique de cet agent
                save_results(agent, result)
                st.session_state.agent_status[agent] = 'completed'

            progress_text.empty()
            st.success("✅ Analyse complète terminée!")
            st.rerun()

# Section des résultats
st.markdown("---")
st.markdown("## 📊 Résultats")

# Tabs pour organiser les résultats
tab1, tab2, tab3 = st.tabs(["🎯 Positionnement", "💼 Fiscalité", "📢 Marketing"])

# Tab 1: Résultats Positionnement
with tab1:
    if st.session_state.results['positioning']:
        st.markdown("### 🎯 Analyse de Positionnement & Offre")

        # Affichage formaté des résultats
        with st.expander("📋 Résultats complets", expanded=True):
            st.markdown(format_results(st.session_state.results['positioning']))

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger les résultats (TXT)",
            data=st.session_state.results['positioning'],
            file_name=f"positionnement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("ℹ️ Lancez l'agent Positionnement pour voir les résultats")

# Tab 2: Résultats Fiscalité
with tab2:
    if st.session_state.results['finance']:
        st.markdown("### 💼 Analyse Fiscale & Trésorerie")

        # Affichage formaté des résultats
        with st.expander("📋 Résultats complets", expanded=True):
            st.markdown(format_results(st.session_state.results['finance']))

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger les résultats (TXT)",
            data=st.session_state.results['finance'],
            file_name=f"fiscalite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("ℹ️ Lancez l'agent Fiscalité pour voir les résultats")

# Tab 3: Résultats Marketing
with tab3:
    if st.session_state.results['marketing']:
        st.markdown("### 📢 Stratégie Marketing & Prospection")

        # Affichage formaté des résultats
        with st.expander("📋 Résultats complets", expanded=True):
            st.markdown(format_results(st.session_state.results['marketing']))

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger les résultats (TXT)",
            data=st.session_state.results['marketing'],
            file_name=f"marketing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("ℹ️ Lancez l'agent Marketing pour voir les résultats")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 2rem;">
    <p>🚀 FreelanceAI Assistant - Propulsé par CrewAI & OpenAI</p>
    <p style="font-size: 0.9rem;">Développé avec ❤️ pour accompagner les freelances</p>
</div>
""", unsafe_allow_html=True)

# Section d'aide dans la sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### ❓ Aide")
    with st.expander("Comment utiliser l'application"):
        st.markdown("""
        1. **Remplissez votre profil** avec vos informations
        2. **Choisissez un agent** ou lancez-les tous
        3. **Consultez les résultats** dans les onglets
        4. **Téléchargez** vos résultats pour les conserver

        **Tips:**
        - Utilisez le mode démo pour tester rapidement
        - Les analyses prennent 1-2 minutes par agent
        - Les résultats sont sauvegardés dans votre session
        """)

    # Bouton de reset
    if st.button("🔄 Réinitialiser tout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()