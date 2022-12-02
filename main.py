import requests
import json
from docker import Client
import os
import time

global token


with open("data.json","r") as file:
    file=file.read()
    fileData = json.loads(file)
    token = fileData["secrets"]["token"]
    lista = fileData["data"]

    print("retrived data")


# put here an example of status i name my status proprety "status"
data = {  "properties":{"status":{"id":"%3C%3B%3Av","type":"status","status":{"name":"currently working"}}} }

# standard headers
headers = {
    "Authorization": "Bearer "+token ,
    "Notion-Version": "2022-06-28"
}

headers_for_change = {
    "Authorization": "Bearer "+token ,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def ReadPage(pageId,headers):
    readUrl = f"https://api.notion.com/v1/pages/{pageId}"
    res = requests.request("GET",readUrl, headers=headers)
    data = res.json()
    print(data["properties"]["status"]["status"]["name"])


def UpdatePage(pageId,headers_for_change,data,statValue):
    data["properties"]["status"]["status"]["name"]=statValue
    readUrl = f"https://api.notion.com/v1/pages/{pageId}"
    requests.request("PATCH",readUrl, headers=headers_for_change,json=data)


if __name__ == "__main__":

    # open the connection thith docker
    cli = Client(base_url='unix://var/run/docker.sock') # open a connecrio to the daemon


    while (1):
        containers = cli.containers(all=True)  # get all the containers == docker ps -all
        for i in range(len(lista)): # for every container to ceck
            for container in range(len(containers)): # search 
                status=containers[container]["Status"].split(" ",1)[0]
                if containers[container]["Id"] == lista[i]["containerId"]:
                    if status != lista[i]["previusStatus"] :  # if state has changed from last time
                        lista[i]["previusStatus"] = status    # set to equal
                        if(status == "Up"):
                            UpdatePage(lista[i]["pageId"],headers,data,"currently working")
                        else:
                            UpdatePage(lista[i]["pageId"],headers,data,"not working")
                    break # i've found what i was looking for

        time.sleep(10)
  
    """
    some useful debughing tools

    for container in range(len(containers)):
    #for key in containers[container]:
        print(containers[container]["Id"])
        print(containers[container]["Names"])
        print(containers[container]["Status"])
        print(type(containers[container]["Status"]))
        print("\n")
    
    ReadPage(pageId,headers)
    UpdatePage(pageId,headers,data,"Not started")
    ReadPage(pageId,headers)
    UpdatePage(pageId,headers,data,"currently working")
    ReadPage(pageId,headers)
    """