import sqlite3
from databaseinter import *
from app import keep_alive

conn = sqlite3.connect('data.db')
try:
    conn.execute('''CREATE TABLE GAMES
                    (WIN1 STR NOT NULL,
                    WIN2 STR NOT NULL,
                    LOSS1 STR NOT NULL,
                    LOSS2 STR NOT NULL,
                    TIME STR NOT NULL);''')
    conn.commit()
except:
    print('table(s) already made')
try:
    conn.execute('''CREATE TABLE PLAYERS
                    (NAME STR PRIMARY KEY NOT NULL,
                    WINS INT NOT NULL,
                    LOSSES INT NOT NULL,
                    WINPERC FLOAT NOT NULL);''')
    conn.commit()
except:
    print('table(s) already made')
try:
    conn.execute('''CREATE TABLE TEAMS
                (NAME1 STR NOT NULL,
                NAME2 STR NOT NULL,
                WINS INT NOT NULL,
                LOSSES INT NOT NULL,
                WINPERC FLOAT NOT NULL);''')
    conn.commit()
except:
    print('table(s) already made')
    
conn.close()


def menu():
    while(True):
        print('\nap: add player\ngp: get player\nrp  remove player\ncp: clear players\npp: print players\nwp: add win to player\nlp: add loss to player\npt: print teams\nct: clear teams\nwt: win team\nlt: loss team\nq:quit')
        comm = input()
        if comm == 'ap':
            player = input('player name: ')
            add(player)
        elif comm == 'gp':
            player = input('player name: ')
            get(player)
        elif comm == 'rp':
            player = input('player name: ')
            remove(player)
        elif comm == 'cp':
            clear()
        elif comm == 'pp':
            printer()
        elif comm == 'wp':
            player = input('player name: ')
            win(player)
        elif comm == 'lp':
            player = input('player name: ')
            loss(player)
        elif comm == 'pt':
            tprinter()
        elif comm == 'ct':
            tclear()
        elif comm == 'wt':
            player1 = input('player1 name: ')
            player2 = input('player2 name: ')
            twin(player1, player2)
        elif comm == 'lt':
            player1 = input('player1 name: ')
            player2 = input('player2 name: ')
            tloss(player1, player2)
        elif comm == 'cg':
            gameclear()
        elif comm == 'q':
            quit(0)
        else:
            print('invalid command')
        

if __name__ == '__main__':
    keep_alive()
    menu()