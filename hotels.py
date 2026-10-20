from fastapi import Query, APIRouter, Body

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Paris", "name": "paris"},
    {"id": 2, "title": "Amsterdam", "name": "amsterdam"},
    {"id": 3, "title": "Barcelona", "name": "Barcelona"},
    {"id": 4, "title": "Berlin", "name": "Berlin"},
    {"id": 5, "title": "Kyiv", "name": "kyiv"},
    {"id": 6, "title": "Warszawa", "name": "warszawa"},
    {"id": 7, "title": "Rome", "name": "rome"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="IDs"),
        title: str | None = Query(None, description="Hotel name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Paris",
        "value": {
            "title": "5-star Paris hotel",
            "name": "paris-5-star",
        }
    },
    "2": {
        "summary": "Dubai",
        "value": {
            "title": "Dubai hotel near fountain",
            "name": "dubai_fountain",
        }
    }
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial data update about hotel",
    description="<h1>Here we partially update the data about the hotel: you can send name, or title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
