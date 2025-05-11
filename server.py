from flask import Flask, request, jsonify
import json
from sentence_transformers.cross_encoder import CrossEncoder


app = Flask(__name__)
model = CrossEncoder("cross-encoder/stsb-distilroberta-base")


@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query')
    with open('courses.json', 'r', encoding='utf-8') as f:
        courses = {i["keywords"] + ". " + i["description"]: i for i in json.load(f)}
    corpus = list(courses.keys())

    ranks = model.rank(query, corpus)
    interesting_courses = []
    threshold = 0.4
    if ranks[9]['score'] > threshold:
        for rank in ranks:
            if rank['score'] < threshold:
                break
            interesting_courses.append(courses[corpus[rank['corpus_id']]]['title'])
    else:
        interesting_courses = [courses[corpus[rank['corpus_id']]]['title'] for rank in ranks[:3]]
    return jsonify({"interest_courses": interesting_courses})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
