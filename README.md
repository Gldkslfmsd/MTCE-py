# MTCE-py

This is a reimplementation of [MT-ComparEval](https://github.com/choko/MT-ComparEval), a tool for comparison and evaluation 
of machine translation systems and system outputs. The original was published by
[Ondřej Klejch et al.](http://ufal.mff.cuni.cz/pbml/104/art-klejch-et-al.pdf) in 2015 and consecutivelly used by many MT researchers.
However, nowadays it suffers on some technical issues which make the usage unconvenient or problematic.
Since it was designed before the advent of NMT, it also doesn't reflect the needs 
of todays researchers in NMT perfectly.

We want to make MTCE convenient, reliable and robust. We have reimplemented it in **Django** and **Python3** to make it easy for 
everyone to contribute and for easy linking with the latest MT evaluation scripts and libraries such as `sacrebleu`.
It's also **easy to install**, an easy lightweight `sqlite3` database is used in backend.
We make MTCE **fast** in loading and evaluation new translation tasks. We use 
`numpy` and multiprocessing parallelization. 
MTCE-py will have the same function as the original, plus new features. 
It already supports displaying optional metainformation for every translation sentence.

## Install

- clone this repo, go inside

- `virtualenv -p python3 p3; source p3/bin/activate`

- `pip install -r requirements.txt`

- `python3 manage.py makemigrations`

- `python3 manage.py migrate`

- `python3 manage.py createsuperuser` -- if you want to add or edit the content through web
interface

## Run

- server: `python3 manage.py runserver`

- open `http://localhost:8000/mtce/` in your browser

- background importer: `python3 manage.py background_importer [--workers 2]`

## Data import

Background importer assumes your translations data to import are in `files/comparisons` directory, 
located in the same directory as your `manage.py` script.

It contains subdirectories with so called "comparisons", each containing source, reference and 
variable metafiles for source and reference, one or more "MT systems", 
each containing one or more "checkpoints".

```
newstest2018_en-de   ......................... variable name for comparison 
├── reference.txt    ......................... referential translation (name mandatory)
├── reference.meta-ref.txt  .................. optional metafile for reference ("meta-ref" is variable name)
└── source.txt    ............................ source file (name mandatory)
├── source.meta-source.txt  .................. optional source metafile
├── marian  .................................. MT system (name variable)
│   ├── converged ............................ checkpoints's variable name
│   |   └── translation.txt .................. translation file (name mandatory)
│   |   └── translation.bpe.txt .............. optional metafile for translation ("bpe" is variable name)
│   └── epoch-1    ........................... checkpoints's variable name
│       └── translation.txt .................. translation file (name mandatory)
│       └── translation.bpe.txt .............. optional metafile for translation ("bpe" is variable name)
├── RWTH_transformer_ensemble
│   └── checkpoint
│       └── translation.txt
└── RWTH_transformer_single
    └── checkpoint
        └── translation.txt
```

In every comparison, source, reference and translations must have the same number of lines.
If you change any translation or reference file on data storage, the background importer will notice and reimports and reevaluates the 
data immediately.

## Quick local install demo

- Install by instructions above.

- `mkdir -p files/comparisons` 

- Run server and open http://localhost:8000/mtce/ . You should see a main page with no comparisons to browse.

- Download and unpack [http://ufallab.ms.mff.cuni.cz/~machacek/demo-data.zip](http://ufallab.ms.mff.cuni.cz/~machacek/demo-data.zip). Move the files from 
package's `files/comparisons/` 
to your `files/comparisons`, if necessary.

- Run `python3 manage.py background_importer`. The data should be evaluating and loading.

- You can repeat importing with `cp empty-db.sqlite3 db.sqlite3`. 

- You can skip the background importer with `cp demo-db.sqlite3 db.sqlite3`. You should see several 
comparisons. 

## Tests 

- `python3 manage.py test`


## Acknowledgements

This work was supported by Student Faculty Grant by Charles University, Faculty of Mathematics and Physics, 
in winter semester 2018/2019.

