# Architecture

## Objectif du POC

Tester Dataiku Cloud (free trial) sur un cas représentatif de BI : croiser une source
temps réel (API), un référentiel stocké en base cloud, et une donnée métier saisie
à la main (Sheets), pour produire un dashboard de suivi.

## Les trois sources

### 1. OpenSky Network (API — positions avions)

- Endpoint de données : `GET https://opensky-network.org/api/states/all`
- Paramètres de bounding box pour limiter à une zone (ex. France) :
  `lamin`, `lomin`, `lamax`, `lomax`
- Authentification OAuth2 client credentials (obligatoire depuis mars 2026, l'ancien
  couple identifiant/mot de passe n'est plus accepté) :
  1. Créer un client API dans le compte OpenSky (page Account)
  2. `POST https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token`
     avec `grant_type=client_credentials`, `client_id`, `client_secret`
  3. Utiliser le `access_token` reçu en header `Authorization: Bearer ...`
  4. Le token expire après ~30 min — à rafraîchir avant chaque appel si le scénario
     Dataiku tourne au-delà de cette fenêtre

### 2. Neon Postgres (BDD cloud — référentiel aéroports)

- Base Postgres serverless, gratuite, accessible depuis n'importe quel poste via
  une chaîne de connexion standard — pas d'installation locale.
- Alimentée une seule fois (ou en rafraîchissement occasionnel) à partir du dump
  ouvert OurAirports (`airports.csv`), filtré sur les aéroports français pour rester léger.
- Rôle : associer chaque position avion à l'aéroport suivi le plus proche, et
  enrichir avec le pays, le type d'aéroport, etc.

### 3. Google Sheets (saisie métier — aéroports suivis)

- Une feuille simple, éditée à la main, qui simule un input métier : quels
  aéroports surveiller en priorité cette semaine.
- Connectée via le plugin natif Google Sheets de Dataiku (authentification par
  compte de service ou OAuth2 par utilisateur).
- Rôle : filtrer/prioriser ce qui est montré dans le dashboard sans toucher au flow.

## Flow Dataiku (vue logique)

1. **Recipe Python** `fetch_opensky` → dataset `positions_avions`
   (icao24, callsign, pays_origine, altitude, vitesse, lat, lon, horodatage)
2. **Dataset SQL** `aeroports` (connexion Neon, table déjà peuplée)
3. **Dataset Google Sheets** `aeroports_suivis` (code ICAO, priorité, commentaire)
4. **Recipe de préparation** : calcul de la distance avion ↔ aéroport le plus
   proche (formule haversine), association à l'aéroport
5. **Recipe de filtre/join** : ne garder que les avions proches d'un aéroport
   présent dans `aeroports_suivis`
6. **Dashboard** : carte des positions, nombre d'avions par aéroport suivi,
   altitude moyenne, répartition par pays d'origine
7. **Scenario** planifié (ex. toutes les 15 minutes) pour ré-exécuter l'étape 1
   et rafraîchir le dashboard

## Pourquoi ce choix

Ce n'est pas la seule architecture possible — c'est celle qui permet de tester les
trois modes de connexion demandés (BDD distante, API, Drive/Sheets) dans un seul
scénario cohérent, sans dépendre d'une seule source qui pourrait ne pas être
disponible. Le référentiel aéroportuaire (statique) sépare bien la partie
"données qui bougent" (API) de la partie "données qui ne bougent presque jamais"
(BDD), ce qui est une distinction utile à documenter pour un POC d'architecture BI.