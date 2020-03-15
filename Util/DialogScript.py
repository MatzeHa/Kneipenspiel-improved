
Dialoge = {}
Triloge = {}
guy = 0
guest = 1
guest2 = 2

Dialoge.update({"ST_0": {1: (guy, ('Wie gehts so?', 'Ich würde dich gerne auf ein Getränk einladen!', 'Tschau'),
                             ((110, 120), (210, 220), 0)),
                         110: (guest, 'Lass mich in Ruhe, ich warte auf meine Freunde!', 111),
                         111: (guy, 'OK', 0),
                         120: (guest, 'Gut, setz dich doch.', 121),
                         121: (guy, ('Ja gerne!', 'Nein danke...'), (0, 0)),
                         210: (guest, 'Dann nehm ich einen Gin Tonic. Den teuersten...', (211, 212)),
                         211: (guy, 'Dabei siehst du doch so billig aus!', 0),
                         212: (guy, 'Klaro!', 0),
                         220: (guy, 'mach das du wegkommst', 0)
                         }})

Dialoge.update({"ST_1": {1: (guy, 'Hi!', 2),
                         2: (guy, 'Mein Name ist Guybrush Threepwood und ich will Pirat werden!', 3),
                         3: (guest, 'Du willst also Pirat werden, siehst aber eher wie ein Buchhalter aus.', 4),
                         4: (guy, 'Wad willste, du Deckschrubba?', 5),
                         5: (guest, 'Verzieh dich!', 0)
                         }})


Dialoge.update({"ST_2": {1: (guest, 'Kommt \'n Schornsteinfeger inne Bar. Sagt der Barkeeper:', 2),
                         2: (guest, 'Der geht aufs Haus!', 3),
                         3: (guest, 'Brrrrruuuu-HAA-HAHAHA!', 4),
                         4: (guy, '...', 0)
                         }})

Dialoge.update({"ST_3": {1: (guy, 'Pfui Deibel, ist die hässlich', 0)}})


Triloge.update({"ST_1": {1: (guy, 'Hi!', 3),
                          3: (guest, 'Ich bin Gast 1', 4),
                          4: (guest2, 'Und ich: Numero dos. Ay Ay Ay!!', 5),
                          5: (guest, 'Verzieh dich!', 0)
                          }})





# ich wollte mich finanziell weiterentwickeln
