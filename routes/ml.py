
from fastapi import APIRouter, File
from starlette.responses import Response
import io
from PIL import Image
import json

from ml.segmentation import get_yolov5, get_image_from_bytes

ml_router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

# model = get_yolov5()

@ml_router.post("/object-to-json")
async def detect_hkd_return_json_result(file: bytes = File(...)):
    input_image = get_image_from_bytes(file)
    # results = model(input_image)
    # detect_res = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    # detect_res = json.loads(detect_res)
    # return {"result": detect_res}


@ml_router.post("/object-to-img")
async def detect_hkd_return_base64_img(file: bytes = File(...)):
    input_image = get_image_from_bytes(file)
    # results = model(input_image)
    # results.render()  # updates results.imgs with boxes and labels
    # for img in results.imgs:
    #     bytes_io = io.BytesIO()
    #     img_base64 = Image.fromarray(img)
    #     img_base64.save(bytes_io, format="jpeg")
    # return Response(content=bytes_io.getvalue(), media_type="image/jpeg")
