from __future__ import division
import gzip
import sys
import math

class NGram(object):

    def __init__(self,ng):
        self.ng=ng
        self.counts={} #key: corpus  value: count

    def count(self,corpus,occ_num=1):
        """Count an occurrence of the ngram in a given corpus"""
        self.counts[corpus]=self.counts.get(corpus,0)+occ_num


    def ll(self,corpus_name,corpus_counts,total):
        """corpus_counts: count for every corpus, total: the grand total of all ngrams"""
        #http://ucrel.lancs.ac.uk/llwizard.html
        
        sum_O_i=sum(c for c in self.counts.itervalues())

        O_1=self.counts.get(corpus_name,0)
        N_1=corpus_counts[corpus_name]
        E_1=N_1*sum_O_i/total

        O_2=sum_O_i-O_1 #Reference
        N_2=total-corpus_counts[corpus_name] #all other corpora but this one -> reference
        E_2=N_2*sum_O_i/total

        #Skip zero-counts
        ll=0.0
        if O_1>0:
            ll+= O_1*math.log(O_1/E_1)
        if O_2>0:
            ll+=O_2*math.log(O_2/E_2) 

        return 2.0*ll
        

def get_corpus_counts(ngrams):
    corpus_counts={} #{corpus_name:total_count}
    for ng in ngrams.itervalues():
        for corpus,count in ng.counts.iteritems():
            corpus_counts[corpus]=corpus_counts.get(corpus,0)+count
    return corpus_counts, sum(count for count in corpus_counts.itervalues())


def read(f_name,corpus_name,ngrams,max_lines=0):
    """ngrams: {ngram:NGram object}"""
    if f_name.endswith(".gz"):
        f=gzip.open(f_name,"r")
    else:
        f=open(f_name,"r")
    for line_idx,line in enumerate(f):
        line=unicode(line.strip(),"utf-8")
        if not line:
            continue
        if line not in ngrams:
            ng=NGram(line)
            ngrams[line]=ng
        else:
            ng=ngrams[line]
        #Now ng is an NGram() object
        ng.count(corpus_name) #counts 1 by the default
        if max_lines>0 and line_idx>max_lines:
            break

def highest_ll_ngrams(corpus_name,ngrams,corpus_counts,total):
    res=[]
    for ng in ngrams.itervalues():
        res.append((ng,ng.ll(corpus_name,corpus_counts,total))) 
    #Res is now a list of (NGram(),ll-value)
    res.sort(reverse=True,key=lambda x: x[1]) #sort descending on that ll-value
    return res

if __name__=="__main__":
    ngrams={} #key: ngram_string, value: NGram()
    corpora=[("Suomi24","kom.gz"),("Reference corpus","ver.gz")]#,("math","triarcs_wikidisc_math.gz")]
    for corpus_name,corpus_file in corpora:
        print >> sys.stderr, "Reading", corpus_name,
        read(corpus_file,corpus_name,ngrams)
        print >> sys.stderr, " ...done"
    
    corpus_counts,total=get_corpus_counts(ngrams)
    
    show_max=50
    for corpus_name,_ in corpora:
        ngrams_and_ll=highest_ll_ngrams(corpus_name,ngrams,corpus_counts,total)[:show_max]
        print "-"*50
        print corpus_name
        for ng,ll in ngrams_and_ll:
            print (u"ll=%.3f   FREQ=%d/%d   %s"%(ll,ng.counts.get(corpus_name,0),sum(ng.counts.itervalues()),ng.ng)).encode("utf-8")

        
    
