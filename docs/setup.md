# Mise en place — pas à pas

À faire dans cet ordre pour éviter de bloquer sur une dépendance manquante.

## 1. Base Neon

1. Créer un compte sur [neon.tech](https://neon.tech), créer un projet (free tier).
2. Récupérer la chaîne de connexion (`postgresql://...`) depuis le dashboard Neon.
3. Exécuter `sql/schema.sql` sur cette base (via l'éditeur SQL Neon, ou `psql`).
4. Lancer `scripts/load_ourairports.py` en local (voir en-tête du script pour les
   variables d'environnement) pour peupler la table `aeroports`.
5. Vérifier que la base est bien joignable depuis un réseau externe : Neon est
   public par défaut, mais si tu actives une restriction IP côté Neon, il faudra
   y ajouter les IP de sortie de Dataiku Cloud (visibles en bas de la page de
   configuration de connexion, une fois le workspace Dataiku créé).

## 2. Compte OpenSky

1. Créer un compte sur [opensky-network.org](https://opensky-network.org/).
2. Aller dans Account → créer un client API → noter `client_id` et `client_secret`.
3. Tester en local avec `scripts/fetch_opensky.py` avant de le porter dans Dataiku.
4. Vérifier dans la réponse HTTP le header `X-Rate-Limit-Remaining` pour connaître
   ton quota réel — je n'ai pas de chiffre officiel fiable à te donner ici.

## 3. Google Sheets

1. Créer la feuille en suivant `docs/google_sheet_template.md`.
2. Dans Google Cloud Console : activer l'API Google Sheets, créer un compte de
   service, exporter la clé JSON.
3. Partager la feuille avec l'adresse email du compte de service (comme un
   partage classique Google Sheets).

## 4. Dataiku Cloud

1. Dans le workspace, créer les connexions :
   - PostgreSQL → Neon (chaîne de connexion de l'étape 1)
   - Google Sheets (plugin natif) → clé de compte de service de l'étape 3
2. Créer un recipe Python pour `fetch_opensky.py`, en stockant `client_id` /
   `client_secret` dans les credentials du projet (pas en clair dans le code).
3. Construire le flow tel que décrit dans `docs/architecture.md`.
4. Construire le dashboard.
5. Créer un scenario planifié (toutes les 15 min par exemple) et vérifier qu'il
   tient sur la durée du trial (14 jours, extensible sur demande au support).

## 5. Documentation finale

Une fois le flow fonctionnel : captures d'écran du flow et du dashboard dans
`screenshots/`, mise à jour de ce dossier avec les choix réels faits (s'ils ont
divergé de ce qui est décrit ici), puis push sur GitHub.