from fastapi import FastAPI, Path, HTTPException,Query
import json
app =FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data =json.load(f)
    return data


@app.get('/')
def hello():
    return {'message' :'Hello world'}

@app.get('/about')
def about():
        return {'message':'CampusX is an educational platform'}

@app.get('/view')
def view():
    data =load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str =Path(...,description ='ID ofthe patient  in DB', example ='p01' )):
     data =load_data()

     if patient_id in data:
          return data[patient_id]
     raise HTTPException(status_code =404, detail ='patien not found')

#query parameter

@app.get('/sort')
def sort_patient(sort_by:str =Query(..., description ='sort on the basis of height, weight or bmi '),order :str =Query('asc', description= 'sort in asc or dec order')):
     valid_fields =['height', 'weight', 'bmi']

     if sort_by not in valid_fields:
          raise HTTPException(status_code =400, detail =f'invalid field, select  from {valid_fields} ')

     if order not in ['asc','dsc']:
          raise HTTPException(status_code =400, detail ='invalid order , select from asc and dsc')

     data =load_data()
     sort_order =True if order =='dsc' else False

     sorted_data =sorted(data.values(), key =lambda x:x.get(sort_by, 0), reverse =sort_order)

     return sorted_data
