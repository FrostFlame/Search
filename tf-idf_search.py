import math
from functools import reduce

from binary_search import get_list_of_lexems, ArticleTerm, TermList
from crawl import Article


def count_idf(word):
    word_id = TermList.select(TermList.term_id).where(TermList.term_text == word)
    x = ArticleTerm.select().where(ArticleTerm.term_id == word_id).count()
    if x == 0:
        idf = 0
    else:
        idf = math.log10(30 / x)
    return idf


def search(request):
    words = get_list_of_lexems(request)
    request_vector = list(map(count_idf, words))
    request_ids = []

    article_ids = set()
    for word in words:
        word_id = list(TermList.select().where(TermList.term_text == word))[0].term_id
        request_ids.append(word_id)
        a = ArticleTerm.select(ArticleTerm.article_id).where(ArticleTerm.term_id == word_id)
        # print(len(a))
        for e in a:
            article_ids.add(e.article_id.id)

    article_idfs = {}
    for article in article_ids:
        vector = []
        for w_id in request_ids:
            a = ArticleTerm.select(ArticleTerm.tf_idf).where(
                (ArticleTerm.article_id == article) & (ArticleTerm.term_id == w_id))
            if a:
                vector.append(a[0].tf_idf)
            else:
                vector.append(0)
        article_idfs[article] = vector
    # print(article_idfs)
    cos_values = {}
    for e in article_idfs.keys():
        doc_vector = article_idfs[e]
        cos = sum([a * b for a, b in zip(request_vector, doc_vector)]) \
              / (math.sqrt(sum(a * a for a in request_vector)) * math.sqrt(sum(b * b for b in doc_vector)))
        cos_values[e] = cos

    sorted_by_cos = sorted(cos_values.items(), key=lambda kv: kv[1], reverse=True)
    for i in range(10):
        id = sorted_by_cos[i][0]
        cos = sorted_by_cos[i][1]
        a = Article.select(Article.url).where(Article.id == id)
        print(a[0].url + ' ' + str(cos))


if __name__ == '__main__':
    s = 'ведьмак от мира сериалов'
    print(s)
    search(s)
