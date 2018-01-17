# Corpus-linguistics

This repository includes data and code that goes together with the examples described in the article "Määrällinen korpuslingvistiikka" in the book "Kielentutkimuksen metodologiat" in Finnish.

1. Keywords estimated with log likelihood.

log_ll.py counts keywords for the data provided in koyha-kommentit-2014.txt.gz in comparison with the reference corpus provided in reference.txt.gz.
Try: python log_ll.py

log_ll_content_words.py counts keywords but uses only content words. Otherwise similar to log_ll.py
Try: python log_ll_content_words.py

2. Keywords estimated with an SVM

svm.py builds a standard two-class support vector machine classifier and estimates keywords or key features for the text classes. To be used together with preprocess.py, which preprocesses koyha-kommentit-2014.txt.gz and no-koyha.txt.gz so that each comment is on one line, preceded by the class label.
Try: python preprocess.py | python svm.py