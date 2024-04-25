from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument
from util.create_objectid import create_objectid
from schemas.prisoner import PrisonerModel, UpdatePrisonerModel, PrisonerCollection
from app import prisoner_collection
from util.hk_time_now import hk_time_now

prisoner_router = APIRouter(
    prefix="/prisoners",
    tags=["Prisoners"],
)


@prisoner_router.post(
    "/",
    response_description="Add a new prisoner",
    response_model=PrisonerModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_prisoner(prisoner: PrisonerModel = Body(...)):
    govn_id = prisoner.id_number
    new_prisoner = await prisoner_collection.insert_one(
        {**prisoner.model_dump(by_alias=True), "_id": create_objectid(govn_id)}
    )
    created_prisoner = await prisoner_collection.find_one(
        {"_id": new_prisoner.inserted_id}
    )
    return created_prisoner


@prisoner_router.get(
    "/",
    response_description="List all prisoners",
    response_model=PrisonerCollection,
    response_model_by_alias=False,
)
async def list_prisoners():
    return PrisonerCollection(
        prisoners=[
            PrisonerModel(**prisoner)
            for prisoner in await prisoner_collection.find().to_list(1000)
        ]
    )


@prisoner_router.get(
    "/{id}",
    response_description="Get a single prisoner",
    response_model=PrisonerModel,
    response_model_by_alias=False,
)
async def show_prisoner(id: str):
    if (
        prisoner := await prisoner_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return PrisonerModel(**prisoner)

    raise HTTPException(status_code=404, detail=f"Prisoner {id} not found")


@prisoner_router.put(
    "/{id}",
    response_description="Update a prisoner",
    response_model=PrisonerModel,
    response_model_by_alias=False,
)
async def update_prisoner(id: str, prisoner: UpdatePrisonerModel = Body(...)):
    prisoner_data = prisoner.model_dump(by_alias=True, exclude_none=True)
    prisoner_data["last_updated"] = hk_time_now()
    update_result = await prisoner_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": prisoner_data},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return PrisonerModel(**update_result)
    else:
        raise HTTPException(status_code=404, detail=f"Prisoner {id} not found")


@prisoner_router.delete(
    "/{id}",
    response_description="Delete a prisoner",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_prisoner(id: str):
    delete_result = await prisoner_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Prisoner {id} not found")


@prisoner_router.get(
    "/officer/{officer_id}",
    response_description="Get all prisoners under an officer",
    response_model=PrisonerCollection,
    response_model_by_alias=False,
)
async def get_prisoners_in_officer(officer_id: str):
    prisoners = await prisoner_collection.find({"officer_id": officer_id}).to_list(1000)
    return PrisonerCollection(
        prisoners=[PrisonerModel(**prisoner) for prisoner in prisoners]
    )
