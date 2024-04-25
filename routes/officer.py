from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from schemas.officer import (
    OfficerModel,
    UpdateOfficerModel,
    OfficerCollection,
    SignupModel,
    LoginModel,
)
from app import officer_collection
from schemas.prisoner import PrisonerModel
from util.create_objectid import create_objectid

officer_router = APIRouter(
    prefix="/officers",
    tags=["Officers"],
)


@officer_router.post(
    "/signup",
    response_description="Add a new officer",
    response_model=OfficerModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def signup_officer(data: SignupModel = Body(...)):
    officer_id = data.officer_id
    new_officer = await officer_collection.insert_one(
        {**data.model_dump(by_alias=True), "_id": create_objectid(officer_id)}
    )
    created_officer = await officer_collection.find_one(
        {"_id": new_officer.inserted_id}
    )
    return OfficerModel(**created_officer)


@officer_router.post(
    "/login",
    response_description="Officer login",
    status_code=status.HTTP_200_OK,
)
async def login_officer(data: LoginModel = Body(...)):
    matching_officer = await officer_collection.find_one(
        {"officer_id": data.officer_id, "password": data.password}
    )
    if matching_officer:
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=401, detail="Invalid officer ID or password")


@officer_router.get(
    "/",
    response_description="List all officers",
    response_model=OfficerCollection,
    response_model_by_alias=False,
)
async def list_officers():
    officers = await officer_collection.find().to_list(1000)
    return OfficerCollection(officers=[OfficerModel(**officer) for officer in officers])


@officer_router.get(
    "/{id}",
    response_description="Get a single officer",
    response_model=OfficerModel,
    response_model_by_alias=False,
)
async def show_officer(id: str):
    if (officer := await officer_collection.find_one({"officer_id": id})) is not None:
        return OfficerModel(**officer)

    raise HTTPException(status_code=404, detail=f"Officer {id} not found")


@officer_router.put(
    "/{id}",
    response_description="Update an officer",
    response_model=OfficerModel,
    response_model_by_alias=False,
)
async def update_officer(id: str, officer: UpdateOfficerModel = Body(...)):
    update_result = await officer_collection.find_one_and_update(
        {"officer_id": id},
        {"$set": officer.model_dump(by_alias=True, exclude_none=True)},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return OfficerModel(**update_result)
    else:
        raise HTTPException(status_code=404, detail=f"Officer {id} not found")


@officer_router.delete(
    "/{id}",
    response_description="Delete an officer",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_officer(id: str):
    delete_result = await officer_collection.delete_one({"officer_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Officer {id} not found")