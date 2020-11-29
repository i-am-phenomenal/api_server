import requests 
import json 
import ast

ENDPOINT = "http://localhost:8000/"

def convertBytesToDictionary(content):
    dictStr = content.decode("utf-8")
    records = ast.literal_eval(repr(dictStr))
    converted = json.loads(records)
    return converted

def getAllDatasets():
    global ENDPOINT
    baseUrl = ENDPOINT + "/dataset/datasets/"
    response = requests.get(baseUrl)
    response = convertBytesToDictionary(response.content)
    print(response)

def getDatasetByDatasetId(datasetId):
    global ENDPOINT 
    baseUrl = ENDPOINT + "/dataset/datasets/" + str(datasetId)
    response = requests.get(baseUrl)
    response = convertBytesToDictionary(response.content)
    print(response)
