# TODO

- [x] Documentation
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
- [ ] Lire CSV file en argument du main.py
- [x] Prendre en compte protocole dans concaténation des ports
- [ ] Amélioration précision généralisation IP pour coller à la réalité (Max /24 et Min /27)
- [x] Amélioration concaténation des ports : pouvoir mettre un range et un port unique pour une règle

Bonus :
- [ ] Ecrire script installation prérequis auto
- [ ] Créer fichier avec les variables

# Description projet
**Projet** : Optimisation algo machine learning pour configurer automatiquement des pare-feux

Projet en 2 étapes : 
1. *Machine Learning* à partir de logs de firewalls afin de déterminer un modèle pour traiter automatiquement de nouveaux logs
2. *Data Mining* à partir des logs pour déterminer des règles de firawall les plus efficaces possibles. Développement de la méthode proposée dans l'article [*Analysis of Firewall Policy Rules Using data Mining Techniques*](https://ieeexplore.ieee.org/document/1687561)

Schéma process *Data Mining* : 

![alt text](step_by_steps_2.png)

# Organisation du repository
### Dossier ```machine_learning```
### Dossier ```data_mining```

# Prérequis
(Windows)
### Machine Learning 
- *python-weka-wrapper3 prérequis* (from [here](http://fracpete.github.io/python-weka-wrapper3/install.html)) :
    - Python 3 (3.8 utilisé pour les développements)
    - Pip
    - Numpy
    - Javabridge
    - Graphviz
    - Matplotlib
    - Microsoft Build Tools 2015 

- python-weka-wrapper3 ([doc](http://fracpete.github.io/python-weka-wrapper3/install.html#windows))

### Data Mining 
- Python 3
