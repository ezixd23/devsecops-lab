from flask import Flask, jsonify
import subprocess
import ipaddress

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/")
def index():
    return jsonify(message="DevSecOps Lab API"), 200

@app.route("/version")
def version():
    return jsonify(version="0.1.0"), 200

@app.route("/ping")
def ping():
    from flask import request
    host = request.args.get("host", "localhost")

    try:
        ipaddress.ip_address(host)
    except ValueError:
        return jsonify(error="invalid host"), 400

    result = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True
    )
    return result.stdout

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # nosemgrep: avoid_app_run_with_bad_host -- intentional: binds inside Docker container, exposure controlled by port mapping
