# 8INF803 Bases de données réparties  Automne 2020
## Devoir 1 - 30% de la note finale.
Professeur: Edmond La Chance
Date de remise : Lundi 19 Octobre 2020

* Lien Skydrive, Lien Google Drive
* Remise :
    * Document en PDF ou HTML (Pas de DOCX)
    * Screenshots de l’exécution + fichiers de code source.
    
(Les pièces jointes sont souvent détruites par gmail….). Gmail est devenu très stricte sur le contenu permis. Il est conseillé de me donner un lien vers un cloud (Google Drive, SkyDrive etc). 
* Équipes : 1 à 4 personnes

## Résumé et mise à jour du devoir
Vous devez aller chercher les données sur les sorts (spells) en programmant un crawler dans le langage de votre choix.
Votre crawler doit ensuite envoyer les données dans une BD répartie. Vous pouvez utiliser MongoDB. MongoDB fonctionne avec des collections d’objets JSON. Donc, votre crawler peut par exemple produire un fichier JSON. Ce dernier est ensuite chargé dans une collection mongodb avec l’outil mongoimport ou alors vous pouvez le faire complètement côté code.

Vous pouvez également choisir d’envoyer les données dans un RDD de Apache Spark. Un RDD sur un cluster Apache Spark est une base de données répartie. Apache  Spark est programmé dans le langage Scala mais les langages Python et Java sont également supportés. 
Une fois les données chargées dans Apache Spark ou MongoDB, vous devez exécuter une petite requête en MapReduce (ou même un RDD.filter en Spark) pour trouver les sorts (niveau maximum 4)  avec composantes verbales seulement qui sont disponibles pour le Wizard. Vous devriez trouver <30 sorts.

Vous devez également charger les mêmes données dans une base de données relationnelle comme SQLite et ensuite faire le même travail, mais cette fois avec le langage de requêtes SQL. J’accepte également la solution DataFrame Spark SQL en utilisant Apache Spark. Voir cette page.
Vous devez ensuite faire l’exercice 2 et programmer un algorithme de PageRank. Si vous utilisez l’engin MapReduce de MongoDB, allez à la section sur l’exercice 2 et suivez les instructions. Si vous décidez d’utiliser Apache Spark, vous devez encodez le graphe dans un RDD et ensuite appliquer l’algorithme pagerank.

Votre graphe peut être encodé avec un RDD de sommets. Voici une manière possible d’implémenter le sommet (Scala, Spark).

case class sommet(pagerank : Double, adjlist : Array[Int])

## Exercice 1 : Le sort du dernier recours
### Mise en situation
 Vous êtes un cuisinier appelé Pito, ex-magicien, sorcier, et propriétaire de votre propre restaurant appelé “Les pain pitas garnis de Pito”. Votre restaurant est situé sur le chemin de la forêt DragonWood,  une forêt peuplée par des elfes sylvains et également domicile à un puissant dragon vert.
Vous avez choisi un endroit magnifique pour y établir votre restaurant. Par contre, il y a peu de passage et les elfes ne sont pas trop fan de la cuisine.

Faire de l’argent avec un commerce n’était peut-être pas la meilleure idée. J’aurais peut-être dû rester aventurier...
Un beau jour, pendant la préparation d’une nouvelle recette de pain pita, Pito se fait attaquer par une troupe de Halflings Chaotic Neutral (CN). Ces halflings étaient là pour les richesses du Dragon Vert, mais finalement n’étant pas de taille, ils s’en prennent plutôt à un restaurateur honnête!! Ne soupçonnant pas du tout les halflings, Pito est pris par surprise et capturé. Il a maintenant les deux mains liées et il est attaché à une poutre. Il doit s’échapper!

Les halflings quittent l’auberge. Ils mettent le feu. Pito est encore attaché. Normalement, quand Pito lance un sort, la plupart du temps, il doit agiter ses mains afin de satisfaire certaines composantes somatiques. Il peut également avoir besoin de certains petits-ingrédients qui servent de catalyseur pour lancer le sort.  Cette fois, tout ce que Pito peut faire, c’est parler.
Pito va brûler vivant s’il ne trouve pas une solution.  Il n’a pas la force ou la dextérité pour se défaire de ses liens. Il plonge donc dans sa mémoire pour essayer de trouver un sort qui peut le tirer d’affaire. S’il a déjà vu le sort en action, ou alors vu le sort dans un grimoire ou parchemin, il a confiance qu’il peut le reproduire. 

