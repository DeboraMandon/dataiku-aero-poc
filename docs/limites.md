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