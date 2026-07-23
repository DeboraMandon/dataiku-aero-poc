\# Observatoire du trafic aérien — POC Dataiku Cloud



POC personnel réalisé sur le free trial de Dataiku Cloud. Objectif : suivre en quasi

temps réel les avions au-dessus d'une zone donnée, enrichis par un référentiel

aéroportuaire et une liste de priorités maintenue à la main.



\## Architecture en un coup d'œil

OpenSky Network API ──┐

(positions avions, │

OAuth2, \~temps réel) │

├──► Flow Dataiku Cloud ──► Dashboard

Neon Postgres │ (join, prepare, (carte, KPI par

(référentiel aéroports, │ filtre) aéroport suivi)

statique) │

│

Google Sheets │

(aéroports suivis, ─┘

saisie manuelle)



Détail complet : \[`docs/architecture.md`](docs/architecture.md)



\## Contenu du repo



\- `docs/architecture.md` — schéma détaillé, choix techniques et pourquoi

\- `docs/setup.md` — étapes de mise en place, dans l'ordre

\- `docs/limites.md` — limites connues du POC, à lire avant de commencer

\- `docs/google\_sheet\_template.md` — structure de la feuille de suivi

\- `sql/schema.sql` — DDL de la table `aeroports` sur Neon

\- `scripts/load\_ourairports.py` — charge le référentiel OurAirports dans Neon

\- `scripts/fetch\_opensky.py` — authentification OAuth2 + appel `/states/all`



\## Statut



POC en cours de construction — voir `docs/setup.md` pour l'état d'avancement.



\## Sources de données



\- \[OpenSky Network](https://opensky-network.org/) — ADS-B temps réel, usage recherche/non-commercial

\- \[OurAirports](https://ourairports.com/data/) — référentiel aéroportuaire, domaine public

\- Google Sheets — saisie manuelle

