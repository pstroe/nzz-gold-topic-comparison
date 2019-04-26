#!/usr/bin/python

#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
script to extract text from xml files (tet or page xml from transkribus). saves all text in one text file per ocr
version, in the format {filename}{tab}{text}. no other preprocessing done.
"""

import argparse
import os
from lxml import etree
from multiprocessing import Pool

__author__ = "Phillip Ströbel"
__email__ = "pstroebel@cl.uzh.ch"
__organisation__ = "Institute of Computational Linguistics, University of Zurich"
__copyright__ = "UZH, 2019"
__status__ = "development"

PAGEPREFIX = '{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}'
TETPREFIX = '{http://www.pdflib.com/XML/TET3/TET-3.0}'


def extract(infile):

    parsed = etree.parse(infile)
    root = parsed.getroot()

    text = []

    split = os.path.basename(infile).split('_')

    if split[0].startswith('0'):
        split = split[1:]

    filename = 'NZZ-%s-%s-%s-%s-p%04d.txt' % (split[1][:4], split[1][4:6], split[1][6:], split[4][0], int(split[4][1:]))

    if not 'tet' in args.inFolder:
        for el in root.findall('.//%sTextRegion' % PAGEPREFIX):
            texts = el.findall('.%sTextLine/%sTextEquiv/%sUnicode' % (PAGEPREFIX, PAGEPREFIX, PAGEPREFIX))
            try:
                text_on_page = '\n'.join([text.text for text in texts])
                text.append(text_on_page)
            except TypeError:
                print('missing or empty text in file %s!' % filename + '\t' + infile)

    else:

        for el in root.findall('.//%sPara' % TETPREFIX):
            line = el.findall('.%sWord/%sText' % (TETPREFIX, TETPREFIX))
            try:
                text.append(' '.join(word.text for word in line))
            except TypeError:
                print('missing or empty text in file %s!' % filename + '\t' + infile)

    text = ' '.join(text)
    text = text.replace('¬\n', '')
    text = text.replace('\n', ' ')

    outfile.write('%s\t%s\n' % (filename, text))


if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--inFolder', help='input folder where xml files are located')
    argparser.add_argument('-o', '--outFolder', help='path to where file should be saved')
    argparser.add_argument('-f', '--outFile', help='file to which text should be written')
    args = argparser.parse_args()

    input_files = [os.path.join(args.inFolder, f) for f in os.listdir(args.inFolder)]

    outfile = open(os.path.join(args.outFolder, args.outFile), 'w')

    for xml in input_files:
        extract(xml)

    outfile.close()