Pour l'utilisation du backend il faut : 
Téléchargé via ce lien https://health.google.com/covid-19/open-data/raw-data
- Epidemiologie, Hospitalisation, démographie, index.
- Pour lancer un entrainement en random forest il faut modifié le test pour savoir quel quantité d'arbre est le mieux (100,300,500)

Pour utiliser l'ETL il faut : 
- Créer la base de données grace à la requete SQL présente dans le directory "CSV Clean"
- Modifier dans le WorkFlow chaque chemin qui pointe vers un fichier pour qu'il correspond à votre chemin.
  Une fois configuré il ne reste plus qu'à lancer le workflow et la database sera rempli.


