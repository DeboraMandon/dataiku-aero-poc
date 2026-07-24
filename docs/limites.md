# Limites connues

À lire avant de commencer, pour ne pas être surpris.

- **Durée du trial** : le free trial Dataiku Cloud dure 14 jours (extension
  possible sur demande au support, non garantie automatiquement). Le scope de ce
  POC est pensé pour tenir dans ce délai.
- **OpenSky, usage non-commercial** : les données sont fournies pour un usage
  recherche/personnel, pas commercial. Pas un problème pour ce POC, mais à
  mentionner si le repo devient public.
- **OpenSky, pas de données commerciales** : pas d'horaires, de retards, de
  numéros de vol garantis — uniquement ce qui est dérivable de l'ADS-B (position,
  altitude, vitesse, indicatif). Si un axe "retards/performance" devient
  nécessaire plus tard, il faudra une source supplémentaire (ex. données DOT
  US, Eurocontrol), hors scope ici.
- **Token OpenSky expirant** : ~30 minutes. Le recipe Python doit rafraîchir le
  token avant chaque appel si le scenario tourne sur une fenêtre plus longue.
- **Rate limit OpenSky en accès authentifié** : pas de chiffre officiel vérifié
  au moment de la rédaction — à observer via le header `X-Rate-Limit-Remaining`
  renvoyé par l'API, plutôt que de se fier à un chiffre trouvé ailleurs.
- **Neon, auto-suspend** : le compute Neon se met en veille après inactivité,
  avec un léger délai de réveil (de l'ordre de quelques centaines de ms) sur la
  première requête après une pause. Sans impact réel sur un scenario planifié
  toutes les 15 minutes, mais à savoir en cas de latence inattendue.
- **Git natif Dataiku → GitHub** : le push ne contient que les métadonnées du
  projet (structure du flow, recipes, réglages), pas les données physiques. Le
  repo GitHub ne remplace donc pas une sauvegarde des données elles-mêmes.
- **OpenSky abandonné** : OpenSky bloque explicitement le trafic AWS et les
  autres hyperscalers dans sa politique anti-abus officielle. Dataiku Cloud
  tournant sur AWS, tous les appels timeout depuis les pods d'exécution.
  Remplacé par Aviationstack (statuts de vol par aéroport suivi, plutôt que
  positions ADS-B en direct).
- **Quota Aviationstack, plan gratuit** : entre 100 et 500 requêtes/mois selon
  la source consultée — vérifier le chiffre exact sur le dashboard du compte.
  4 aéroports suivis = 4 requêtes par run, donc pas de scenario automatique
  fréquent possible sans dépasser le quota rapidement.