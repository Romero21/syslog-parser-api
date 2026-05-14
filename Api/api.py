from flask import Flask, jsonify
import json


app = Flask(__name__)
app.json.compact = False
app.json.sort_keys = False

with open('/var/log/remote/Parser/data.json') as f:
    data = json.load(f)


@app.route('/logs')
def logs():
    return jsonify(data), 200


@app.route('/logs/<ip>')
def filter_ip(ip):
    filtered = {}

    for session_id, session in data.items():
        if session["DST IP"] == ip or session["SRC IP"] == ip:
            filtered[session_id] = session

    return jsonify(filtered), 200


@app.route('/stats/top-dst/<n>')
def top_dst(n):
    dst_counter = {}

    try:
        n = int(n)
    except ValueError:
        return jsonify({"error": "Invalid number"}), 400

    for session_id, session in data.items():
        IP = session["DST IP"]
        if session["DST IP"] not in dst_counter:
            dst_counter[IP] = 1
        else:
            dst_counter[IP] += 1

    dst_counter = sorted(dst_counter.items(), key=lambda kv: kv[1], reverse=True)
    return jsonify(dict(dst_counter[:(int(n))])), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
