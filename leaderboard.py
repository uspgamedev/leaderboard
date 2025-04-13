import json, sys, argparse
from flask import Flask, request, jsonify

from better_profanity import profanity
from profanity_check import predict, predict_prob

from peewee import *
from random import randint


MAX_LENGTH = 255
MAX_ENTRIES = 500

db = SqliteDatabase('db/leaderboard.db')

class Board(Model):
    name: CharField = CharField(MAX_LENGTH)

    class Meta:
        database = db


class Entry(Model):
    name: CharField = CharField(MAX_LENGTH)
    score: IntegerField = IntegerField()
    data: CharField = CharField(MAX_LENGTH)
    #id: IntegerField = IntegerField()


    board = ForeignKeyField(Board, backref='entries')

    class Meta:
        database = db



db.connect()
db.create_tables([Board, Entry])

parser = argparse.ArgumentParser(
                    prog='Leaderboard',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=
"""A simple leaderboard API.

Endpoints:
 - GET /leaderboard/<leaderboard> - Top 10 scores;
 - GET /leaderboard/<leaderboard>/<size> - Top <size> scores;
 - GET /leaderboard/<leaderboard>/rank/<score> - Rank of score <score>;
 - POST /leaderboard/<leaderboard> - Sumbit name and score.""",
                    epilog='')


parser.add_argument('-p', '--port', help='port to listen', type = int, default = 8080)
parser.add_argument('-l', '--leaderboards', action='extend', nargs="+", type=str, help='list of leaderboards to create/use')

args = parser.parse_args()
leaderboards = [] if args.leaderboards == None else args.leaderboards


for board_name in leaderboards:
    board = Board.select().where(Board.name == board_name)
    if len(board) == 0:
        Board(name=board_name).save()

app = Flask(__name__)

@app.route('/leaderboard/<string:board_name>', methods=['GET'])
@app.route('/leaderboard/<string:board_name>/<int:size>', methods=['GET'])
@app.route('/leaderboard/<string:board_name>/rank/<score>', methods=['GET'])
def query_records(board_name, score = None, size = 10):
    name = request.args.get('name')

    board = get_board(board_name)

    if board == None:
        return 'Leaderboard not found!', 404

    if score != None:
        score = int(score)
        rank = Entry.select().where(Entry.board == board).where(Entry.score > score).count()+1

        if rank > MAX_ENTRIES:
            rank = ">" + str(rank)
        else:
            rank = str(rank)

        return rank



    entries = get_top_entries(board, size)

    return jsonify(entries)





@app.route('/leaderboard/<string:board_name>', methods=['POST'])
def update_record(board_name, size = None):
    record = json.loads(request.data)
    record['name'] = record['name'][:MAX_LENGTH] if len(record['name']) > MAX_LENGTH else record['name']


    record['name'] = profanity.censor(record['name'])
    if predict_prob([record['name']]) > 0.4:
        record['name'] = "***"

    board = get_board(board_name)

    if board == None:
        return 'Leaderboard not found!', 404



    if Entry.select().where(Entry.board == board).where(Entry.name == record['name']).where(Entry.score == int(record['score'])).count() == 0:
        entry = Entry(
            name=record['name'],
            score=int(record['score']),
            board = board,
            data = '',
            #id = 0
        )
        entry.save(True)

        if Entry.select().where(Entry.board == board).count() >= MAX_ENTRIES:
            Entry.select().where(Entry.board == board).order_by(Entry.score).first().delete_instance()



    return jsonify(get_top_entries(board))



def get_board(board_name) -> Board:
    return Board.select().where(Board.name == board_name).get()


def get_top_entries(board, quantity: int = 10):
    entries = []
    for entry in Entry.select().where(Entry.board == board).order_by(Entry.score.desc()).limit(quantity):
        entries.append({"name":entry.name, "score":int(entry.score)})
    return entries



profanity.load_censor_words()
app.run(debug=True, port=args.port, host="0.0.0.0")
