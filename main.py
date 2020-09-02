

import pandas as pd
from flask import Flask



app = Flask(__name__)

#test
n = 10 
percentage_exploitation = 0.7

top_skills = pd.read_csv("top_skills_recommandation (2).csv", sep = ";")
top_skills.drop("Unnamed: 0", axis=1, inplace = True)

#initialisation of top_skills selection score and num_appears
top_skills["selection_score"] = [100 for i in range(len(top_skills))]
top_skills["num_appear"] = [0 for i in range(len(top_skills))]


top_skills_grouped = top_skills.groupby(by="job_title")

@app.route("/")
def selected_skills_test():
    job_title = request.args.get('job_title')
    skills = top_skills_grouped.get_group(job_title).reset_index(drop = True).iloc[0:10,1]
    return skills.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5005)
