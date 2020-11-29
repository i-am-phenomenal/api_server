from django.http import HttpResponse
import pandas as pd
import csv
import json
from .models import File
from api_server import settings
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

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

def getFormattedStats(val):
    return {
        "count": val["count"],
        "mean": val["mean"],
        "std": val["std"],
        "min": val["min"],
        "25%": val["25%"],
        "50%": val["50%"],
        "75%": val["75%"],
        "max": val["max"]
    }

@checkIfFileWithIdExists
def getFileStats(request, datasetId):
    fileObject = File.objects.get(id=datasetId)
    filePath = settings.MEDIA_ROOT + fileObject.fileName
    dataFrame = pd.read_csv(filePath)
    stats = dataFrame.describe()
    idStats = getFormattedStats(stats.id)
    zipStats = getFormattedStats(stats.zip)
    versionStats = getFormattedStats(stats.version)
    return HttpResponse(
        json.dumps(
            {
                "idStats": idStats,
                "zipStats": zipStats,
                "versionStats": versionStats
            }
        ),
        status=200
    )

def returnOnlyNumericColumns(formattedValues): 
    numericCols = []
    for key in formattedValues: 
        values = formattedValues[key]
        if all(isinstance(val, int) for val in values): 
            numericCols.append({
                "key": key,
                "values": values
            })
        else:
            pass
    return numericCols

@checkIfFileWithIdExists
def generateAndReturnPdf(request, datasetId):
    fileObject = File.objects.get(id=datasetId)
    filePath = settings.MEDIA_ROOT + fileObject.fileName
    dataFrame = pd.read_csv(filePath)
    formattedValues = {}
    for col in dataFrame:
        formattedValues[col] = dataFrame[col].to_list()
    numericCols = returnOnlyNumericColumns(formattedValues)
    trimmedFileName = fileObject.fileName.split(".")[0]
    pdfFile = PdfPages(settings.MEDIA_ROOT +  trimmedFileName + ".pdf")
    for numericCol in numericCols:
        fig = plt.hist(np.array(numericCol["values"]), bin=50)
        # trimmedFileName = fileObject.fileName.split(".")[0]
        # pdfFilePath =  settings.MEDIA_ROOT +  trimmedFileName +str(iter) +  ".pdf"
        pdfFile.savefig(fig, bbox_inches="tight")
    with open(pdfFilePath, "rb") as file: 
        response = HttpResponse(file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=" + os.path.basename(pdfFilePath)
        return response
    

