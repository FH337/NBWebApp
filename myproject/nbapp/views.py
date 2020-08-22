from django.shortcuts import render, redirect 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Emiten, TbpTable2
from .filters import EmitenFilter, TbpTable2Filter
from .forms import EmitenForm, TbpTable2Form
from .nbapputils import Nbfunctions
import pandas as pd
import string
import re
import random
import numpy as np
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
import pickle


def home(request):
    return render(request, "home.html",{})

def about(request):
    return render(request, "about.html",{})


def tbp_table2_list(request):
    tbp_table2_list=TbpTable2.objects.all().order_by('-date')
    emiten_list=Emiten.objects.all().order_by('emiten_name')
    return render(request, 'tbp-table2-list.html', {'tbp_table2_list':tbp_table2_list, 'emiten_list': emiten_list})


def tbp_table2_delete(request, id):
    tbp_table2 = TbpTable2.objects.get(id=id)
    try:
        tbp_table2.delete()
    except:
        print("except")
    return redirect("/tbp-table2-list/") 

def tbp_table2_breakdown(request, id):
    tbp_table2 = TbpTable2.objects.get(id=id)
    percentage=1
    df_0, df_1copy, df0, df1, TF0, TF1, IDF0, IDF1, TFIDF0, TFIDF1, percentTFIDF0, percentTFIDF1, PriorPOS,  PriorNEG, ListSent=Nbfunctions.nbprocess(tbp_table2.paragraph, percentage)
    percentagePOS, percentageNEG= getPersentase(ListSent)
    return render(request, 'tbp-table2-breakdown.html', {
        "id":id, 
        "tbp_table2":tbp_table2,
        "outputs":ListSent,
        "df_0":df_0,  
        "df_1copy": df_1copy, 
        "df0": df0,
        "df1": df1,
        "TF0": TF0,
        "TF1": TF1,
        "IDF0": IDF0,
        "IDF1": IDF1,
        "TFIDF0": TFIDF0,
        "TFIDF1": TFIDF1,
        "percentTFIDF0":percentTFIDF0,
        "percentTFIDF1": percentTFIDF1,
        "PriorPOS": PriorPOS,
        "PriorNEG": PriorNEG,
        "percentagePOS":percentagePOS,
        "percentageNEG":percentageNEG})


def emiten_add(request):
    if request.method == "POST":  
        form = EmitenForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/tbp-table2-list/')  
            except:  
                pass  
    else:  
        form = EmitenForm()  
    return render(request,'emiten-add.html',{'form':form})

def emiten_list(request):
    emiten_list = Emiten.objects.all()
    emiten_filter = EmitenFilter(request.GET, queryset=emiten_list)
    emiten_filter_qs= emiten_filter.qs
    paginator = Paginator(emiten_filter_qs, 5)  # Show 5 rows per page
    page = request.GET.get('page')
    try:
        emiten_filter_qs = paginator.page(page)
    except PageNotAnInteger:
        emiten_filter_qs = paginator.page(1)
    except EmptyPage:
        emiten_filter_qs = paginator.page(paginator.num_pages)
    return render(request, 'emiten-list.html', {'emiten_filter': emiten_filter, 'emiten_filter_qs':emiten_filter_qs})

def emiten_detail(request, id):
    emiten=Emiten.objects.get(id=id)
    return render(request, "emiten-detail.html",{"emiten":emiten})

def emiten_edit(request, id):
    emiten= Emiten.objects.get(id=id)
    return render(request, "emiten-edit.html", {'emiten':emiten})

def emiten_updated(request, id):  
    emiten = Emiten.objects.get(id=id)  
    form = EmitenForm(request.POST, instance = emiten)  
    if form.is_valid():  
        form.save()  
        return redirect("/emiten-detail/"+str(id))  
    return render(request, 'emiten-edit.html', {'emiten': emiten})  

def emiten_delete(request, id):
    emiten = Emiten.objects.get(id=id)
    try:
        emiten.delete()
    except:
        print("except")
    return redirect("/emiten-list/") 

def getPersentase(listSentence):
    percentagePOS_count=0
    percentageNEG_count=0
    percentage_count=0
    for k, v in listSentence.items():
        if (v=="POS"):
            percentagePOS_count=percentagePOS_count+1
        else:
            percentageNEG_count=percentageNEG_count+1
        percentage_count=percentage_count+1
    percentagePOS=str(round(100*percentagePOS_count/percentage_count, 2))+" %"
    percentageNEG=str(round(100*percentageNEG_count/percentage_count, 2))+" %"
    
    return percentagePOS, percentageNEG

def test(request):
    testdata=""
    option=""
    checked1="checked"
    checked2=""
    checked3=""
    checked4=""
    ListSent=""
    df_0=""  
    df_1copy=""
    df0=""
    df1=""
    TF0=""
    TF1="" 
    IDF0=""
    IDF1=""
    TFIDF0=""
    TFIDF1=""
    percentTFIDF0="" 
    percentTFIDF1=""
    percentagePOS="" 
    percentageNEG=""
    PriorPOS=""  
    PriorNEG=""
    if request.method == "POST":
        testdata=request.POST["rawdata"]
        option=request.POST["inlineRadioOptions"]
        if (option=="10"):
            checked1="checked"
        elif (option=="25"):
            checked2="checked";
        elif (option=="50"):
            checked3="checked"
        elif (option=="100"):
            checked4="checked";
        percentage=int(option)/100
        df_0, df_1copy, df0, df1, TF0, TF1, IDF0, IDF1, TFIDF0, TFIDF1, percentTFIDF0, percentTFIDF1, PriorPOS,  PriorNEG, ListSent=Nbfunctions.nbprocess(testdata, percentage)
        percentagePOS, percentageNEG= getPersentase(ListSent)
        

    return render(request, "test.html",{
        "testdata":testdata, 
        "option": option, 
        "checked1":checked1, 
        "checked2":checked2, 
        "checked3":checked3, 
        "checked4":checked4, 
        "df_0":df_0,  
        "df_1copy": df_1copy, 
        "df0": df0,
        "df1": df1,
        "TF0": TF0,
        "TF1": TF1,
        "IDF0": IDF0,
        "IDF1": IDF1,
        "TFIDF0": TFIDF0,
        "TFIDF1": TFIDF1,
        "percentTFIDF0":percentTFIDF0,
        "percentTFIDF1": percentTFIDF1,
        "PriorPOS": PriorPOS,
        "PriorNEG": PriorNEG,
        "percentagePOS": percentagePOS,
        "percentageNEG": percentageNEG,
        "outputs":ListSent,
        })

def error_404_view(request, exception):
    return render(request,'error_404.html', {})
