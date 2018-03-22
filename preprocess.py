# -*- coding: utf-8 -*-
#from __future__ import print_function
import sys
import codecs
import gzip


search_words = [u'köyhä', u'rutiköyhä', u"ruti#köyhä", u"rahaton", u"persaukinen", u"pers#aukinen", u"vähävarainen", u"vähä#varainen", u"perseaukinen", u"perse#aukinen", u"tyhjätasku", u"tyhjä#tasku", u"pienituloinen", u"pieni#tuloinen",  u"sossupummi", u"sossu#pummi", u"saita", u"sosiaalipummi", u"sosiaali#pummi", u"varaton", u"eläkeläinen", u"pienipalkkainen", u"pieni#palkkainen"]

pos_not_to_keep = [u"PUNCT", u"SCONJ", u"CONJ", u"AUX", u"PRON"] 

out8 = codecs.getwriter(u"utf-8")(sys.stdout)

def read_comment(corpus_l, file_n):
  f=gzip.open(file_n, "r")
  comment=[]
  for line in f:
      
      line=unicode(line.strip(),"utf-8")
      if line.startswith("#"):
          continue
      if not line:
          if comment:
              print >> out8, corpus_l, u" ".join([word for word in comment])
              comment=[]
      else:
          line=line.split("\t")
          try:
              if  line[1].strip() not in search_words:
                  if line[2].strip() not in pos_not_to_keep:
                      comment.append(line[1].strip())
          except: continue 
          
if __name__=="__main__":

  corpora=["koyha-kommentit-2014.txt.gz", "no-koyha.txt.gz"]
  for label, file in enumerate(corpora):
    read_comment(label, file)
