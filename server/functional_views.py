from django.http import HttpResponse
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