# Observatoire du trafic aérien — POC Dataiku Cloud

POC personnel réalisé sur le free trial de Dataiku Cloud. Suivi des statuts de
vol pour une liste d'aéroports suivis, enrichis par un référentiel
aéroportuaire stocké en base cloud et une liste de priorités maintenue à la
main dans Google Sheets.

## Architecture en un coup d'œil

Aviationstack API ──┐
(statuts de vol par │
aéroport suivi) │
├──► Flow Dataiku Cloud ──► Dashboard
Neon Postgres │ (jointure ICAO/IATA, (vols par aéroport,
(référentiel aéroports, │ appels API, écriture) répartition statuts)
statique) │
│
Google Sheets │
(aéroports suivis, ─┘
saisie manuelle)

Détail complet : [`docs/architecture.md`](docs/architecture.md)

## Contenu du repo

- `docs/architecture.md` — schéma détaillé, choix techniques et pourquoi
- `docs/setup.md` — étapes de mise en place, dans l'ordre
- `docs/limites.md` — limites connues du POC, y compris le pivot OpenSky → Aviationstack
- `docs/google_sheet_template.md` — structure de la feuille de suivi
- `sql/schema.sql` — DDL de la table `aeroports` sur Neon
- `scripts/load_ourairports.py` — charge le référentiel OurAirports dans Neon
- `scripts/fetch_aviationstack.py` — récupère les statuts de vol par aéroport suivi

## Statut

POC fonctionnel : pipeline Neon + Google Sheets + Aviationstack opérationnel,
dashboard avec 2 graphiques (vols par aéroport suivi, répartition par statut
de vol), scenario planifié quotidien.

## Sources de données

- [Aviationstack](https://aviationstack.com/) — statuts de vol, plan gratuit limité en requêtes/mois
- [OurAirports](https://ourairports.com/data/) — référentiel aéroportuaire, domaine public
- Google Sheets — saisie manuelle

## Note sur OpenSky

Le projet utilisait initialement OpenSky Network (positions ADS-B en direct).
OpenSky bloque explicitement le trafic AWS dans sa politique anti-abus — or
Dataiku Cloud tourne sur AWS, rendant l'API injoignable depuis les pods
d'exécution. Voir [`docs/limites.md`](docs/limites.md) pour le détail du
diagnostic et du pivot vers Aviationstack.