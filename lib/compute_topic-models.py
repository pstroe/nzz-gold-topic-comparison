#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
compute topic models for each text version
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.externals import joblib
from random import randint
import os
import sys
import argparse
import random
import pandas as pd
import numpy as np
from multiprocessing import Pool
#from infer_topics import get_doc_topics, get_topics

__author__ = "Phillip Ströbel"
__email__ = "pstroebel@cl.uzh.ch"
__organisation__ = "Institute of Computational Linguistics, University of Zurich"
__copyright__ = "UZH, 2019"
__status__ = "development"

#os.environ['OMP_NUM_THREADS'] = '50'

#stoplist_file = '/mnt/storage/karr/projects/climpresso/topicmodeling/nzz/nzz_addons/de.txt'

random.seed(42)

def lda(infile):

    #source, prep = infile.split('/')[-1].split('.')

    print(infile, file=sys.stderr, flush=True)

    #stoplist_open = open(stoplist_file, 'r')
    #stoplist = [word.strip() for word in stoplist_open.readlines()]

    infile_open = open(infile, 'r')

    lines = infile_open.readlines()

    input = [line.split('\t')[1] for line in lines if line.split('\t')[1] is not '']

    lda_pipeline = Pipeline([
        ('count', CountVectorizer()),
        ('lda', LatentDirichletAllocation())
    ])

    for num_topics in [50, 100, 150]:
        lda_pipeline.set_params(#tfidf__max_df=0.5,
                            count__min_df=10,
                            #tfidf__max_features=10000,  # also for tfidf
                            #count__stop_words=stoplist,  # also for tfidf
                            lda__n_components=num_topics,
                            lda__learning_method='batch',
                            lda__max_iter=100,
                            lda__learning_offset=50.,
                            lda__random_state=42,
                            lda__n_jobs=45)

        lda_pipeline.fit(input)

        print('# features: ', len(lda_pipeline.steps[0][1].get_feature_names()))

        display_topics(lda_pipeline.steps[1][1], lda_pipeline.steps[0][1].get_feature_names(), 20)


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx), file=sys.stderr, flush=True)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]), file=sys.stderr, flush=True)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--inputFile', help="path to txt file")
    args = argparser.parse_args()

    lda(args.inputFile)
