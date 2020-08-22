import pandas as pd
import string
import re
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import os
from django.conf import settings
from nbapputils import Nbfunctions
from testclass import TestClassFunction



nbf=Nbfunctions()
print(nbf.Predict("test test test test test test. test2 test2 test2 test2 test2 test2."))

#testclassobj=TestClassFunction()
#print(testclassobj.getHelloWorld())
#testclassobj.printHello()