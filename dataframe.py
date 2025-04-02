import pandas as pd
from app import db, app, StroopResult

with app.app_context():
    results = StroopResult.query.all()
    df = pd.DataFrame([
        {
            "word": r.word,
            "color": r.color,
            "response": r.response,
            "reaction_time": r.reaction_time,
            "is_correct": r.is_correct
        }
        for r in results
    ])

print(df.head())  
df.to_csv("stroop_results.csv", index=False)  

