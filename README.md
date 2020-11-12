# enquete_emploi


## Preparation 

Vertical stack of INDIV18*.csv

* first install [csvkit](https://csvkit.readthedocs.io/)
   >mkdir csvkit
   >pipenv --three
   >pipenv install csvkit
* stack: 
   >pipenv run csvstack ~/local/data/emploi/lil-1350b/Csv/INDIV18* > INDIV18.csv 

* import into sqlite3
   > $ sqlite3 emploi.db
   > sqlite>.separator ;
   > sqlite>.import INDIV18.csv indiv

* TODO:  try [csvsql](https://csvkit.readthedocs.io/en/latest/scripts/csvsql.html)



* ref: https://www.datascienceatthecommandline.com/1e/chapter-5-scrubbing-data.html#
