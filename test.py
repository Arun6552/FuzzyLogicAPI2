from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzy_match import algorithims
import re


def preprocess_string(s):
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    s = s.lower()
    return s.strip()


str1 = "ARU'.[;'n] Kuma"
str2 = "arun,.; kuma"
str1 = preprocess_string(str1)
str2  = preprocess_string(str2)
print(str1,str2)
 
Per = algorithims.trigram(str1,str2)
perc1 = algorithims.cosine(str1,str2)
print(Per,perc1)


vectorizer = CountVectorizer().fit_transform([str1, str2])
cosine_similarity_matrix = cosine_similarity(vectorizer)
cosine_similarity = cosine_similarity_matrix[0, 1]

print(cosine_similarity)