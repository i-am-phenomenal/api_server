from django.shortcuts import render
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pandas as pd
# Create your views here.

class DatasetView(View):
    def post(self, request): 
        params = request.body.decode("utf-8")
        # csvFile = request.FILE["file"]
        # print(csvFile)
        # dataFrame = pd.read_csv(csvFile, sep=',')
        # print(dataFrame)
        return HttpResponse("ok")
