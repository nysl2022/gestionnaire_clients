TP01 - Gestionnaire de Clients avec Python 
👥 Équipe de développement
Membre	Rôle	Tâches principales
Steve	Développeur backend	• Architecture du module services.py
• Logique métier CRUD
• Gestion JSON & persistance
Fayol	Développeur frontend/UI	• Interface utilisateur main.py
• Menu interactif
• Démonstration automatique

Cours: Structures de données Python
Date: Février 2025
Contexte: TP  Manipulation avancée des structures natives Python
📁 Structure du projet
text

tp01-gestion-client/
│
├── src/
│   ├── 📄 main.py              # Interface utilisateur (Fayol)
│   └── 📄 services.py          # Logique métier (Steve)
│
├── data/
│   └── 📊 clients.json         # Base de données JSON
│
├── outputs/
│   └── 📝 demo_run.txt         # Preuve d'exécution complète
│
└── 📖 README.md                # Documentation du projet

🚀 Installation & exécution
bash

# 1. Cloner le dépôt
git clone https://github.com/ton-username/tp01-gestion-client.git

# 2. Se positionner dans le dossier
cd tp01-gestion-client

# 3. Lancer le programme (Python 3.8+ requis)
cd src
python main.py

🎯 Objectifs atteints
✅ Tâches obligatoires
Fonctionnalité	Implémentée par	Fichier
Structure client (dict)	Steve	services.py
CRUD complet	Steve	services.py
Recherche nom/ville	Steve	services.py
Tri par nom & dépenses	Steve	services.py
Calcul total dépenses	Steve	services.py
Sauvegarde JSON	Steve	services.py
Interface interactive	Fayol	main.py
Démo automatique	Fayol	main.py
🎖️ Bonus réalisés

    ✅ Validation téléphone camerounais (9 chiffres, préfixes 2,3,6,7)

    ✅ Gestion d'erreurs complète (try/except, KeyError)

    ✅ Tags dynamiques & historique d'achats

    ✅ Compatibilité multiplateforme (Windows/Linux/Mac)

    ✅ Documentation exhaustive des concepts Python

📊 Démonstration rapide
python

# Mode démo automatique
python main.py
# → Choisir option 1

# Mode interactif
python main.py
# → Choisir option 2
# → Menu complet avec toutes les opérations CRUD

🛠️ Technologies & compétences
python

# Compétences techniques démontrées
- 🔹 Structures natives: Listes, Tuples, Dictionnaires
- 🔹 Algorithmes: Recherche, Tri, Agrégation
- 🔹 Persistance: JSON, chemins relatifs
- 🔹 UX/UI: Menu interactif, validation
- 🔹 Gestion erreurs: Try/Except, assertions

📝 Preuves de réalisation

    Code source complet - src/ avec architecture modulaire

    Base de données - data/clients.json avec données réelles

    Exécution détaillée - outputs/demo_run.txt (10+ opérations)

    Documentation - Ce README avec spécifications techniques

👨‍🏫 Concepts pédagogiques maîtrisés
python

# Steve a implémenté dans services.py:
- ID auto-incrémenté
- Recherche insensible à la casse (.lower())
- Tri avec lambda functions
- Agrégation avec sum() et compréhensions
- Serialization/deserialization JSON

# Fayol a implémenté dans main.py:
- Interface utilisateur intuitive
- Validation des entrées utilisateur
- Gestion d'état avec boucles while
- Formatage avancé (f-strings, alignement)
- Séparation des préoccupations

📞 Exemple client camerounais
json

{
  "id": 1,
  "nom": "Jean Mbarga",
  "ville": "Yaoundé",
  "telephone": "677123456",
  "tags": ["fidèle", "vip", "entreprise"],
  "historique_achats": [
    ["2025-11-10", 75000],
    ["2025-12-15", 120000]
  ]
}

🏅 Points forts du projet
Steve (services.py)

    Architecture modulaire et réutilisable

    Gestion robuste des erreurs

    Algorithmes optimisés (O(n) pour les recherches)

    Code documenté avec exemples d'utilisation

Fayol (main.py)

    Expérience utilisateur fluide

    Démonstration pédagogique automatique

    Validation des données en temps réel

    Interface professionnelle et intuitive

📈 Statistiques du projet

    Lignes de code: ~500 lignes

    Fonctions: 15+ fonctions

    Tests: 12 scénarios de démo

    Compatibilité: Python 3.8+

    Sans dépendances externes