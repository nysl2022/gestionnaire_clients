#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 12:46:26 2026

@author: the-nysl
"""

import os #Ce module permet d'interagir avec le systeme
import json

#Importer les donnees en JSON 
#Cette fonction permet de recuperer les donnees clients depuis le fichier json pour vers python au demarrage du programme ceci permet aussi de retrouver les clients ajouter apres avoir fermer le programme
def charger_clients(path):
    #On verifie si le chemin n'existe pas si c'est le cas on renvoie une liste vide
    if not os.path.exists(path):
        return []
    try:
        with open(path,"r", encoding="utf-8") as f:
            data = json.load(f)#On lit data/clients.json, data ici est la liste de clients
            
            #Or avec json on ne peut avoir que des listes et non des tuples, il convient de transforme cela
            #pour avoir [date, montant] => (date, montant)
            for c in data:
                hist = c.get("historique_achats", []) #[] permet de recuperer un historique vide ceci permet de ne pas casser la conversion avec le  None
                c["historique_achats"] = [ tuple(item) for item in hist ] 
            return data
    #Si le fichier client.json est vide ou malforme , le programme consider qu'il est vide
    except json.JSONDecodeError:
            return []
 
        
#Exporter les donnees
#Cette fonction permet d'ecrire ce qu'on a modifie en memoire dans le fichier JSON c'est a dire de client(en memoire) => JSON(sur disque)
def sauvegarder_clients(clients, path):
    #On cree le dossier client s'il n'existe pas
    dossier = os.path.dirname(path)
    #On evite les potentiels conflits si le dossiers existe deja
    if dossier:
        os.makedirs(dossier, exist_ok=True)
        
    #Etand donnee que json ne lit pas les tuples , il faut qu'on cree une version compatible pour pouvoir sauvergarder
    serializable = []
    for c in clients:
        hist = c.get("historique_achats", [])
        #On convertir les tuples en liste pour les rendre compatibles avec JSON
        hist_json = [list(item) for item in hist]
        serializable.append({
            "id" : c["id"],
            "nom" : c["nom"],
            "ville" : c["ville"],
            "telephone" : c["telephone"],
            "tags" : c.get("tags", []),
            "historique_achats" : hist_json
            })
    #On ecris dans le fichier en format lisible
    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
        

def total_depense_client(client) : 
        total = 0
        for date, montant in client.get("historique_achats", []): #client.get(["historique_achats"], []) recupere la valeur associe a la cle historique_achats si la cle n'existe pas renvoie une liste vide
            total += montant
        return total
    
    
def ajouter_client(clients, nom, ville, telephone, tags):
    #On calcule le nouvel id
    if len(clients) == 0:
        new_id = 1
    else:
        new_id = max(c["id"] for c in clients) + 1
    #On cree le dictionnaire client
    client = {
        "id" : new_id,
        "nom" : nom.strip(),
        "ville" : ville.strip(),
        "telephone" : telephone.strip(),
        "tags" : [t.strip() for t in tags],
        "historique_achats" : []
        }
    #On ajoute le client a la liste et on retourne le client cree
    clients.append(client)
    return client


def rechercher_par_nom(clients, nomRechercher):
    clients_trouves = []
    for c in clients:
        if nomRechercher.strip().lower() in c["nom"].lower():
            clients_trouves.append(c)
    return clients_trouves


def rechercher_par_ville(clients, villeRechercher ):
    clients_trouves = []
    for c in clients:
        if villeRechercher.strip().lower() in c["ville"].lower():
            clients_trouves.append(c)
    return clients_trouves
            

def trier_par_nom(clients):
    #On cree ue fonction qui renvoie une nouvelle liste trie par ordre alphabetique
    return sorted(clients, key=lambda c: c["nom"].lower() )#lambda est une fonction anonyme et rapide pour trier par nom en ignorant la casse et key attend une fonction qui a partir d'un element renvoie une valeur comparable


def trier_par_total_achat(clients):
    return sorted(clients, key=lambda c: total_depense_client(c), reverse=True )


def supprimer_client(clients, client_id):
    for index, c in enumerate(clients):
        if c["id"] == client_id:
            del clients[index] #del et remove sont deux methodes pour supprimer un element d'une liste en python, del utilise l'index de l'element a supprimer tandis que remove utilise la valeur de l'element a supprimer.

            return
    raise KeyError("Client introuvable") #On affiche ce message si l'id du client n'existe pas 


def modifier_client(clients, client_id, nom=None, ville=None, telephone=None, tags=None):
    for c in clients:
        if c["id"] == client_id:
            if nom is not None:#Ceci se fais si l'utilisateur a fourni une nouvelle valeur pour le nom, sinon on laisse le nom actuel
                c["nom"] = nom.strip()
            if ville is not None:
                c["ville"] = ville.strip()
            if telephone is not None:
                c["telephone"] = telephone.strip()
            if tags is not None:
                c["tags"] = [t.strip() for t in tags]
            return c
    raise KeyError("Client introuvable")


