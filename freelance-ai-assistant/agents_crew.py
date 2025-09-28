"""
Backend CrewAI - Système Multi-Agent pour Freelances
"""

import os
import sys
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from typing import Dict, Any

# Fix pour l'encodage UTF-8 sur Windows
if sys.platform == 'win32':
    import locale
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

class FreelanceCrew:
    """Orchestrateur du système multi-agent pour l'accompagnement des freelances"""

    def __init__(self):
        """Initialisation des outils et configuration"""
        # Récupération des clés API depuis le fichier .env
        from dotenv import load_dotenv
        load_dotenv()

        # Configuration des clés API
        os.environ['OPENAI_API_KEY'] = "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"
        os.environ['SERPER_API_KEY'] = "bc1bd438793d6bb90a2fe3cfdb273f5740116b12"

        # Initialisation des outils
        try:
            self.search_tool = SerperDevTool()
            self.scrape_tool = ScrapeWebsiteTool()
            self.tools = [self.search_tool, self.scrape_tool]
        except Exception as e:
            print(f"Erreur lors de l'initialisation des outils: {e}")
            self.tools = []

    def create_agents(self) -> Dict[str, Agent]:
        """Création des trois agents IA spécialisés"""

        agents = {}

        # 🎯 Agent 1: Positionnement & Offre
        agents['positioning'] = Agent(
            role="Expert en Positionnement et Marketing Freelance",
            goal="Aider le freelance à clarifier sa cible, son offre et à se différencier dans un marché concurrentiel",
            backstory="""Vous êtes un expert en stratégie de positionnement avec 15 ans d'expérience
            dans l'accompagnement de freelances. Vous excellez dans l'identification de niches rentables,
            la création de propositions de valeur uniques et l'optimisation de la visibilité professionnelle.
            Votre approche est pragmatique et orientée résultats.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools
        )

        # 💼 Agent 2: Statut, Fiscalité & Trésorerie
        agents['finance'] = Agent(
            role="Expert en Fiscalité et Gestion Financière pour Freelances",
            goal="Aider le freelance à choisir le bon statut, anticiper les charges et simuler les revenus pour sécuriser son activité",
            backstory="""Vous êtes un conseiller expert en droit social et fiscalité des indépendants.
            Avec une expertise pointue des différents statuts juridiques français (micro-entreprise, SASU, EURL),
            vous aidez les freelances à optimiser leur situation fiscale et à sécuriser leur trésorerie.
            Vous êtes précis, pédagogue et toujours à jour des dernières réglementations.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools
        )

        # 📢 Agent 3: Visibilité & Prospection
        agents['marketing'] = Agent(
            role="Expert en Marketing Digital et Prospection B2B",
            goal="Accompagner le freelance dans l'acquisition de visibilité et la recherche de clients",
            backstory="""Vous êtes un spécialiste du marketing digital et de la prospection commerciale
            avec une expertise spécifique pour les freelances. Vous maîtrisez LinkedIn, l'email marketing,
            et les stratégies de contenu. Votre approche est systématique et orientée conversion,
            avec un focus sur l'acquisition de clients qualifiés.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools
        )

        return agents

    def create_positioning_tasks(self, agents: Dict[str, Agent], profile: Dict[str, Any]) -> list:
        """Création des 7 tâches pour l'agent Positionnement"""

        tasks = []

        # Tâche 1: Identifier la niche
        tasks.append(Task(
            description=f"""Analyser le profil suivant et identifier la niche la plus pertinente:
            - Nom: {profile.get('nom', 'Freelance')}
            - Objectif: {profile.get('objectif', 'Lancer mon activité')}
            - Compétences: {profile.get('competences', [])}
            - Expérience: {profile.get('experience', '')}
            - Secteur: {profile.get('secteur', '')}

            Adapter les recommandations selon l'objectif principal du freelance.
            Identifier une niche spécifique en croisant les compétences avec les tendances du marché actuel.
            Fournir une analyse de la demande et du potentiel de cette niche.""",
            expected_output="Niche identifiée avec justification basée sur les tendances marché et analyse de la demande",
            agent=agents['positioning']
        ))

        # Tâche 2: Définir le persona client
        tasks.append(Task(
            description=f"""Définir précisément le client idéal (persona) pour ce freelance.
            Inclure: profil démographique, besoins principaux, pain points, budget type,
            critères de décision, canaux de communication préférés.""",
            expected_output="Persona client détaillé avec caractéristiques complètes",
            agent=agents['positioning']
        ))

        # Tâche 3: Créer le pitch
        tasks.append(Task(
            description=f"""Créer 3 versions d'un pitch percutant:
            1. Version courte (1 ligne - elevator pitch)
            2. Version moyenne (3-4 lignes - présentation LinkedIn)
            3. Version longue (1 paragraphe - présentation détaillée)

            Le pitch doit être orienté bénéfices clients et différenciant.""",
            expected_output="3 versions de pitch adaptées à différents contextes",
            agent=agents['positioning']
        ))

        # Tâche 4: Bio LinkedIn optimisée
        tasks.append(Task(
            description=f"""Rédiger une bio LinkedIn optimisée pour {profile.get('nom', 'le freelance')}.
            La bio doit:
            - Accrocher dès la première ligne
            - Mettre en avant la proposition de valeur unique
            - Inclure des mots-clés pertinents pour le SEO LinkedIn
            - Avoir un CTA clair
            - Faire maximum 2000 caractères""",
            expected_output="Bio LinkedIn complète et optimisée SEO",
            agent=agents['positioning']
        ))

        # Tâche 5: Description des services
        tasks.append(Task(
            description="""Transformer l'offre technique en une description de services orientée bénéfices clients.
            Pour chaque service:
            - Nom accrocheur
            - Bénéfices concrets pour le client
            - Résultats attendus
            - Différenciateurs""",
            expected_output="Description de 3-5 services principaux orientés bénéfices",
            agent=agents['positioning']
        ))

        # Tâche 6: Benchmark concurrentiel
        tasks.append(Task(
            description="""Réaliser une analyse rapide de 3 concurrents principaux.
            Pour chaque concurrent identifier:
            - Positionnement
            - Points forts
            - Points faibles
            - Opportunités de différenciation""",
            expected_output="Tableau comparatif avec opportunités de différenciation",
            agent=agents['positioning']
        ))

        # Tâche 7: Simplifier l'offre
        tasks.append(Task(
            description="""Simplifier et améliorer l'offre globale:
            - Reformuler en langage orienté résultats (pas de jargon technique)
            - Structurer en 3 packages/formules clairs
            - Définir les garanties/engagements
            - Proposer une offre d'appel""",
            expected_output="Offre structurée en 3 formules avec pricing indicatif",
            agent=agents['positioning']
        ))

        return tasks

    def create_finance_tasks(self, agents: Dict[str, Agent], profile: Dict[str, Any]) -> list:
        """Création des 7 tâches pour l'agent Fiscalité"""

        tasks = []

        # Tâche 1: Questions orientation statut
        tasks.append(Task(
            description=f"""Pour le profil {profile.get('nom', 'Freelance')} avec:
            - Objectif principal: {profile.get('objectif', 'Lancer mon activité')}
            - Revenu cible: {profile.get('revenu_cible', 4000)}€/mois
            Déterminer les questions clés à poser pour orienter le choix du statut juridique optimal.
            Adapter les conseils selon l'objectif (démarrage, croissance, spécialisation).""",
            expected_output="Liste de 5-7 questions essentielles pour le choix du statut",
            agent=agents['finance']
        ))

        # Tâche 2: Comparatif des statuts
        tasks.append(Task(
            description=f"""Comparer les statuts juridiques adaptés (micro-entreprise, SASU, EURL, portage salarial)
            pour un revenu cible de {profile.get('revenu_cible', 4000)}€/mois.
            Inclure avantages, inconvénients, plafonds, régime fiscal et social.""",
            expected_output="Tableau comparatif détaillé des statuts avec recommandation",
            agent=agents['finance']
        ))

        # Tâche 3: Simulation revenus nets
        tasks.append(Task(
            description=f"""Simuler les revenus nets, cotisations et impôts pour un CA mensuel de
            {profile.get('revenu_cible', 4000) * 1.3}€ selon 3 scénarios:
            1. Micro-entreprise
            2. SASU avec dividendes
            3. EURL à l'IS""",
            expected_output="Simulations chiffrées avec revenus nets après charges et impôts",
            agent=agents['finance']
        ))

        # Tâche 4: Tableau de trésorerie
        tasks.append(Task(
            description="""Générer un tableau de trésorerie prévisionnel sur 6 mois incluant:
            - Entrées (CA prévisionnel avec progression)
            - Sorties (charges fixes, variables, cotisations, impôts)
            - Solde de trésorerie
            - Besoins en fonds de roulement""",
            expected_output="Tableau de trésorerie mois par mois sur 6 mois",
            agent=agents['finance']
        ))

        # Tâche 5: Planning démarches
        tasks.append(Task(
            description="""Créer un planning détaillé des démarches administratives pour créer son activité:
            - Étapes dans l'ordre chronologique
            - Documents nécessaires
            - Délais moyens
            - Coûts associés
            - Organismes à contacter""",
            expected_output="Checklist chronologique des démarches avec détails pratiques",
            agent=agents['finance']
        ))

        # Tâche 6: Rappels fiscaux
        tasks.append(Task(
            description="""Établir un calendrier des obligations fiscales et sociales sur 12 mois:
            - Dates de déclaration et paiement
            - Cotisations sociales
            - TVA si applicable
            - Impôts
            - CFE
            Avec système d'alertes recommandé""",
            expected_output="Calendrier annuel avec dates clés et montants estimés",
            agent=agents['finance']
        ))

        # Tâche 7: Conseils et erreurs
        tasks.append(Task(
            description="""Identifier:
            1. Les 5 principales aides disponibles pour les freelances débutants
            2. Les 7 erreurs fiscales/administratives les plus courantes à éviter
            3. Les 3 optimisations fiscales légales recommandées""",
            expected_output="Guide pratique des aides, erreurs à éviter et optimisations",
            agent=agents['finance']
        ))

        return tasks

    def create_marketing_tasks(self, agents: Dict[str, Agent], profile: Dict[str, Any]) -> list:
        """Création des 7 tâches pour l'agent Marketing"""

        tasks = []

        # Tâche 1: Identifier les canaux
        tasks.append(Task(
            description=f"""Pour un freelance {profile.get('secteur', 'tech')} avec l'objectif "{profile.get('objectif', 'Lancer mon activité')}",
            identifier les 5 canaux de visibilité les plus pertinents (LinkedIn, Twitter, blog, newsletter, etc.)
            avec justification et priorité adaptées à cet objectif spécifique.""",
            expected_output="Liste priorisée des canaux avec stratégie pour chacun",
            agent=agents['marketing']
        ))

        # Tâche 2: Plan de contenu
        tasks.append(Task(
            description="""Créer un plan de contenu structuré sur 4 semaines incluant:
            - Thématiques par semaine
            - Types de contenu (article, vidéo, infographie, etc.)
            - Fréquence de publication
            - Objectifs par contenu (notoriété, engagement, conversion)""",
            expected_output="Calendrier éditorial détaillé sur 4 semaines",
            agent=agents['marketing']
        ))

        # Tâche 3: Posts LinkedIn
        tasks.append(Task(
            description="""Rédiger 5 posts LinkedIn prêts à publier:
            1. Post de présentation/positionnement
            2. Post éducatif (partage d'expertise)
            3. Post storytelling (retour d'expérience)
            4. Post engagement (question à la communauté)
            5. Post case study/résultats client

            Inclure émojis, hashtags et CTA adaptés.""",
            expected_output="5 posts LinkedIn complets avec formatting et hashtags",
            agent=agents['marketing']
        ))

        # Tâche 4: Templates prospection
        tasks.append(Task(
            description="""Créer 3 templates d'emails de prospection personnalisables:
            1. Cold email première approche
            2. Email de relance
            3. Email de nurturing (partage de valeur)

            Plus 2 templates de messages LinkedIn (connexion et message).""",
            expected_output="5 templates de messages prêts à personnaliser",
            agent=agents['marketing']
        ))

        # Tâche 5: Système de suivi
        tasks.append(Task(
            description="""Organiser un système de suivi des prospects simple:
            - Catégorisation des leads (chaud/tiède/froid)
            - Pipeline de conversion en 5 étapes
            - Indicateurs de suivi (taux d'ouverture, réponse, conversion)
            - Outils recommandés (CRM simple, spreadsheet)""",
            expected_output="Système de suivi structuré avec process et outils",
            agent=agents['marketing']
        ))

        # Tâche 6: Planning relances
        tasks.append(Task(
            description="""Créer une séquence de relances automatiques:
            - Timeline des relances (J+3, J+7, J+14, J+30)
            - Messages types pour chaque relance
            - Critères d'arrêt
            - Automatisation possible avec outils gratuits""",
            expected_output="Séquence de relance complète avec messages et timing",
            agent=agents['marketing']
        ))

        # Tâche 7: Métriques et ajustements
        tasks.append(Task(
            description="""Définir les KPIs à suivre et le process d'optimisation:
            - 5 métriques clés à tracker
            - Fréquence d'analyse
            - Process d'A/B testing
            - Ajustements recommandés selon résultats
            - Objectifs réalistes mois par mois""",
            expected_output="Dashboard de KPIs et process d'amélioration continue",
            agent=agents['marketing']
        ))

        return tasks

    def run(self, profile: Dict[str, Any], agent_type: str = 'all') -> str:
        """
        Exécution du crew pour un ou plusieurs agents

        Args:
            profile: Données du profil freelance
            agent_type: Type d'agent à exécuter ('positioning', 'finance', 'marketing', 'all')

        Returns:
            Résultats formatés en string
        """
        try:
            # Création des agents
            agents = self.create_agents()

            # Pour simplifier et éviter les timeouts, on limite à 2 tâches par agent
            tasks = []

            if agent_type == 'positioning':
                positioning_tasks = self.create_positioning_tasks(agents, profile)
                tasks.extend(positioning_tasks[:2])  # Seulement 2 premières tâches
            elif agent_type == 'finance':
                finance_tasks = self.create_finance_tasks(agents, profile)
                tasks.extend(finance_tasks[:2])  # Seulement 2 premières tâches
            elif agent_type == 'marketing':
                marketing_tasks = self.create_marketing_tasks(agents, profile)
                tasks.extend(marketing_tasks[:2])  # Seulement 2 premières tâches
            elif agent_type == 'all':
                # Pour 'all', on prend 1 tâche de chaque agent
                positioning_tasks = self.create_positioning_tasks(agents, profile)
                finance_tasks = self.create_finance_tasks(agents, profile)
                marketing_tasks = self.create_marketing_tasks(agents, profile)
                tasks.extend([positioning_tasks[0], finance_tasks[0], marketing_tasks[0]])

            # Sélection des agents nécessaires
            selected_agents = []
            if agent_type == 'all':
                selected_agents = list(agents.values())
            elif agent_type in agents:
                selected_agents = [agents[agent_type]]

            # Création et exécution du crew
            crew = Crew(
                agents=selected_agents,
                tasks=tasks,
                verbose=True,  # Activer verbose pour voir les détails
                process=Process.sequential
            )

            # Exécution avec timeout implicite
            result = crew.kickoff()

            # Convertir le résultat en string de manière sécurisée
            try:
                result_str = str(result)
                # Nettoyer les caractères Unicode problématiques
                result_str = result_str.encode('utf-8', errors='ignore').decode('utf-8')
                return result_str
            except:
                # Fallback en cas de problème d'encodage
                return str(result).encode('ascii', errors='ignore').decode('ascii')

        except Exception as e:
            # Gérer l'erreur de manière sécurisée
            error_msg = str(e)
            try:
                error_msg = error_msg.encode('utf-8', errors='ignore').decode('utf-8')
            except:
                error_msg = error_msg.encode('ascii', errors='ignore').decode('ascii')
            return f"Erreur lors de l'exécution: {error_msg}"


def execute_crew(profile_data: Dict[str, Any], agent_type: str = 'all') -> str:
    """
    Fonction principale pour exécuter le crew depuis l'interface Streamlit

    Args:
        profile_data: Dictionnaire contenant les données du profil
        agent_type: Type d'agent à exécuter

    Returns:
        Résultats de l'exécution en string
    """
    crew = FreelanceCrew()
    return crew.run(profile_data, agent_type)
