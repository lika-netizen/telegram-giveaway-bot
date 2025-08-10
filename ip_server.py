from flask import Flask, request, jsonify

app = Flask(__name__)
ip_counts = {}

MAX_PER_IP = 2

@app.route("/ip_check", methods=["POST"])
def ip_check():
    data = request.get_json()
    ip = data.get("ip")

    if not ip:
        return jsonify({"error": "IP not provided"}), 400

    count = ip_counts.get(ip, 0)
    if count >= MAX_PER_IP:
        return jsonify({"count": count}), 200

    ip_counts[ip] = count + 1
    return jsonify({"count": ip_counts[ip]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
