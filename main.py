

import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import request

app = Flask(__name__)


top_skills = pd.read_pickle("top_skills.pkl")
top_skills_grouped = top_skills.groupby(by="job_title")


@app.route("/")    
def selected_skills_test2():
    job_title = request.args.get('job_title')
    nb_skills_selected = request.args.get('nb_skills_selected', default = 10, type = int)
    
    df = top_skills_grouped.get_group(job_title).reset_index(drop = True)
    
    if nb_skills_selected > len(df):
        skills = df.top_skills
    
    else:
        nb_exploration = round(0.3*nb_skills_selected)
        nb_exploitation = nb_skills_selected - nb_exploration
        
        #exploration
        exploration_skills = df.sample(n=nb_exploration).skill
        #exploitation
        selection_weight = np.array([1.00001- np.exp(-0.2*x) for x in df.num_appear])*df.selection_score
        df["weight_sample"] = selection_weight
        
        exploitation_skills = df.sample(n = nb_exploitation, weights= "weight_sample").skill
        
        skills = exploitation_skills.append(exploration_skills)
    return skills.reset_index(drop = True).to_json()
if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8080, debug=True)
