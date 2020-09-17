

import pandas as pd
import numpy as np
from flask import Flask, render_template
from flask import request
import operator
from fuzzywuzzy import fuzz

app = Flask(__name__)

#Job matching
job_titles_esco = pd.read_pickle("job_titles_esco.pkl")
 

def get_top_similarities_fuzz( word, word_list, n):
    
    similarities = {}
    for i in range(len(word_list)):
        similarities[word_list[i]] = fuzz.token_set_ratio(str(word),word_list[i])
    sorted_similarity = sorted(similarities.items(),key=operator.itemgetter(1),reverse=True)
    return sorted_similarity[:n]

def job_title_match_fuzzy(job_searched, threshold = 90):
    scores = []
    for job_titles in job_titles_esco.preferredLabel:
        scores.append(get_top_similarities_fuzz(job_searched,[job_titles],1)[0][1])
    position_job_title_highest_score = np.argmax(scores)
    highest_score = np.max(scores)
    
    
    if highest_score > threshold:
        return job_titles_esco.iloc[position_job_title_highest_score,0], highest_score
    else :
        scores = []
        for job_titles in job_titles_esco.altLabels:
            scores.append(get_top_similarities_fuzz(job_searched,job_titles,1)[0][1])
        position_job_title_highest_score = np.argmax(scores)
        highest_score = np.max(scores)
    
    
        if highest_score > threshold:
            return job_titles_esco.iloc[position_job_title_highest_score,0], highest_score
        else :
            return None
        

        
        

top_skills_fr = pd.read_pickle("top_skills.pkl")
top_skills_grouped_fr = top_skills_fr.groupby(by="job_title")

top_skills_en = pd.read_pickle("English_Job_Titles_Skills.pkl")
top_skills_grouped_en = top_skills_en.groupby(by="job_title")



@app.route("/")    
def selected_skills_test2():
    job_title = request.args.get('job_title')
    nb_skills_selected = request.args.get('nb_skills_selected', default = 10, type = int)
    language = request.args.get('language', default = "fr", type = str)
    
    if language == "fr":
        df = top_skills_grouped_fr.get_group(job_title).reset_index(drop = True)
    if language == "en":
        job_title = job_title_match_fuzzy(job_title)[0]
        if job_title != None :
            df = top_skills_grouped_en.get_group(job_title).reset_index(drop = True)
       
    if job_title == None:
        return pd.DataFrame({"wrong input":[]}).to_json()
    else:
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
