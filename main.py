

import pandas as pd
from flask import Flask
from flask import request

import spacy
import en_core_web_sm
import operator



app = Flask(__name__)

nlp_en = spacy.load("en_core_web_sm")

def Matcher(word, word_list):
    similarities = {}
    doc1 = nlp_en(str(word))
    for item in word_list:
        doc2 = nlp_en(item)
        if item != word:
            similarities[item] = doc1.similarity(doc2)
        else:
            similarities[item] = 1
    return sorted(similarities.items(),key=operator.itemgetter(1),reverse=True)[0][0]


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
    if job_title not in list(top_skills.job_title.unique()):
        job_title = Matcher(job_title,list(top_skills.job_title.unique()))
        #job_title = "data scientist"
    skills = top_skills_grouped.get_group(job_title).reset_index(drop = True).iloc[0:10,1]
    return skills.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5005)
