#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP01 - Gestionnaire de clients
Un petit programme pour gérer des clients avec des structures Python de base
"""

import os
import sys
from datetime import datetime

# Import des fonctions que j'ai codées
from services import (
    charger_clients, sauvegarder_clients, ajouter_client,
    modifier_client, supprimer_client, rechercher_par_nom,
    rechercher_par_ville, trier_par_nom, trier_par_total_achat,
    total_depense_client
)

# CONCEPT IMPORTANT : Chemins relatifs/absolus
# Je définis le chemin vers le fichier de données en utilisant os.path.join 
# pour une compatibilité multiplateforme (Windows/Linux/Mac)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "clients.json")

# Gestion du fichier : création du dossier s'il n'existe pas
# CONCEPT : Gestion des erreurs de système de fichiers
if not os.path.exists(os.path.dirname(DATA_FILE)):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def afficher_un_client(client, details=False):
    """Affiche un client de manière lisible"""
    # CONCEPT : Fonction qui calcule une valeur (dépense totale)
    total = total_depense_client(client)
    
    # CONCEPT : Formatage de chaînes avec f-strings et alignement
    ligne = f"ID:{client['id']} | {client['nom']:15} | {client['ville']:10}"
    ligne += f" | Tél: {client['telephone']}"
    
    # CONCEPT : Méthode get() avec valeur par défaut pour éviter KeyError
    if client.get('tags'):
        # CONCEPT : Transformation de liste en chaîne avec join()
        ligne += f" | Tags: {','.join(client['tags'])}"
    
    ligne += f" | Total: {total} FCFA"
    print(ligne)
    
    # CONCEPT : Slicing de liste pour afficher seulement les N derniers éléments
    if details and client.get('historique_achats'):
        print("   Achats:")
        for date, montant in client['historique_achats'][-3:]:  # 3 derniers seulement
            print(f"     - {date}: {montant} FCFA")


def afficher_tous(clients):
    """Affiche tous les clients"""
    print("\n" + "="*60)
    print(f"LISTE DES CLIENTS ({len(clients)} total)")
    print("="*60)
    
    # CONCEPT : Vérification de liste vide
    if not clients:
        print("Aucun client enregistré pour le moment.")
        return
    
    for client in clients:
        afficher_un_client(client)
    
    # CONCEPT : Compréhension de liste et fonction sum() pour calculs
    total_general = sum(total_depense_client(c) for c in clients)
    print(f"\nTotal général des dépenses: {total_general} FCFA")
    # CONCEPT : Opérateur ternaire implicite pour éviter la division par zéro
    print(f"Moyenne par client: {total_general//len(clients) if clients else 0} FCFA")


def demo_automatique():
    """Une démo automatique pour montrer que tout fonctionne"""
    print("\n" + "*"*60)
    print("DÉMONSTRATION AUTOMATIQUE DES FONCTIONNALITÉS")
    print("*"*60)
    
    # CONCEPT : Persistance des données - chargement depuis un fichier JSON
    clients = charger_clients(DATA_FILE)
    print(f"1. Chargement: {len(clients)} clients trouvés")
    
    # CONCEPT : Initialisation des données si fichier vide (premier lancement)
    if len(clients) == 0:
        print("\n2. Création de 3 clients de démo...")
        
        # Client 1 - Un client avec plusieurs achats
        # CONCEPT : Appel de fonction avec plusieurs arguments
        c1 = ajouter_client(
            clients,
            "Jean Mbarga",
            "Yaoundé",
            "677123456",
            ["fidèle", "vip", "entreprise"]
        )
        # CONCEPT : Modification directe d'un dictionnaire (historique d'achats)
        c1["historique_achats"] = [
            ("2025-11-10", 75000),
            ("2025-12-15", 120000),
            ("2026-01-05", 85000)
        ]
        
        # Client 2 - Un client récent
        c2 = ajouter_client(
            clients,
            "Marie Ngo",
            "Douala", 
            "699887766",
            ["nouveau", "whatsapp", "particulier"]
        )
        c2["historique_achats"] = [
            ("2026-02-01", 45000),
            ("2026-02-03", 35000)
        ]
        
        # Client 3 - Un client sans tags
        c3 = ajouter_client(
            clients,
            "Paul Tchouassi",
            "Bafoussam",
            "623456789",
            []  # CONCEPT : Liste vide pour les tags
        )
        c3["historique_achats"] = [
            ("2026-01-20", 125000)
        ]
        
        print(f"   {len(clients)} clients  créés")
    
    # Affichage initial
    afficher_tous(clients)
    
    # CONCEPT : Recherche insensible à la casse (lower())
    print("\n3. Test de recherche par nom (recherche: 'jean')")
    resultats = rechercher_par_nom(clients, "jean")
    if resultats:
        for client in resultats:
            afficher_un_client(client, details=True)
    else:
        print("   Aucun résultat")
    
    # Recherche par ville
    print("\n4. Test de recherche par ville (recherche: 'yaoundé')")
    resultats = rechercher_par_ville(clients, "yaoundé")
    if resultats:
        for client in resultats:
            afficher_un_client(client)
    else:
        print("   Aucun résultat")
    
    # CONCEPT : Tri avec fonction lambda comme clé de tri
    print("\n5. Tri par ordre alphabétique du nom")
    tries = trier_par_nom(clients)
    for client in tries:
        print(f"   - {client['nom']}")
    
    # Tri par dépenses
    print("\n6. Tri par montant total dépensé (du plus grand au plus petit)")
    tries = trier_par_total_achat(clients)
    for client in tries:
        total = total_depense_client(client)
        print(f"   - {client['nom']}: {total} FCFA")
    
    # CONCEPT : CRUD - Update (modification d'un client)
    print("\n7. Modification d'un client (changement de ville)")
    if clients:
        client_id = clients[0]['id']
        ancienne_ville = clients[0]['ville']
        modifier_client(clients, client_id, ville="Garoua")
        print(f"   Client {clients[0]['nom']}: {ancienne_ville} -> Garoua")
    
    # CONCEPT : Gestion des erreurs avec try/except
    print("\n8. Test de gestion d'erreur (suppression ID inexistant)")
    try:
        supprimer_client(clients, 9999)
        print("   ERREUR: devrait échouer!")
    except KeyError as e:
        print(f"   OK: Erreur attrapée - {e}")
    
    # CONCEPT : CRUD - Delete (suppression d'un client existant)
    print("\n9. Suppression d'un client existant (ID: 2)")
    try:
        supprimer_client(clients, 2)
        print("   Client ID:2 supprimé avec succès")
    except KeyError as e:
        print(f"   Erreur: {e}")
    
    # CONCEPT : CRUD - Create (ajout d'un nouveau client après suppression)
    print("\n10. Ajout d'un nouveau client")
    c4 = ajouter_client(
        clients,
        "Amina Diallo",
        "Maroua",
        "655432109",
        ["nouveau", "recommande"]
    )
    c4["historique_achats"] = [("2026-02-05", 60000)]
    print(f"   Nouveau client ajouté: {c4['nom']} (ID: {c4['id']})")
    
    # Affichage final après toutes les opérations CRUD
    print("\n11. Affichage final après opérations CRUD")
    afficher_tous(clients)
    
    # CONCEPT : Persistance - sauvegarde des modifications
    print("\n12. Sauvegarde des données...")
    sauvegarder_clients(clients, DATA_FILE)
    print(f"   Données sauvegardées dans: {DATA_FILE}")
    
    print("\n" + "*"*60)
    print("RÉCAPITULATIF DES OPÉRATIONS CRUD DÉMONTRÉES")
    print("*"*60)
    print("✓ CREATE: Ajout de 3 clients initiaux + 1 nouveau client")
    print("✓ READ: Recherche par nom et par ville")
    print("✓ UPDATE: Modification de la ville d'un client")
    print("✓ DELETE: Suppression d'un client existant")
    print("*"*60)


def menu_interactif():
    """Un petit menu interactif pour tester manuellement"""
    # CONCEPT : Chargement initial des données
    clients = charger_clients(DATA_FILE)
    
    # CONCEPT : Boucle infinie pour un menu interactif
    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL")
        print("="*40)
        print("1. Voir tous les clients")
        print("2. Ajouter un client")
        print("3. Chercher un client")
        print("4. Trier les clients")
        print("5. Modifier un client")
        print("6. Supprimer un client")
        print("7. Ajouter un achat à un client")
        print("8. Lancer la démo automatique")
        print("9. Sauvegarder et quitter")
        print("-"*40)
        
        choix = input("Votre choix (1-9): ").strip()
        
        if choix == "1":
            afficher_tous(clients)
            
        elif choix == "2":
            print("\n--- AJOUT D'UN CLIENT ---")
            # CONCEPT : Saisie utilisateur avec validation
            nom = input("Nom: ").strip()
            ville = input("Ville: ").strip()
            tel = input("Téléphone (9 chiffres): ").strip()
            tags = input("Tags (séparés par des virgules): ").strip()
            
            # CONCEPT : Validation des entrées obligatoires
            if not nom or not ville or not tel:
                print("Erreur: Nom, ville et téléphone sont obligatoires!")
                continue
            
            # Validation du numéro de téléphone s'il s'agit d'un camerounais
            if not (tel.isdigit() and len(tel) == 9 and tel[0] in "2367"):
                print("Erreur: Numéro de téléphone invalide (doit avoir 9 chiffres et commencer par 2,3,6 ou 7)")
                continue
                
            # CONCEPT : Transformation d'une chaîne en liste
            tags_liste = [t.strip() for t in tags.split(",")] if tags else []
            nouveau = ajouter_client(clients, nom, ville, tel, tags_liste)
            print(f"✅ Client ajouté avec ID: {nouveau['id']}")
            
            # CONCEPT : Ajout conditionnel d'éléments à une liste
            ajouter_achat = input("Ajouter un achat maintenant? (o/n): ").strip().lower()
            if ajouter_achat == 'o':
                montant = input("Montant de l'achat (FCFA): ").strip()
                if montant.isdigit():  # CONCEPT : Validation numérique
                    # CONCEPT : Utilisation du module datetime pour la date actuelle
                    date = datetime.now().strftime("%Y-%m-%d")
                    nouveau['historique_achats'].append((date, int(montant)))
                    print("✅ Achat ajouté!")
            
        elif choix == "3":
            print("\n--- RECHERCHE ---")
            print("1. Par nom")
            print("2. Par ville")
            sous_choix = input("Votre choix: ").strip()
            
            # CONCEPT : Structure conditionnelle pour sous-menu
            if sous_choix == "1":
                nom = input("Nom à rechercher: ").strip()
                resultats = rechercher_par_nom(clients, nom)
            elif sous_choix == "2":
                ville = input("Ville à rechercher: ").strip()
                resultats = rechercher_par_ville(clients, ville)
            else:
                print("❌ Choix invalide")
                continue
                
            # CONCEPT : Affichage conditionnel selon résultats
            if resultats:
                print(f"\n{len(resultats)} client(s) trouvé(s):")
                for client in resultats:
                    afficher_un_client(client, details=True)
            else:
                print("Aucun client trouvé")
                
        elif choix == "4":
            print("\n--- TRI ---")
            print("1. Par nom (A-Z)")
            print("2. Par dépenses totales (du + grand au + petit)")
            sous_choix = input("Votre choix: ").strip()
            
            if sous_choix == "1":
                tries = trier_par_nom(clients)
                titre = "Clients triés par nom"
            elif sous_choix == "2":
                tries = trier_par_total_achat(clients)
                titre = "Clients triés par dépenses"
            else:
                print("❌ Choix invalide")
                continue
                
            print(f"\n{titre}:")
            for client in tries:
                afficher_un_client(client)
                
        elif choix == "5":
            # CONCEPT : CRUD - Update avec interface utilisateur
            afficher_tous(clients)
            try:
                # CONCEPT : Conversion de type avec gestion d'erreur
                id_client = int(input("\nID du client à modifier: ").strip())
            except ValueError:
                print("❌ ID invalide")
                continue
                
            print("Laissez vide pour ne pas modifier")
            nom = input("Nouveau nom: ").strip()
            ville = input("Nouvelle ville: ").strip()
            tel = input("Nouveau téléphone: ").strip()
            tags = input("Nouveaux tags (séparés par virgules): ").strip()
            
            # CONCEPT : Construction dynamique d'un dictionnaire de paramètres
            params = {}
            if nom:
                params['nom'] = nom
            if ville:
                params['ville'] = ville
            if tel:
                params['telephone'] = tel
            if tags:
                params['tags'] = [t.strip() for t in tags.split(",")]
            
            # CONCEPT : Appel de fonction avec déballage de dictionnaire (**kwargs)
            try:
                modifier_client(clients, id_client, **params)
                print("✅ Client modifié avec succès!")
            except KeyError:
                print("❌ Erreur: Client non trouvé")
                
        elif choix == "6":
            # CONCEPT : CRUD - Delete avec confirmation
            afficher_tous(clients)
            try:
                id_client = int(input("\nID du client à supprimer: ").strip())
            except ValueError:
                print("❌ ID invalide")
                continue
                
            confirmer = input(f"Êtes-vous sûr de supprimer le client {id_client}? (o/n): ").strip().lower()
            if confirmer == 'o':
                try:
                    supprimer_client(clients, id_client)
                    print("✅ Client supprimé!")
                except KeyError:
                    print("❌ Erreur: Client non trouvé")
            else:
                print("Suppression annulée")
                
        elif choix == "7":
            print("\n--- AJOUT D'UN ACHAT ---")
            afficher_tous(clients)
            try:
                id_client = int(input("\nID du client: ").strip())
            except ValueError:
                print("❌ ID invalide")
                continue
                
            # Recherche du client
            client_trouve = None
            for c in clients:
                if c["id"] == id_client:
                    client_trouve = c
                    break
                    
            if not client_trouve:
                print("❌ Client non trouvé")
                continue
                
            print(f"Client: {client_trouve['nom']}")
            montant = input("Montant de l'achat (FCFA): ").strip()
            date_achat = input("Date (YYYY-MM-DD, laisser vide pour aujourd'hui): ").strip()
            
            if not montant.isdigit():
                print("❌ Montant invalide")
                continue
                
            if not date_achat:
                date_achat = datetime.now().strftime("%Y-%m-%d")
            else:
                # Validation basique de la date
                try:
                    datetime.strptime(date_achat, "%Y-%m-%d")
                except ValueError:
                    print("❌ Format de date invalide (utilisez YYYY-MM-DD)")
                    continue
            
            # CONCEPT : Ajout d'un tuple à une liste
            client_trouve.setdefault("historique_achats", []).append((date_achat, int(montant)))
            print(f"✅ Achat de {montant} FCFA ajouté le {date_achat}")
            
        elif choix == "8":
            demo_automatique()
            # CONCEPT : Rechargement des données après modifications externes
            clients = charger_clients(DATA_FILE)
            
        elif choix == "9":
            # CONCEPT : Sauvegarde finale avant fermeture
            print("\nSauvegarde avant de quitter...")
            sauvegarder_clients(clients, DATA_FILE)
            print(f"✅ Données sauvegardées dans {DATA_FILE}")
            print("Au revoir!")
            break  # CONCEPT : Sortie de boucle infinie
            
        else:
            print("❌ Choix invalide, veuillez réessayer")
        
        # CONCEPT : Pause pour laisser l'utilisateur lire les résultats
        input("\nAppuyez sur Entrée pour continuer...")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("TP01 - GESTIONNAIRE DE CLIENTS")
    print("="*60)
    print("Réalisé par: Steve et Fayol")
    print("Date: " + datetime.now().strftime("%Y-%m-%d"))
    print("\nCe programme utilise des listes, tuples et dictionnaires Python")
    print("pour gérer une base de données simple de clients.")
    print("="*60)
    
    # CONCEPT : Vérification du chargement initial des données
    clients = charger_clients(DATA_FILE)
    print(f"\n📊 Statut: {len(clients)} clients chargés depuis {DATA_FILE}")
    
    # Menu simple pour choisir le mode d'exécution
    print("\nQue souhaitez-vous faire?")
    print("1. Lancer la démonstration automatique")
    print("2. Utiliser le menu interactif")
    print("3. Quitter")
    
    choix = input("\nVotre choix (1-3): ").strip()
    
    if choix == "1":
        demo_automatique()
        
        # CONCEPT : Option post-exécution pour inspection des données
        print("\nVoulez-vous voir les données sauvegardées?")
        voir = input("Afficher les données finales? (o/n): ").strip().lower()
        if voir == 'o':
            clients = charger_clients(DATA_FILE)
            afficher_tous(clients)
            
    elif choix == "2":
        menu_interactif()
        
    elif choix == "3":
        print("\nAu revoir!")
        sys.exit(0)  # CONCEPT : Sortie propre du programme
        
    else:
        print("❌ Choix invalide, au revoir!")
    
    # Message de fin récapitulatif
    print("\n" + "="*60)
    print("Fin du programme TP01")
    print("Toutes les opérations CRUD ont été testées:")
    print("- Create: ajouter_client")
    print("- Read: rechercher_par_nom, rechercher_par_ville")
    print("- Update: modifier_client") 
    print("- Delete: supprimer_client")
    print("="*60)


# CONCEPT IMPORTANT : Point d'entrée du programme
# Le bloc __name__ == "__main__" permet de définir ce qui s'exécute
# quand le fichier est lancé directement (pas importé comme module)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # CONCEPT : Gestion propre de l'interruption clavier (Ctrl+C)
        print("\n\nProgramme interrompu par l'utilisateur.")
        print("Merci d'avoir utilisé le gestionnaire de clients!")
    except Exception as e:
        # CONCEPT : Capture des exceptions non prévues
        print(f"\n⚠️ Une erreur inattendue s'est produite: {e}")
        print("Veuillez vérifier votre fichier de données ou votre code.")