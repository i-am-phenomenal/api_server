from django.http import HttpResponse
import pandas as pd
import csv
import json
from .models import File
from api_server import settings
import os

def checkIfFileWithIdExists(function): 
    def innerFunction(request, datasetId): 
        if File.objects.filter(id=datasetId).exists():
            return function(request, datasetId)
        else:
            return HttpResponse(
                json.dumps(
                    {"message": "File with given id does not exist"}
                ),
                status=500
            )
    return innerFunction

@checkIfFileWithIdExists
def getDataSetByDatasetId(request, datasetId):
    fileObject = File.objects.get(id=datasetId)
    if request.method == 'GET': 
        return HttpResponse(
            json.dumps(
                {
                    "fileName": fileObject.fileName,
                    "fileSize" : fileObject.fileSize
                }
            ),
            status=200
        )

    elif request.method== "DELETE":
        try:
            fileObject.delete()
            filePath = settings.MEDIA_ROOT +  fileObject.fileName
            os.remove(filePath)
            return HttpResponse("Succesfully deleted file from server")
        except Exception as e: 
            print(e)
            return HttpResponse(
                json.dumps(
                    "There was an error while trying to delete file"
                ),
                status=500
            )

@checkIfFileWithIdExists
def exportDatasetToExcel(request, datasetId):
    fileObject = File.objects.get(id=datasetId)
    filePath = settings.MEDIA_ROOT + fileObject.fileName
    dataFrame = pd.read_csv(filePath)
    excelFileName = fileObject.fileName.split(".")[0] + "_excel" + ".xlsx"
    excelFilePath = settings.MEDIA_ROOT + excelFileName
    excelWriterObject = pd.ExcelWriter(excelFilePath)
    dataFrame.to_excel(excelWriterObject, index=False)
    excelWriterObject.save()
    fileObject = File(
        fileName=excelFileName,
        fileSize = fileObject.fileSize
    )
    fileObject.save()
    return HttpResponse(
        json.dumps(
            {
                "filePath": excelFilePath,
                "fileName": excelFileName,
                "fileId": fileObject.id,
                "message": "File converted to excel and saved to the server"
            }
        ),
        status=200
    )

@checkIfFileWithIdExists
def getFileStats(request, datasetId):
    fileObject = File.objects.get(id=datasetId)
    filePath = settings.MEDIA_ROOT + fileObject.fileName
    dataFrame = pd.read_csv(filePath)
    stats = dataFrame.describe()
    print(stats.id, "!!!!!!!")
    for row in stats:
        print(row, type(row), "11111111111111")
    # print(stats[0], '2222222222')
    return HttpResponse("Ok")
