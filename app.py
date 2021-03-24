from flask import Flask, render_template, request
from databaseinter import getall, tgetall, twin, tloss, game, add
from threading import Thread
import os
import sqlite3
from waitress import serve
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def index():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYERS ORDER BY wins DESC, losses ASC")
    data1 = cursor.fetchmany(1)
    cursor.execute("SELECT * FROM TEAMS ORDER BY wins DESC, losses ASC")
    data2 = cursor.fetchmany(1)
    cursor.execute("SELECT * FROM GAMES ORDER BY rowid DESC")
    data3 = cursor.fetchmany(1)
    cursor.execute("SELECT COALESCE(MAX(rowid), 0) FROM GAMES")
    data4 = cursor.fetchmany(1)
    for row in data4:
        data4 = row[0]
    conn.close()
    return render_template('index.html',
                           data1=data1,
                           data2=data2,
                           data3=data3,
                           data4=data4)


@app.route("/matchup", methods=['GET', 'POST'])
def matchup():
    if request.method == 'POST':
        t1p1 = request.form['t1p1']
        t1p2 = request.form['t1p2']
        t2p1 = request.form['t2p1']
        t2p2 = request.form['t2p2']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM TEAMS WHERE (name1 = ? AND name2 = ?) OR (name2 = ? AND name1 = ?)",
            (
                t1p1,
                t1p2,
                t1p1,
                t1p2,
            ))
        data1 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM TEAMS WHERE (name1 = ? AND name2 = ?) OR (name2 = ? AND name1 = ?)",
            (
                t2p1,
                t2p2,
                t2p1,
                t2p2,
            ))
        data2 = cursor.fetchall()
        # god this lookup makes me want to cry
        # theres gotta be a better way ffs
        cursor.execute(
            "SELECT * FROM GAMES WHERE (((win1 = ? OR win2 = ?) AND (win2 = ? OR win1 = ?)) AND ((loss1 = ? OR loss2 = ?) AND (loss2 = ? OR loss1 = ?))) OR (((win1 = ? OR win2 = ?) AND (win2 = ? OR win1 = ?)) AND ((loss1 = ? OR loss2 = ?) AND (loss2 = ? OR loss1 = ?))) ORDER BY rowid DESC",
            (
                t1p1,
                t1p1,
                t1p2,
                t1p2,
                t2p1,
                t2p1,
                t2p2,
                t2p2,
                t2p1,
                t2p1,
                t2p2,
                t2p2,
                t1p1,
                t1p1,
                t1p2,
                t1p2,
            ))
        data3 = cursor.fetchall()
        t1wins = 0
        t2wins = 0
        for row in data3:
            if (row[0] == t1p1 or row[1] == t1p1) and (row[0] == t1p2
                                                       or row[1] == t1p2):
                t1wins += 1
            elif (row[0] == t2p1 or row[1] == t2p1) and (row[0] == t2p2
                                                         or row[1] == t2p2):
                t2wins += 1
        return render_template('matchup.html',
                               data1=data1,
                               data2=data2,
                               data3=data3,
                               t1wins=t1wins,
                               t2wins=t2wins)
    return render_template('matchup.html')


@app.route("/qr")
def qr():
    return render_template('qr.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        player = request.form['player']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PLAYERS WHERE name = ?", (player, ))
        data1 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM TEAMS WHERE (name1 = ?) OR (name2 = ?) ORDER BY wins DESC, losses ASC",
            (
                player,
                player,
            ))
        data2 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM GAMES WHERE (win1 = ?) OR (win2 = ?) OR (loss1 = ?) OR (loss2 = ?)",
            (
                player,
                player,
                player,
                player,
            ))
        data3 = cursor.fetchall()
        conn.close()
        return render_template('playerdisp.html',
                               name=player,
                               data1=data1,
                               data2=data2,
                               data3=data3)
    else:
        return render_template('search.html')


@app.route("/search/<name>", methods=['GET', 'POST'])
def playerdisp(name=None):
    player = name
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYERS WHERE name = ?", (player, ))
    data1 = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM TEAMS WHERE (name1 = ?) OR (name2 = ?) ORDER BY wins DESC, losses ASC",
        (
            player,
            player,
        ))
    data2 = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM GAMES WHERE (win1 = ?) OR (win2 = ?) OR (loss1 = ?) OR (loss2 = ?)",
        (
            player,
            player,
            player,
            player,
        ))
    data3 = cursor.fetchall()
    conn.close()
    return render_template('playerdisp.html',
                           name=name,
                           data1=data1,
                           data2=data2,
                           data3=data3)


@app.route("/leaderboard")
def leaderboard():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM TEAMS WHERE (wins+losses) >= 1 ORDER BY wins DESC, losses ASC"
    )
    data = cursor.fetchall()
    conn.close()
    return render_template('leaderboard.html', data=data)


@app.route("/teams")
def teams():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TEAMS ORDER BY wins DESC, losses ASC")
    data = cursor.fetchall()
    conn.close()
    return render_template('teams.html', data=data)


@app.route("/players")
def players():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLAYERS ORDER BY wins DESC, losses ASC")
    data = cursor.fetchall()
    conn.close()
    return render_template('players.html', data=data)


@app.route("/games")
def games():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GAMES ORDER BY rowid DESC")
    data = cursor.fetchall()
    cursor.execute("SELECT COALESCE(MAX(rowid), 0) FROM GAMES")
    data1 = cursor.fetchmany(1)
    for row in data1:
        data1 = row[0]
    conn.close()
    return render_template('games.html', data=data, data1=data1)


@app.route("/playerin", methods=['GET', 'POST'])
def playerin():
    if request.method == 'POST':
        if request.form['pass'] != os.getenv('PASS'):
            return render_template('error.html')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT NAME FROM PLAYERS")
        playerss = cursor.fetchall()
        players = []
        for row in playerss:
            players.append(row[0])
        conn.close()
        if request.form['player'] in players or request.form['player'] == '':
            return render_template('error.html')
        else:
            add(request.form['player'])
            return render_template('playerin.html',
                                   data=request.form['player'])
    return render_template('playerin.html')


@app.route("/gamein", methods=['GET', 'POST'])
def gamein():
    if request.method == 'POST':
        if request.form['pass'] != os.getenv('PASS'):
            return render_template('error.html')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT NAME FROM PLAYERS")
        playerss = cursor.fetchall()
        players = []
        conn.close()
        for row in playerss:
            players.append(row[0])
        if request.form['win1'] not in players or request.form[
                'win2'] not in players or request.form[
                    'loss1'] not in players or request.form[
                        'loss2'] not in players:
            return render_template('error.html')
        else:
            game(request.form['win1'], request.form['win2'],
                 request.form['loss1'], request.form['loss2'])
            return render_template('gamein.html', data=True)
    return render_template('gamein.html')


def run():
    serve(app, listen='*:8080')


def keep_alive():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    run()
