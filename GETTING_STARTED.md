# Guide de Démarrage - CrewAI Travel Agents

Ce guide est conçu pour les débutants en Python et en IA agentique. Il vous accompagnera étape par étape pour comprendre et utiliser ce projet CrewAI.

## 🤖 Qu'est-ce que CrewAI ?

**CrewAI** est un framework Python qui permet de créer des équipes d'agents IA qui collaborent pour résoudre des problèmes complexes.

### Concepts de base :

- 🤖 **Agent** : Un "employé virtuel" avec un rôle spécifique (ex: planificateur de voyage)
- 📋 **Task** : Une mission donnée à un agent (ex: "trouve des restaurants à Paris")
- 👥 **Crew** : Une équipe d'agents qui travaillent ensemble
- 🔄 **Flow** : Un workflow qui coordonne plusieurs équipes

## 🏗️ Composants Principaux du Projet

Ce projet simule une **agence de voyage virtuelle** avec 4 agents spécialisés :

### 1. 🗺️ Macro Trip Planner
- **Rôle** : Chef de projet voyage
- **Mission** : Créer l'itinéraire global (2-3 villes principales)
- **Sortie** : Plan macro avec dates et destinations

### 2. 🎯 Activity Planner
- **Rôle** : Guide touristique
- **Mission** : Trouver des activités intéressantes par ville
- **Sortie** : Liste d'activités avec descriptions

### 3. 🍽️ Food Planner
- **Rôle** : Critique gastronomique
- **Mission** : Recommander restaurants et expériences culinaires
- **Sortie** : Guide gastronomique personnalisé

### 4. 🏨 Accommodation Planner
- **Rôle** : Expert hébergement
- **Mission** : Trouver les meilleurs hébergements
- **Sortie** : Options d'hébergement avec prix et avis

## 🛠️ Installation Étape par Étape

### Prérequis
- Python 3.10+ installé
- Accès à internet
- Clé API OpenAI

### Étape 1: Vérifier Python

```bash
# Vérifier la version de Python
python --version
# ou
python3 --version
```

Vous devez avoir Python 3.10 ou plus récent.

### Étape 2: Installer Poetry (gestionnaire de dépendances)

Poetry est comme un "gestionnaire de paquets" pour Python :

```bash
# Sur Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Sur macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

Redémarrer votre terminal après installation.

**Note:** Ce projet contient aussi un `uv.lock`, mais nous utiliserons Poetry pour la simplicité.

### Étape 3: Cloner et préparer le projet

```bash
# Aller dans le dossier du projet
cd crewIA-Travel-agent

# Installer les dépendances
poetry install
```

Cette commande télécharge automatiquement toutes les bibliothèques nécessaires.

⚠️ **Sur Windows** : Si vous rencontrez une erreur concernant "Microsoft Visual C++ 14.0", installez les "Microsoft C++ Build Tools" : https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Étape 4: Configuration des Clés API

Les agents ont besoin d'accéder à des services externes :

1. **Créer un compte OpenAI** : https://platform.openai.com/
2. **Obtenir une clé API** dans votre dashboard OpenAI
3. **Configurer le fichier `.env`** :

Le fichier `.env` existe déjà dans le projet. Ouvrir `.env` et remplir :

```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
OPENAI_MODEL_NAME=gpt-4o-mini
SERPER_API_KEY=              # Optionnel pour étapes 3-5
GOOGLE_MAP_API_KEY=          # Optionnel
LANGTRACE_API_KEY=           # Optionnel
```

⚠️ **Important** : Gardez votre clé API secrète !

## 🚀 Première Exécution

Le projet est organisé en 5 étapes progressives. Commençons par la plus simple :

### Step 1 : Agents de Base

```bash
poetry run step1
```

**Ce qui se passe :**
1. 4 agents se réveillent 🤖 (définis dans `travel_ai/step1/config/agents.yaml`)
2. Chaque agent reçoit sa mission (définie dans `travel_ai/step1/config/tasks.yaml`)
3. Ils travaillent en séquence (un après l'autre)
4. Résultats affichés dans le terminal

**Durée attendue :** 2-3 minutes
**Destination par défaut :** France → Vietnam

### Step 2 : Sortie Structurée

```bash
poetry run step2
```

**Nouveauté :** Les agents renvoient maintenant des données structurées (JSON) au lieu de texte libre.

### Step 3 : Avec Recherche Web

```bash
poetry run step3
```

**Nouveauté :** Les agents peuvent maintenant chercher sur internet pour des informations à jour.

⚠️ **Prérequis** : Clé Serper API nécessaire

### Step 4 : Outils Personnalisés

```bash
poetry run step4
```

**Nouveauté :**
- Lecteur de passeport (OCR)
- Interaction avec l'utilisateur

### Step 5 : Workflow Complet

```bash
poetry run step5
```

**Nouveauté :**
- Workflow interactif
- Gestion d'état avancée
- Sauvegarde JSON finale

## 📁 Comprendre les Résultats

### Fichiers de Sortie

```
project/
├── travel_ai/
│   ├── step1/              # Agents de base
│   │   ├── config/         # agents.yaml, tasks.yaml
│   │   ├── crew.py         # Orchestration des agents
│   │   └── main.py         # Point d'entrée
│   ├── step2/              # Sortie structurée + models/
│   ├── step3/              # Avec outils externes (Serper)
│   ├── step4/              # Outils personnalisés + tools/
│   └── step5/              # Workflow complet + flow.py
└── output/                 # Fichiers de sortie générés
    └── travel_data.json    # Plan complet final (step5)
