import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from ..data_model.PriorityPredictor import PriorityPredictor, DataSourceAdapter, DataClasifier



router = APIRouter()

class PredictionRequest(BaseModel):
    id: Optional[int]
    name: Optional[str]
    expiresAt: str = Field(..., description="The expiration date of the item, required")
    price: float = Field(..., description="The price of the item, required")
    weight: Optional[str]
    packagingUnit: Optional[str]
    available: int = Field(..., description="The quantity available, required")
    SalesRateDay: float = Field(..., description="The sales rate per day, required")

# @router.post("/", response_description="Add new noun type", response_model=NounTypeModel)
# async def create_noun(noun: NounTypeModel = Body(...)):
#     noun = jsonable_encoder(noun)
#     new_noun = await noun_collection.insert_one(noun)
#     created_noun = await noun_collection.find_one({"_id": new_noun.inserted_id})
#     return created_noun

@router.post("/items_per_priorities/", response_description="Get items in stage sent ")
async def get_items_by_stage(request: List[int]):
     
     data = DataSourceAdapter('json', 'app\\tests\\testing_data.json')
     clasifier = DataClasifier(data)
     return {"body": clasifier.filter_data('priority', request).to_dict(orient='records')}
     #raise HTTPException(status_code=404, detail=f"Noun type with ID {id} not found")



@router.post("/predict_stage/")
async def predict_stage(request: List[PredictionRequest]):
    data_dicts = [item.dict() for item in request]
    data = DataSourceAdapter('json', 'app\\tests\\testing_data.json')
    predictor = PriorityPredictor(data, )
    prediction,prediction_classes=predictor.make_predictions(data_dicts)
    return {"body": f"{prediction_classes}"}


@router.get("/percentage/{atribute}", response_description="Get items in stage sent ")
async def show_percentages(atribute: str):
    data = DataSourceAdapter('json', 'app\\tests\\testing_data.json')
    clasifier = DataClasifier(data)
    frequency = clasifier.get_frequency(atribute)
    percentage = clasifier.get_ratio(atribute)

    if set(frequency.keys()) != set(percentage.keys()):
        raise HTTPException(status_code=500, detail="Frequency and ratio keys do not match")

    # Combine frequency and ratio into a single dictionary with tuples
    combined = {key: {'count':frequency[key], 'percentage': percentage[key]} for key in frequency}

    return {"body" : combined}




