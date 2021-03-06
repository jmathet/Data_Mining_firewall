# Sommaie documentation projet
1. [Description générale](#description-projet)
2. [Organisation des dossier](#organisation-du-repository)
3. [Prérequis pour installation / utilisation](#prérequis-windows)
4. [Tutoriel](#tuto)

# Description générale
**Projet** : Optimisation algo machine learning / data mining pour configurer automatiquement des pare-feux

Projet en 3 étapes : 
1. *Machine Learning* à partir de logs (journaux d'évènements) de pare-feu afin de déterminer un modèle pour traiter automatiquement de nouveaux flux (prise de décision automatique)
2. *Data Mining* à partir des logs (journaux d'évènements) pour déterminer des règles de pare-feu les plus efficaces possibles. Développements inspirés de la méthode proposée dans l'article [*Analysis of Firewall Policy Rules Using data Mining Techniques*](https://ieeexplore.ieee.org/document/1687561)
3. Envoi des règles à l'API Cisco

## Process Data Mining : 

![alt text](step_by_step.png)

<ins> Etapes clés pour l'algorithme FRG :
1. Génération des clusters 
    - Regroupement @IP SRC qui ont les mêmes @IP DST et PORT
    - Regroupement @IP DST qui ont les mêmes @IP SRC et PORT
    - Regroupement  PORT   qui ont les mêmes @IP SRC et @IP DST
4. Suppresion des redondances
6. Généralisation des clusters

<ins> Pseudo code pour la généralisation des clusters 

(code dans ```filtering_rule_generation.py```)
```
MIN_LENGTH_CLUSTER = 10 # Minimum 10 IP dans un cluster (éviter masque trop précis)
Pour chaque cluster d'IP SRC et d'IP DST:
    Si longeur cluster>MIN_LENGTH_CLUSTER :
        new_cluster_IP = adresse IP sous-réseau à partir du 1er et du dernier élément du cluster
Pour chaque cluster de PORTS DST :
    Si cluster_PORT_dst[0]>1024 et cluster_PORT_dst[last]<=49151 :
        Si cluster_PORT_dst[0] == cluster_PORT_dst[last]:
            new_cluster_PORT = cluster_PORT_dst[0]
        Sinon :
            new_cluster_PORT = cluster_PORT_dst[0] + "-" + cluster_PORT_dst[last]
    Si cluster_PORT_dst[0]>49151 :
        new_cluster_PORT = "49152-65535"
    # Sinon (ports < 1024) : Ne rien faire (pas de cluster car "Well Known Ports")
```

<ins> Etapes pour la génération des clusters par évaluation des distances CAGA

 (code dans ```clustering_algo_gap_analysis.py```)

*Entrée* : Liste d'éléments

*Sortie* : Liste de clusters

1. Trier la liste dans l'ordre croissant
2. Calculer l'écart (distance 2 à 2 par soustraction)
    
   **Seuil** fixé arbitrairement à **128** pour les adresses IP et à **1** pour les ports
3. Création des clusters basés sur l'écart, pour chaque élement e de la liste initiale :
```
Si écart[e] == 0 :
    # Ne rien faire pour éviter les répétitions
Si écart[e] < seuil :
    Ajout de l'élément e dans cluster actuel
Sinon :
    Création d'un nouveau cluster
    Ajout de l'élément dans le nouveau cluster
```

<ins> Ordonnancement des règles

1. Regroupement des règles qui partagent les mêmes IP sources et destination : création de listes de ports (en tenant compte du protocole)
2. Regroupement des listes d'IP (src ou dst) afin d'éviter les répétitions (lorsque le champ port est le même)
3. Ordonnancement basé sur la fréquence d'occurence (COUNT)

## Process envoi API
1. Création d'une *policy* (nom passé en argument)
2. Envoi de toutes les règles (lecture fichier `xlsx` passé en argument)

# Organisation du repository
## Dossier ```machine_learning```
//
## Dossier ```data_mining```
Contient les codes permettant de convertir des logs en règles par le processus présenté plus haut. 
- ```clustering_algo_gap_analysis.py``` : contient l'algorithme de génération des clusters qui est basé sur un seuil et qui sert pour les listes d'@IP et les listes de ports
- ```create_primitive_rule_list.py``` : contient l'algorithme pour détecter les redondances et éviter d'avoir 2 lignes identiques (ne tient pas compte du champ compteur / COUNT)
- ```filtering_rule_generation.py``` : contient toute l'architecture et l'intelligence du bloc FRG
- ```group_list_ip.py``` : contient l'algorithme qui permet de regourper les listes d'IP (src ou dst) lorsque la cluterisation n'a pas été possible afin d'éviter les répétitions 
- ```group_proto_ports.py``` : contient l'algorithme qui permet de regrouper les protocoles / ports dans le même champs et de concaténer tous les logs qui ont les mêmes @IP src et @IP dst
- ```logs_test_simple.csv``` :  exemple de fichier de logs qui doit être donné en entrée au main.py
- ```print.log``` :  log de toutes les actions effectuées par l'algo sauvegarder dans ce fichier (permet de rentrer dans les détails)
- ```main.py``` : point d'entrée de tout l'algorithme de data mining
- ```tools.py``` : diverses fonctions basiques + **variables globales**
- ```prepare_file.py``` : contient l'algo qui permet d'extraire les données brut vers un fichier csv facilement exploitable

## Dossier ```api```
Contient les codes permettant de communiquer avec l'API FirePower de Cisco. 
- ```base_request.json``` : JSON template pour données à envoyer à l'API (ajout d'ACL)
- ```complete_json.py``` : contient la fonction qui permet de transférer les ACL d'un fichier xlsx au format JSON imposé par l'API
- ```fmc_post_policy.py``` : point d'entrée (scirpt) pour poster une nouvelle polocy et des ACL associées

<ins> Utilisation

```python fmc_post_policy.py <rule_file.xlsx> <policy_name> <FMC_USERNAME> <FMC_PASSWORD>```

**/!\ WARNING** : Le nom de la *policy* doit être unique.  Dans script (ligne 50)
Exemple :
```
post_data = {
  "type": "AccessPolicy",
  "name": "TEST", # UNIQUE NAME 
  "defaultAction": {
    "action": "BLOCK"
  }
}
```
**/!\ WARNING** : l'URL de l'API doit être modifée ligne 10 du fichier fmc_post_policy.py

# Prérequis (Windows)
## Généraux
- Python 3 (3.8 utilisé pour les développements)
- Pip

## API interractions
- Requests (used for API requests)
- Xlrd (used for read XLSX files)
- Numpy

## Machine Learning 
- *python-weka-wrapper3 prérequis* (from [here](http://fracpete.github.io/python-weka-wrapper3/install.html)) :
    - Numpy
    - Javabridge
    - Graphviz
    - Matplotlib
    - Microsoft Build Tools 2015 

- python-weka-wrapper3 ([doc](http://fracpete.github.io/python-weka-wrapper3/install.html#windows))

## Data Mining 
- Python 3

# Tuto

1. Préparation des données sources : mise en forme des données pour qu'elles soient compréhensibles par l'algo
    - Extract des données depuis un pare-feu (uniquement des logs où la décision est PERMIT) au format csv. Une première ligne est souvent à supprimer car pas des données bruts. 
    - Utilisation (si nécessaire) de scirpt de préparation des fichiers ```python prepare_file.py <path_file_src> <path_file_dst>```. La modification du script peut être nécessaire pour s'adapter aux données en entrées :
        ```
        # Variables to be defined 
        ip_src_i = 2
        ip_dst_i = 5
        port_dst_i = 6
        proto_i = 7
        ```
    
2. Lancement de l'algo
```python main.py <path_file_src.csv>```

3. Envoi des règles à l''API
```python fmc_post_policy.py <rule_file.xlsx> <policy_name> <FMC_USERNAME> <FMC_PASSWORD>```

**/!\ WARNING** : 
- Utilisation d'un chemain relatif vers le fichier source (structure obligatoire voir logs_test_simple.csv)
- l'URL de l'API doit être modifée ligne 10 du fichier fmc_post_policy.py
