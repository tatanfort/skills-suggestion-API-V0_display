


import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import request



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

    df = top_skills_grouped.get_group(job_title).reset_index(drop = True) 
    rank_weight = np.array([5*(29-r)/29 for r in range(30)]) #from 1 to 5 based on the rank
    selection_weight = np.array([5*selection/100 for selection in df["selection_score"]]) #from 0 to 5 based on the selection score
    exploitation_percentage = np.array([percentage_exploitation*(1- np.exp(-0.1*x)) for x in df.num_appear]) #for 0 to 0.7 
    #a maximum of 70% of weight will be based on the selection score and a minimum of 0% depending on the number of appearance
    df["weight_sample"] = (np.array([1 for i in range(30)]) - exploitation_percentage) * rank_weight  +  exploitation_percentage * selection_weight
    skills = df.sample(n = 10, weights= "weight_sample").top_skills
    return skills.to_json()


if __name__ == '__main__':
    app.run(debug=False, port=5005)


    
"""  
df = pd.read_pickle("robotics_test.pkl")
  
@app.route("/")
def selected_skills_test():
    #df = top_skills_grouped.get_group(job_title).reset_index(drop = True) 
    job_title = request.args.get('job_title')
    rank_weight = np.array([5*(29-r)/29 for r in range(30)]) #from 1 to 5 based on the rank
    selection_weight = np.array([5*selection/100 for selection in df["selection_score"]]) #from 0 to 5 based on the selection score
    exploitation_percentage = np.array([percentage_exploitation*(1- np.exp(-0.1*x)) for x in df.num_appear]) #for 0 to 0.7 
    #a maximum of 70% of weight will be based on the selection score and a minimum of 0% depending on the number of appearance
    df["weight_sample"] = (np.array([1 for i in range(30)]) - exploitation_percentage) * rank_weight  +  exploitation_percentage * selection_weight
    skills = df.sample(n = 10, weights= "weight_sample").top_skills
    return skills.to_json()


if __name__ == '__main__':
    app.run(debug=False, port=5005)
    
"""

