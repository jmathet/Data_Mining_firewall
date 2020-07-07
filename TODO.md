# TODO

- [x] Créer fonction (tools) pour lire logs (important data) dans fichiers csv
- [x] Choisir structure de données adaptées aux logs / règles de FW
- [x] Ecrire algo génération "premitive rules" --> rèles identiques
- [x] Ecrire Clustering Algo bu Gap Analaysis (CAGA)
- [x] Ecrire algo "main" FRG
    - [x] STEP 1: Regroupement @IP SRC qui ont même @IP DST et PORT
	- [x] STEP 2: Regroupement @IP DST qui ont même @IP SRC et PORT
	- [x] STEP 3: Regroupement  PORT   qui ont même @IP SRC et @IP DST
    - [x] STEP 4: Suppresion des redondances (adapter algo génération "premitive rules")
    - [x] STEP 5: Cluster généralisation
- [x] Créer fonction écrriture dans fichier .xlxs
- [x] Ecrire algo d'ordonnancement des règles (basé sur le nombre count)
- [x] Lire CSV file en argument du main.py
- [x] Prendre en compte protocole dans concaténation des ports
- [x] Amélioration précision généralisation IP pour coller à la réalité (Max /24 et Min /27)
- [x] Amélioration concaténation des ports : pouvoir mettre un range et un port unique pour une règle

Bonus :
- [ ] Ecrire script installation prérequis auto
- [ ] Créer fichier avec les variables