from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.services.predict_service import PredictorService

router = APIRouter(
    prefix="/predictor",
    tags=["predictor"],
)
predictor_service = PredictorService()


@router.post("/predict/{model_name}",
             response_model=Dict[str, Any],
             summary="Make Prediction",
             description="Make a prediction using the specified model.")
async def make_prediction(
    model_name: str,
    input_data: Dict[str, Any],
    service: PredictorService = Depends()
):
    """
    Make a prediction using the specified model.

    Args:
        model_name (str): The name of the model to use for prediction.
        input_data (Dict[str, Any]): Input data for making a prediction.
        service (PredictorService): Predictor service.

    Returns:
        Dict[str, Any]: Result of the prediction task.
    """
    try:
        if model_name not in service.models:
            await service.load_model(model_name, f"models/{model_name}_model.pkl")

        prediction_task = service.predict(model_name, input_data)
        return {"prediction_task_id": id(prediction_task), "message": "Prediction task created successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/prediction/{prediction_task_id}",
            response_model=Dict[str, Any],
            summary="Get Prediction Result",
            description="Get the result of a previously made prediction.")
async def get_prediction_result(
    prediction_task_id: int,
    service: PredictorService = Depends()
):
    """
    Get the result of a previously made prediction.

    Args:
        prediction_task_id (int): The ID of the prediction task.
        service (PredictorService): Predictor service.

    Returns:
        Dict[str, Any]: Result of the prediction.
    """
    try:
        result = await service.get_prediction_result(prediction_task_id)
        return {"prediction_result": result, "message": "Prediction result retrieved successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
