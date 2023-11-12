from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzy_match import algorithims
from difflib import SequenceMatcher
import re

app = Flask(__name__)

def preprocess_string(s):
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    s = s.lower()
    return s.strip()

def validate_input(fromString, toString):
    if not fromString or not toString:
        return False
    if len(fromString) < 3 or len(toString) < 3:
        return False
    return True

def fuzzy_match_percentage(fromString, toString):
    is_valid = validate_input(fromString, toString)
    if not is_valid:
        return "Validation Failed","Validation Failed" # Return default values when validation fails
    else:
        try:
            fuzzy_trigram = algorithims.trigram(fromString, toString)
            fuzzy_cosine = algorithims.cosine(fromString, toString)
            
            return fuzzy_trigram, fuzzy_cosine
        except Exception as e:
            return 0.0,0.0

def difflib_percentage(fromString, toString):
    is_valid = validate_input(fromString, toString)
    if not is_valid:
        return "Validation Failed"
    else:

        try:
            matcher = SequenceMatcher(None, fromString, toString)
            difflib_p = matcher.ratio()

            return difflib_p
        except Exception as e:
            return 0.0
    
def sklearn_cosine(fromString, toString):
    is_valid = validate_input(fromString, toString)
    if not is_valid:
        return "Validation Failed"
    else:
        try:
            vectorizer = CountVectorizer().fit_transform([fromString, toString])
            cosine_similarity_matrix = cosine_similarity(vectorizer)
            sklearn_cosine = cosine_similarity_matrix[0, 1]

            return sklearn_cosine
        except Exception as e:
            return 0.0

@app.route('/stringmatch', methods=['POST'])
def fuzzy_match():
    try:
        data = request.get_json()

        if 'fromString' not in data or 'toString' not in data:
            return jsonify({'error': 'Both "fromString" and "toString" must be provided in the request'}), 400

        fromString = data['fromString']
        toString = data['toString']
        
        fromString = preprocess_string(fromString)
        toString = preprocess_string(toString)
        
        print(fromString, toString)
    
        fuzzy_trigram, fuzzy_cosine = fuzzy_match_percentage(fromString, toString)
        difflib_percentage_val = difflib_percentage(fromString, toString)
        sklearn_cosine_val = sklearn_cosine(fromString, toString)
        

        response = {
            'fuzzy_trigram_percentage': fuzzy_trigram,
            'fuzzy_cosine_percentage': fuzzy_cosine,
            'sklearn_cosine_percentage': sklearn_cosine_val,
            'difflib_percentage': difflib_percentage_val
        }

        return jsonify(response)
    except Exception as e:
         return "Interval Server Error :" + str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
