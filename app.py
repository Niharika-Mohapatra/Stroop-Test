from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from config import Config
import os
import csv
import pandas as pd

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

@app.route("/generate_dataframe")
def generate_dataframe():
    with app.app_context():
        results = StroopResult.query.all()
        df = pd.DataFrame([
            {
                "word": r.word,
                "color": r.color,
                "response": r.response,
                "reaction_time": r.reaction_time,
                "is_correct": r.is_correct, 
                "time": r.timestamp.strftime('%b %d, %Y %I:%M %p')
            }
            for r in results
        ])
    
    csv_data = df.to_csv(index=True)
    
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=stroop_results.csv"})

@app.route("/clear_db", methods=["GET","POST"])
def clear_db():
    with app.app_context():
        db.session.execute(text("DELETE FROM stroop_result;"))
        db.session.commit()
    return "Database cleared!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  
    app.run(host="0.0.0.0", port=port, debug=True)  




