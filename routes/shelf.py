from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument
from models.shelf import ShelfModel, UpdateShelfModel, ShelfCollection
from app import shelf_collection

shelf_router = APIRouter(
    prefix="/shelves",
    tags=["Shelves"],
)


@shelf_router.post(
    "/",
    response_description="Add new shelf",
    response_model=ShelfModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_shelf(shelf: ShelfModel = Body(...)):
    """
    Insert a new shelf record.

    A unique `id` will be created and provided in the response.
    """
    new_shelf = await shelf_collection.insert_one(
        shelf.model_dump(by_alias=True, exclude=["id"])
    )
    created_shelf = await shelf_collection.find_one({"_id": new_shelf.inserted_id})
    return created_shelf


@shelf_router.get(
    "/",
    response_description="List all shelves",
    response_model=ShelfCollection,
    response_model_by_alias=False,
)
async def list_shelves():
    """
    List all of the shelf data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return ShelfCollection(shelves=await shelf_collection.find().to_list(1000))


@shelf_router.get(
    "/{id}",
    response_description="Get a single shelf",
    response_model=ShelfModel,
    response_model_by_alias=False,
)
async def show_shelf(id: str):
    """
    Get the record for a specific shelf, looked up by `id`.
    """
    if (shelf := await shelf_collection.find_one({"_id": ObjectId(id)})) is not None:
        return shelf

    raise HTTPException(status_code=404, detail=f"Shelf {id} not found")


@shelf_router.put(
    "/{id}",
    response_description="Update a shelf",
    response_model=ShelfModel,
    response_model_by_alias=False,
)
async def update_shelf(id: str, shelf: UpdateShelfModel = Body(...)):
    """
    Update individual fields of an existing shelf record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    shelf = {k: v for k, v in shelf.model_dump(by_alias=True).items() if v is not None}

    if len(shelf) >= 1:
        update_result = await shelf_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": shelf},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Shelf {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_shelf := await shelf_collection.find_one({"_id": id})) is not None:
        return existing_shelf

    raise HTTPException(status_code=404, detail=f"Shelf {id} not found")


@shelf_router.delete("/{id}", response_description="Delete a shelf")
async def delete_shelf(id: str):
    """
    Remove a single shelf record from the database.
    """
    delete_result = await shelf_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Shelf {id} not found")
