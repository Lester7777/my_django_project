"""
WSGI config for item project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'item.settings')

application = get_wsgi_application()

# ML registry
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.tourism_classifier.random_forest import TourismRandomForestClassifier

try:
    registry = MLRegistry()  # create ML registry
    # Random Forest classifier for tourism
    trf = TourismRandomForestClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="tourism_classifier",
                            algorithm_object=trf,
                            algorithm_name="random forest",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="User",
                            algorithm_description="Random Forest for tourism destination prediction",
                            algorithm_code=inspect.getsource(TourismRandomForestClassifier))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
