import threading
import time
from flask import Flask, render_template
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


@app.context_processor
def inject_load():
    with open('/proc/loadavg', 'rt') as f:
        load = f.read().split()[0:3]
    return {'load5': load[0], 'load10': load[1], 'load15':load[2]}


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')