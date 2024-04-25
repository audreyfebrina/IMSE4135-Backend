from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument
from util.py_objectid import PyObjectId
from app import box_collection
from schemas.box import BoxCollection, BoxModel, UpdateBoxModel

box_router = APIRouter(
    prefix="/boxes",
    tags=["Boxes"],
)


@box_router.post(
    "/",
    response_description="Add a new box",
    response_model=BoxModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_box(box: BoxModel = Body(...)):
    new_box = await box_collection.insert_one(box.model_dump(by_alias=True, exclude=["id"]))
    created_box = await box_collection.find_one({"_id": new_box.inserted_id})
    return created_box


@box_router.get(
    "/",
    response_description="List all boxes",
    response_model=list[BoxModel],
    response_model_by_alias=False,
)
async def list_boxes():
    return [BoxModel(**box) for box in await box_collection.find().to_list(1000)]


@box_router.get(
    "/{id}",
    response_description="Get a single box",
    response_model=BoxModel,
    response_model_by_alias=False,
)
async def show_box(id: str):
    if (box := await box_collection.find_one({"_id": ObjectId(id)})) is not None:
        return BoxModel(**box)

    raise HTTPException(status_code=404, detail=f"Box {id} not found")


@box_router.put(
    "/{id}",
    response_description="Update a box",
    response_model=BoxModel,
    response_model_by_alias=False,
)
async def update_box(id: str, box: UpdateBoxModel = Body(...)):
    update_result = await box_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": box.model_dump(by_alias=True, exclude_none=True)},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return BoxModel(**update_result)
    else:
        raise HTTPException(status_code=404, detail=f"Box {id} not found")


@box_router.delete(
    "/{id}",
    response_description="Delete a box",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_box(id: str):
    delete_result = await box_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Box {id} not found")


@box_router.get(
    "/shelf/{shelf_id}",
    response_description="Get all boxes in a shelf",
    response_model=BoxCollection,
    response_model_by_alias=False,
)
async def list_boxes_in_shelf(shelf_id: PyObjectId):
    return [
        BoxModel(**box)
        for box in await box_collection.find({"shelf_id": shelf_id}).to_list(1000)
    ]
