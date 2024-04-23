from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import ReturnDocument
from utils.create_objectid import create_objectid
from utils.py_objectid import PyObjectId
from app import bag_collection
from models.bag import BagModel, BagCollection

bag_router = APIRouter(
    prefix="/bags",
    tags=["Bags"],
)


@bag_router.post(
    "/",
    response_description="Add a new bag",
    response_model=BagModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_bag(bag: BagModel = Body(...)):
    bag_epc = bag.rfid_epc
    new_bag = await bag_collection.insert_one(
        {**bag.model_dump(by_alias=True), "_id": create_objectid(bag_epc)}
    )
    created_bag = await bag_collection.find_one({"_id": new_bag.inserted_id})
    return created_bag


@bag_router.get(
    "/",
    response_description="List all bags",
    response_model=BagCollection,
    response_model_by_alias=False,
)
async def list_bags():
    return BagCollection(
        bags=[BagModel(**bag) for bag in await bag_collection.find().to_list(1000)]
    )


@bag_router.get(
    "/{id}",
    response_description="Get a single bag",
    response_model=BagModel,
    response_model_by_alias=False,
)
async def show_bag(id: str):
    if (bag := await bag_collection.find_one({"_id": ObjectId(id)})) is not None:
        return BagModel(**bag)

    raise HTTPException(status_code=404, detail=f"Bag {id} not found")


@bag_router.put(
    "/{id}",
    response_description="Update a bag",
    response_model=BagModel,
    response_model_by_alias=False,
)
async def update_bag(id: str, bag: BagModel = Body(...)):
    update_result = await bag_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": bag.model_dump(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return BagModel(**update_result)
    else:
        raise HTTPException(status_code=404, detail=f"Bag {id} not found")


@bag_router.delete(
    "/{id}",
    response_description="Delete a bag",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bag(id: str):
    delete_result = await bag_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Bag {id} not found")


@bag_router.get(
    "/box/{box_id}",
    response_description="Get bags by box_id",
    response_model=BagCollection,
    response_model_by_alias=False,
)
async def get_bags_by_box_id(box_id: PyObjectId):
    bags = [BagModel(**bag) async for bag in bag_collection.find({"box_id": box_id})]
    return BagCollection(bags=bags)


@bag_router.get(
    "/prisoner/{prisoner_id}",
    response_description="Get bags by prisoner_id",
    response_model=BagCollection,
    response_model_by_alias=False,
)
async def get_bags_by_prisoner_id(prisoner_id: PyObjectId):
    bags = [
        BagModel(**bag)
        async for bag in bag_collection.find({"prisoner_id": prisoner_id})
    ]
    return BagCollection(bags=bags)
