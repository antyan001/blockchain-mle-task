from flask import Flask

from blockchain_task.reporting.endpoint import reporting_bp

app = Flask(__name__)
app.register_blueprint(reporting_bp)
app.run(host="0.0.0.0", port=2899, debug=True)
