from app import *

choices = [
    ('1', 'Alternative'),
    ('2', 'Blues'),
    ('3', 'Classical'),
    ('4', 'Country'),
    ('5', 'Electronic'),
    ('6', 'Folk'),
    ('7', 'Funk'),
    ('8', 'Hip-Hop'),
    ('9', 'Heavy Metal'),
    ('10', 'Instrumental'),
    ('11', 'Jazz'),
    ('12', 'Musical Theatre'),
    ('13', 'Pop'),
    ('14', 'Punk'),
    ('15', 'R&B'),
    ('16', 'Reggae'),
    ('17', 'Rock n Roll'),
    ('18', 'Soul'),
    ('19', 'Other'),
]

for ch in choices:
    gen = genre(name=ch[1]);
    db.session.add(gen);
    db.session.commit();
    db.session.close();