```

### Exemple de Sortie

```json
{
  "macro_planning": {
    "ordered_cities": [
      {"name": "Ho Chi Minh City", "days": 4},
      {"name": "Hoi An", "days": 3},
      {"name": "Hanoi", "days": 3}
    ]
  },
  "activities": [
    {
      "name": "Visite des Tunnels de Cu Chi",
      "location": "Ho Chi Minh City",
      "description": "Exploration historique..."
    }
  ]
}
```

## 🔧 Personnalisation pour Débutants

### Modifier la Destination

Éditer `travel_ai/step5/flow.py` ligne 33-36 :

```python
def initialize(self):
    self.state.original_country = "France"      # Votre pays
    self.state.destination_country = "Japon"    # Nouvelle destination
    self.state.date = "juillet 2025"            # Vos dates
    self.state.traveler_count = 4               # Nombre de voyageurs
```

De même, vous pouvez modifier les paramètres par défaut dans les autres steps:
- `travel_ai/step1/main.py` ligne 18-21
- `travel_ai/step2/main.py`, `travel_ai/step3/main.py`, `travel_ai/step4/main.py`

### Modifier les Agents

Les comportements des agents sont définis dans les fichiers `config/agents.yaml` :

```yaml
macro_trip_planner:
  role: Macro trip planner
  goal: >
     Créer un plan de voyage qui privilégie la culture locale
  backstory: >
    Vous êtes un expert passionné par l'immersion culturelle...
```

## 🐛 Résolution de Problèmes

### Erreur: "Module not found"

```bash
# Réactiver l'environnement Poetry
poetry shell
poetry install
```

### Erreur: "Invalid API Key"

1. Vérifier que votre clé OpenAI est correcte
2. Vérifier qu'elle commence par `sk-`
3. Vérifier que vous avez des crédits sur votre compte OpenAI

### Erreur: "Rate limit exceeded"

Vous faites trop d'appels API :
1. Attendre quelques minutes
2. Vérifier votre quota OpenAI
3. Passer à un modèle moins coûteux si nécessaire

### Les Agents Donnent des Réponses Bizarres

1. Vérifier vos prompts dans `config/tasks.yaml`
2. Ajuster le modèle (gpt-4 vs gpt-3.5-turbo)
3. Modifier les instructions des agents

## 📚 Pour Aller Plus Loin

### Concepts Python à Apprendre

1. **Décorateurs** (`@agent`, `@task`) : Fonctions qui modifient d'autres fonctions
2. **Classes** : Modèles d'objets (comme `TravelCrew`)
3. **Pydantic** : Validation automatique des données
4. **Async/Await** : Programmation asynchrone

### Concepts CrewAI Avancés

1. **Process Types** : Sequential vs Hierarchical
2. **Memory** : Agents qui se souviennent
3. **Tools Integration** : Connecter APIs externes
4. **Custom LLMs** : Utiliser d'autres modèles qu'OpenAI

### Ressources Recommandées

- [Documentation CrewAI](https://docs.crewai.com/)
- [Python pour débutants](https://python.org/about/gettingstarted/)
- [Pydantic Tutorial](https://docs.pydantic.dev/latest/)
- [OpenAI API Docs](https://platform.openai.com/docs)

## 💡 Idées d'Améliorations

Pour vous exercer, essayez d'ajouter :

1. **Nouvel Agent** : Agent météo qui vérifie la météo
2. **Nouvel Outil** : Intégration API vols (Skyscanner)
3. **Interface Web** : Streamlit ou Gradio pour une interface graphique
4. **Base de Données** : Sauvegarder les voyages dans SQLite
5. **Notifications** : Envoyer le plan par email

## 🆘 Besoin d'Aide ?

1. **Lire les logs** : Poetry affiche des erreurs détaillées
2. **Documentation** : Consulter `CLAUDE.md` pour les détails techniques
3. **Community** : Discord CrewAI, StackOverflow
4. **Issues** : Créer une issue GitHub si bug persistant

---

**Bon voyage avec vos agents IA ! 🌍✈️🤖**