import math
import pickle

from numpy.linalg import svd
import numpy as np

from binary_search import get_list_of_lexems, ArticleTerm, TermList
from crawl import *


def search(request, k=5):
    words = [word.term_text for word in TermList.select(TermList.term_text)]
    # matrix = []
    docs = Article.select(Article.id)
    q = []
    for word in words:
        # w_vector = []
        # for d in docs:
        #     if ArticleTerm.select().join(TermList).distinct().where(TermList.term_text == word,
        #                                                             ArticleTerm.article_id == d.id).count():
        #         w_vector.append(1)
        #     else:
        #         w_vector.append(0)
        # matrix.append(w_vector)
        if word in get_list_of_lexems(request):
            q.append(1)
        else:
            q.append(0)
    q = np.array(q)
    # pickle.dump(matrix, open('matrix.txt', 'wb'))
    matrix = pickle.load(open('matrix.txt', 'rb'))
    matrix = np.array(matrix)
    u, s, v = svd(matrix)
    u = u[:, :5]
    s = s[:5]
    s = np.diag(s)
    v = v[:, :5]
    q = q.reshape(1, 9012)
    q = np.dot(q, u)
    request_vector = np.dot(q, s)
    request_vector = request_vector[0]

    cos_values = {}
    for doc_id, doc_vector in zip(docs, v):
        cos = sum([a * b for a, b in zip(request_vector, doc_vector)]) \
              / (math.sqrt(sum(a * a for a in request_vector)) * math.sqrt(sum(b * b for b in doc_vector)))
        cos_values[doc_id.id] = cos

    sorted_by_cos = sorted(cos_values.items(), key=lambda kv: kv[1], reverse=True)
    for i in range(10):
        id = sorted_by_cos[i][0]
        cos = sorted_by_cos[i][1]
        a = Article.select(Article.url).where(Article.id == id)
        print(a[0].url + ' ' + str(cos))


if __name__ == '__main__':
    search(request='ведьмак от мира сериалов больше слов для запроса')
