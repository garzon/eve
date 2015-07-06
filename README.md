# garzonEve

## Install

```
~$ sudo apt-get install sqlite3
~$ sudo pip install evelink
~$ git clone https://github.com/garzon/eve.git
~$ cd eve
~/eve$ curl http://cdn1.eveonline.com/data/Carnyx_1.0_113321_db.zip -o eve.zip
~/eve$ unzip eve.zip
~/eve$ sqlite3 ./universeDataDx.db

sqlite> ALTER TABLE mapSolarSystems ADD jumpsHist TEXT;
sqlite> update `mapSolarSystems` set jumpsHist='0,0,0,0,0';
sqlite> .quit
```

When at 9:51~9:58, add cronjob:
```
~$ crontab -e
0,10,20,30,40,50 * * * * /usr/bin/python ~/eve/jumpsCron.py
```