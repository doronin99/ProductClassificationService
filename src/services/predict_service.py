import pickle
from typing import Any, Dict
from asyncio import Queue, create_task, gather, get_event_loop
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class PredictorService:
    def __init__(self):
        self.models = {}
        self.prediction_queue = Queue()
        self.executor = ThreadPoolExecutor()

    async def load_model_async(self, model_name: str, model_path: str):
        if model_name in self.models:
            return

        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
            self.models[model_name] = model

    async def predict_async(self, model_name: str, input_data: Dict[str, Any]):
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Load the model first.")

        model = self.models[model_name]

        df = pd.DataFrame([input_data])

        try:
            prediction = await self.run_in_threadpool(model.predict, df)
            return prediction.tolist()
        except Exception as e:
            raise ValueError(f"Error predicting with model '{model_name}': {str(e)}")

    async def get_prediction_result(self, prediction_task_id: int):
        task = await self.prediction_queue.get()
        await task  # Wait for the task to complete
        return task.result()  # Assuming the result is a list

    async def load_model(self, model_name: str, model_path: str):
        task = create_task(self.load_model_async(model_name, model_path))
        await task

    def predict(self, model_name: str, input_data: Dict[str, Any]):
        task = create_task(self.predict_async(model_name, input_data))
        self.prediction_queue.put_nowait(task)
        return task

    async def run_in_threadpool(self, func, *args, **kwargs):
        loop = get_event_loop()
        return await loop.run_in_executor(self.executor, lambda: func(*args, **kwargs))
