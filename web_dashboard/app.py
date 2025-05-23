from flask import Flask, render_template
from queue_manager import global_queue

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template("dashboard.html", queue_size=global_queue.queue.qsize())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
