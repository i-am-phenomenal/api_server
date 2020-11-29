from django.shortcuts import render
from django.views import View
import json
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import csv
import pandas as pd
from io import StringIO, TextIOWrapper
from api_server import settings
import os

# Create your views here.

class DatasetView(View):

    def getNumberOfFilesOnMediaDir(self):
        dirName = settings.MEDIA_ROOT
        files = os.listdir(dirName)
        return str(len(files))

    def post(self, request): 
        params = request.body.decode("utf-8")
        myFile = request.FILES["file"]
        file = myFile.read().decode("utf-8")
        reader = csv.DictReader(StringIO(file))
        data = [line for line in reader]
        columnNames = data[0].keys()
        dataFrame = pd.DataFrame(data, columns=columnNames)
        filePath = settings.MEDIA_ROOT + "file" + self.getNumberOfFilesOnMediaDir() + ".csv"
        try: 
            dataFrame.to_csv(filePath, index=False)
            return HttpResponse(
                json.dumps(
                    {
                        "filePath": filePath,
                        "message": "File saved as pandas dataframe successfully !"
                    }
                ),
                status=200
            )
        except Exception as e: 
            return HttpResponse(
                json.dumps(
                    str(e)
                ),
                status=500
            )
        
