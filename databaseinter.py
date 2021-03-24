import sqlite3
from datetime import datetime
from pytz import timezone

#players
def add(player: str):
    conn = sqlite3.connect('data.db')
    conn.execute('INSERT INTO PLAYERS (NAME,WINS,LOSSES,WINPERC) \
        VALUES (?,?,?,?)',(player,0,0,0.0))
    conn.commit()
    conn.close()
    gen(player)

def get(player: str):
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT name,wins,losses from PLAYERS where name = ?', (player,))
    print(cursor.fetchone())
    conn.close()

def remove(player: str):
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE from PLAYERS where NAME = ?;',(player,))
    conn.commit()
    tremove(player)
    print(f'deleted {player}')
    conn.close()

def clear():
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM PLAYERS')
    conn.commit()
    conn.close()

def printer():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT * from PLAYERS ORDER BY wins DESC')
    for row in cursor:
        print(row)
    conn.close()

def getall():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT name,wins,losses from PLAYERS ORDER BY wins DESC')
    result = '<p>'
    for row in cursor:
        result += str(row) + '</p><p>'
    conn.close()
    return result

def win(player: str):
    conn = sqlite3.connect('data.db')
    conn.execute('UPDATE PLAYERS set wins = wins + 1 where NAME = ?',(player,))
    conn.commit()
    conn.close()
    winper(player)

def loss(player: str):
    conn = sqlite3.connect('data.db')
    conn.execute('UPDATE PLAYERS set losses = losses + 1 where NAME = ?',(player,))
    conn.commit()
    conn.close()
    winper(player)

def winper(player: str):
    conn = sqlite3.connect('data.db')
    wins = conn.execute('SELECT wins FROM PLAYERS WHERE name = ?', (player,)).fetchone()[0]
    losses = conn.execute('SELECT losses FROM PLAYERS WHERE name = ?', (player,)).fetchone()[0]
    winpercent = 0.0
    if wins+losses != 0:
        winpercent = round((wins/(wins+losses))*100, 2)
    conn.execute('UPDATE PLAYERS SET winperc = ? where NAME = ?',(winpercent,player))
    conn.commit()
    conn.close()

#teams
def gen(player: str):
    conn = sqlite3.connect('data.db')
    players = conn.execute('SELECT name FROM PLAYERS WHERE name != ?',(player,))
    for name in players:
        conn.execute('INSERT INTO TEAMS (NAME1, NAME2, WINS, LOSSES, WINPERC) VALUES (?,?,?,?,?)',(str(name)[2:-3],player,0,0,0.0))
    conn.commit()
    conn.close()

def tgetall():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT name1,name2,wins,losses from TEAMS ORDER BY wins DESC')
    result = ''
    for row in cursor:
        result += str(row) + '\n'
    conn.close()
    return result

def tremove(player:str):
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM TEAMS WHERE name1 = ? OR name2 = ?',(player,player,))
    conn.commit()
    conn.close()

def tclear():
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM TEAMS')
    conn.commit()
    conn.close()

def tprinter():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT * from TEAMS ORDER BY wins DESC')
    for row in cursor:
        print(row)
    conn.close()

def twin(player1: str, player2: str):
    conn = sqlite3.connect('data.db')
    conn.execute('UPDATE TEAMS SET wins = wins + 1 WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)',(player1,player2,player2,player1,))
    conn.commit()
    conn.close()
    twinper(player1, player2)
    win(player1)
    win(player2)

def tloss(player1: str, player2: str):
    conn = sqlite3.connect('data.db')
    conn.execute('UPDATE TEAMS SET losses = losses + 1 WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)',(player1,player2,player2,player1,))
    conn.commit()
    conn.close()
    twinper(player1, player2)
    loss(player1)
    loss(player2)

def twinper(player1: str, player2: str):
    conn = sqlite3.connect('data.db')
    wins = conn.execute('SELECT wins FROM TEAMS WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)', (player1, player2, player2, player1,)).fetchone()[0]
    losses = conn.execute('SELECT losses FROM TEAMS WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)', (player1, player2, player2, player1)).fetchone()[0]
    winpercent = 0.0
    if wins+losses != 0:
        winpercent = round((wins/(wins+losses))*100, 2)
    conn.execute('UPDATE TEAMS SET winperc = ? WHERE (name1 = ? AND name2 = ?) OR (name1 = ? AND name2 = ?)',(winpercent, player1, player2, player2, player1))
    conn.commit()
    conn.close()

def game(win1, win2, loss1, loss2):
    conn = sqlite3.connect('data.db')
    now = datetime.now()
    now = now.replace(tzinfo=timezone('UTC'))
    now = now.astimezone(timezone('US/Pacific'))
    dt = now.strftime('%m/%d/%Y %H:%M:%S')
    conn.execute('INSERT INTO GAMES (WIN1,WIN2,LOSS1,LOSS2,TIME) \
        VALUES (?,?,?,?,?)',(win1,win2,loss1,loss2,dt))
    conn.commit()
    conn.close()
    twin(win1,win2)
    tloss(loss1,loss2)
    
def gameclear():
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM GAMES')
    conn.commit()
    conn.close()