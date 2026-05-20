import joblib
import pandas as pd
import os


class TourismRandomForestClassifier:
    def __init__(self):
        # Get the path to the research directory
        # Go up from backend/item/apps/ml/tourism_classifier/ to my_django_project/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_artifacts = os.path.join(current_dir, "..", "..", "..", "..", "..", "research")
        path_to_artifacts = os.path.normpath(path_to_artifacts)
        
        self.activity_encoder = joblib.load(os.path.join(path_to_artifacts, "activity_encoder.pkl"))
        self.destination_encoder = joblib.load(os.path.join(path_to_artifacts, "destination_encoder.pkl"))
        self.model = joblib.load(os.path.join(path_to_artifacts, "tourism_model.pkl"))

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(input_data, index=[0])
        # Convert categorical preferred_activity
        input_data["preferred_activity"] = self.activity_encoder.transform(input_data["preferred_activity"])
        return input_data

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, input_data):
        # Decode the predicted destination
        destination = self.destination_encoder.inverse_transform(input_data)[0]
        return {"destination": destination, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
