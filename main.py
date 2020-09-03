

import pandas as pd
from flask import Flask
from flask import request

import spacy
import warnings
import operator
warnings.filterwarnings("ignore")

class Matcher():
    def __init__(self):
        self.nlp_en = "en_core_web_lg"
        #self.nlp_en = spacy.load("en_core_web_lg")
        #self.nlp_fr = spacy.load("fr_core_news_md")
    def get_top_similarities(self, word, word_list, n, nlp):
        similarities = {}
        doc1 = nlp(str(word))
        for item in word_list:
                doc2 = nlp(item)
                if item != word:
                    similarities[item] = doc1.similarity(doc2)
                else:
                    similarities[item] = 1
        return sorted(similarities.items(),key=operator.itemgetter(1),reverse=True)[:n]
    

    def get_top_similarities_en(self, word, word_list, n):
        return self.get_top_similarities(word, word_list, n, self.nlp_en)
 

matcher = Matcher()




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