Votre tâche est de trouver un sort qui peut tirer Pito d’affaire (avec la programmation). Pito est capable de lancer des sorts de maximum niveau 4. Outre trouver un sort, vous devez accomplir les énoncés suivants.

### 1. Crawler
Vous devez utiliser le langage de votre choix (C++, Scala, JS, Java, Python) pour télécharger tous les sorts. Voici quelques sites qui donnent une telle liste (voir plus bas).
Téléchargez tous les sorts, et ensuite faites le tri avec du code MapReduce (ou un filter sur MongoDB ou Spark) pour ne garder que les sorts <=4 de Wizard avec composante verbale seulement.

Vous devez insérer les sorts dans une collection MongoDB ou alors insérer les sorts dans une collection parallèle sur Apache Spark (RDD).

Voici un exemple de JSON inséré. Vous devez utiliser le même schéma au minimum. Pour le niveau du sort, il peut varier. Prenez n’importe lequel. Si c’est un sort du Wizard, prenez le level du sort pour le Wizard.

(Si un sort n’a pas de spell resistance, par exemple celui-ci, mettre la spell resistance à false)

{
  "name": "Acid Arrow",
  "level": “bloodrager 2, magus 2, sorcerer/wizard 2”
  "components" : ["V", "S", "M"],
  "spell_resistance" : false
}

Sites qui contiennent le data (Ils contiennent tous les mêmes sorts)

* Archives of Nethys (Tous les sorts)
* Archives of Nethys
* Pathfinder Main
* DXContent
* Pathfinder #2

Si vous choisissez le site DXContent, c’est peut-être plus facile!
Note sur DXContent :
http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID=1543

SDBID=1 a 1500-1600

Par contre, c’est la liste de tous les spells. Il faut faire 100 % du tri avec le map (ce qui est correct).

Voir aussi ces outils :

* http://www.d20pfsrd.com/magic/tools/advanced-spell-search/ (Un exemple d’application pour chercher dans les spells)
* http://regexr.com/   (Si vous utilisez des regex)
* https://stackoverflow.com/questions/7772605/get-url-contents-in-node-js-with-express (Pour naviguer dans le html sans avoir besoin de regex ou code spécial)
* https://www.npmjs.com/package/jssoup

### 2. Trouver le/un sort qui libère Pito
Il faut que ça soit un sort de Wizard, verbal seulement (V), maximum niveau 4. Exemple de sort verbal seulement : Holy Word (voir plus bas).

Vous devez écrire un code en MapReduce qui génère la liste des sorts valables.

Exemple de code : https://gist.github.com/mitchi/18a9ad3aaf084823a97807f8eeb89a7c

### 3. Vous devez également envoyer les données dans une BD SQlite
Créez un schéma avec une table qui a a peu près la même structure que votre JSON.

{
  "name": "Acid Arrow",
  "level": 2,
  "components" : ["V", "S", "M"],
  "spell_resistance" : false
}

Ensuite, vous devez écrire une requête SQL qui va produire la même liste de spells qu’à l’énoncé 2.

## Exercice 2 : Calculer le pagerank avec plusieurs itérations MapReduce.
Cet exercice est beaucoup plus classique. Vous devez coder l’algorithme du PageRank avec MapReduce (MongoDB) ou en utilisant Apache Spark (Scala, Python ou Java).

Les données des spells du Wizard ne sont pas assez interconnectées pour mériter de faire un PageRank. Nous allons donc prendre un graphe beaucoup plus simple.

Tous les sommets commencent avec un pagerank de 1.

Exemple de code (BFS) :

https://gist.github.com/mitchi/18a9ad3aaf084823a97807f8eeb89a7c

Liens pertinents :
* http://pr.efactory.de/e-pagerank-algorithm.shtml
* https://courses.cs.washington.edu/courses/cse490h/08au/lectures/algorithms.pdf
* http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm
* http://www.sirgroane.net/google-page-rank/
* http://hadooptutorial.info/mapreduce-use-case-to-calculate-pagerank/

Faites attention, il faut qu’il y ait 2 valeurs dans le tableau des valeurs pour que le reducer d’une clé soit appelé.

## Authors
* [maximenrb](https://github.com/maximenrb)
* [adrienls](https://github.com/adrienls)
* [LisaMoulis](https://github.com/LisaMoulis)

## License
This project is licensed under the GNU AGPLv3 License - see the [LICENSE.md](LICENSE) file for details

License chosen thanks to [choosealicense.com](https://choosealicense.com/)