import xml.etree.ElementTree as ET
import sqlite3

con=sqlite3.connect('tdb.sqlite')
cur=con.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
);

CREATE TABLE Genre(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
);

CREATE TABLE Album(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
artist_id INTEGER,
title TEXT UNIQUE
);

CREATE TABLE Track(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT UNIQUE,
album_id INTEGER,
genre_id INTEGER,
len INTEGER,
rating INTEGER,
count INTEGER
);
''' )

fname=input('Enter file name - ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

det=ET.parse(fname)
req=det.findall('dict/dict/dict')
print('Dict count:', len(req))

for entry in req:
    #if(lookup(entry, 'TRACK ID') is None): continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    genre = lookup(entry, 'Genre')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or genre is None or album is None : continue

    print(name, artist, album, count, rating, length)

    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)',(artist,))
    cur.execute('SELECT id From Artist WHERE name=?',(artist,))
    artist_id=cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)',(genre,))
    cur.execute('select id from Genre where name=?',(genre,))
    genre_id=cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
    VALUES (?, ?)''', (album,artist_id))
    cur.execute('SELECT id FROM Album WHERE title=?',(album,))
    album_id=cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id,
    len, rating , count) VALUES (?, ?, ?, ?, ?, ?)''',(name, album_id, genre_id,
    length, rating, count))

    con.commit()
