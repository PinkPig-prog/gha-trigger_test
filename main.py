from fastapi import FastAPI, Body
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OWNER = "PinkPig-prog"   
REPO = "gha-trigger_test"      
WORKFLOW_FILE = "deploy.yml"  
TOKEN = os.getenv("GITHUB_TOKEN") 

@app.post("/deploy-model")
def deploy_model(config: dict = Body(...)):
    """
    API endpoint that triggers a GitHub Actions workflow with model config details.
    """
    if not TOKEN:
        return {"error": "GITHUB_TOKEN not set in environment"}

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {"Authorization": f"token {TOKEN}"}
    
    data = {
        "ref": "main", 
        "inputs": config
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 204:
        return {"message": "Workflow triggered successfully", "config": config}
    else:
        return {"error": response.json()}

