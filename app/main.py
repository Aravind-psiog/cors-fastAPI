from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json


# only used for aws for loading Swagger doc. Doesnot work on local machine
# app = FastAPI(root_path="/dev/")
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         'Access-Control-Allow-Headers': 'Content-Type',
    #         'Access-Control-Allow-Origin': '*',
    #         'Access-Control-Allow-Methods': '*'
    #     },
    #     'body': json.dumps('Hello from Lambda!')
    # }
    content = {"message": "Hello World"}
    headers = {'Access-Control-Allow-Headers': 'Content-Type',
               'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': '*'}
    return JSONResponse(content=content, headers=headers)


handler = Mangum(app)
