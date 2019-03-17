import math


from binary_search import ArticleTerm
from preprocessing import WordsPorter


def tf_idf():
    article_terms = ArticleTerm.select()
    for elem in article_terms:
        tf = WordsPorter.select().where((WordsPorter.term == elem.term_id.term_text) & (
                WordsPorter.article_id == elem.article_id)).count() / WordsPorter.select().where(
            WordsPorter.article_id == elem.article_id).count()
        idf = math.log10(30 / (ArticleTerm.select().where(ArticleTerm.term_id == elem.term_id).count()))
        ArticleTerm.update(tf_idf=tf * idf).where(ArticleTerm.id == elem.id).execute()


if __name__ == '__main__':
    tf_idf()
