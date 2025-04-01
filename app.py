from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import os
import csv

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class StroopResult(db.Model):
    __tablename__ = "stroop_result"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    response = db.Column(db.String(10), nullable=False)
    reaction_time = db.Column(db.Float, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    new_result = StroopResult(
        word=data["word"],
        color=data["color"],
        response=data["response"],
        reaction_time=data["reaction_time"],
        is_correct=data["response"] == data["color"]
    )
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Data saved!"}), 201

@app.route("/data")
def get_data():
    results = StroopResult.query.all()
    return render_template("data.html", results=results)

@app.route("/export_data")
def export_data():
    results = StroopResult.query.all()
    def generate():
        yield "word,color,response,reaction_time,is_correct, timestamp\n"
        for result in results:
            yield f"{result.word},{result.color},{result.response},{result.reaction_time},{result.is_correct}, {result.timestamp}\n"
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=stroop_results.csv"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  
    app.run(host="0.0.0.0", port=port, debug=True)  




