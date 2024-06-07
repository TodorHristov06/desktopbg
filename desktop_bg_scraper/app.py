from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def query_db(query, args=(), one=False):
    con = sqlite3.connect('desktop_bg/computers.db')
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/computers', methods=['GET'])
def get_computers():
    query_parameters = request.args
    processor = query_parameters.get('processor')
    gpu = query_parameters.get('gpu')
    motherboard = query_parameters.get('motherboard')
    ram = query_parameters.get('ram')

    query = "SELECT * FROM computers WHERE"
    to_filter = []

    if processor:
        query += ' processor=? AND'
        to_filter.append(processor)
    if gpu:
        query += ' gpu=? AND'
        to_filter.append(gpu)
    if motherboard:
        query += ' motherboard=? AND'
        to_filter.append(motherboard)
    if ram:
        query += ' ram=? AND'
        to_filter.append(ram)

    if not (processor or gpu or motherboard or ram):
        return jsonify({'error': 'No filter provided'}), 400

    query = query[:-4] + ';'
    results = query_db(query, to_filter)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)