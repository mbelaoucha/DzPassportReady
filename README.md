# Quoi?

Ce script est un simple hack permettant de scanner la disponibilité de votre passeport auprès de votre consulat algérien en France. Cette version est configurée pour interroger le site de Nanterre, mais peut facilement être reconfiguré pour interroger un autre site voire tous les sites consulaires en France.

 # Comment l’Utiliser?
Pour connaitre la disponibilité de votre passeport:
```shell
      python3 passport.py -id <numéro de demande>
```
Pour connaitre la disponibilité de tous les passeports dont le dossier est compris entre `X` et `Y`:
```shell
    python3 passport.py -s X,Y -sc
```
Vous pouvez aussi l’utiliser comme module 


```python
from passport import CheckPassportReady
...
if CheckPassportReady(1234):
	SendNotifications()

```
# Evolution?

J'ai eu la furtive idée de l'utiliser comme base d'applications web: 1) informer des inscrits de la disponibilité de leurs passeports, et 2) évaluer la performance des sites consulaires.
Mais je manque de temps pour le faire. Je peux néanmoins aider les bonnes volontés :)

# Je demande un passeport:

Je  prépare actuellement un retour d’expérience de ma récente demande de passeport avec leçons apprises et astuces. Il sera publié dans les meilleurs délais.
