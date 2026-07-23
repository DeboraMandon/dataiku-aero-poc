# Feuille Google Sheets — `aeroports_suivis`

Une seule feuille, une ligne par aéroport suivi. Saisie manuelle, c'est le but :
simuler un input métier maintenu par une personne, pas par un pipeline.

| Colonne | Type | Exemple | Description |
|---|---|---|---|
| `code_icao` | texte | `LFPG` | Code ICAO de l'aéroport (4 lettres) |
| `nom` | texte | `Paris Charles de Gaulle` | Libre, pour lisibilité humaine |
| `priorite` | entier 1-3 | `1` | 1 = priorité haute |
| `commentaire` | texte | `Suivi renforcé cette semaine` | Libre |

Le code ICAO doit correspondre à la colonne `icao_code` (ou `ident`) de la table
`aeroports` sur Neon pour que la jointure fonctionne côté Dataiku.