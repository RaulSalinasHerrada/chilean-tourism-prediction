import matplotlib

from .datamodel import DataTourism
from .predict_model import Forecaster
from .plotter import Plotter
from .enums import TypePrediction, Horizon, Sector
import os 

matplotlib.use("Agg")

def pipeline(sector_origin: int,
    sector_destiny: int,
    input_type: str,
    horizon_type: str,
    ):
    
    sector_origin = int(sector_origin)
    sector_destiny = int(sector_destiny)
    sector = Sector.Region
    
    type_prediction = TypePrediction.from_value(input_type)
    type_horizon = Horizon.from_value(horizon_type)
    
    if type_prediction == TypePrediction.Origin:
        sector_destiny = None
    
    if type_prediction == TypePrediction.Destiny:
        sector_origin = None
    
    data_path = os.environ.get(
        "DATA_PATH", "./data/trips.parquet")
    
    data_tourism = DataTourism.from_path(
        path = data_path,
        sector_origin = sector_origin,
        sector_destiny = sector_destiny)
    
    forecaster = Forecaster(
        data_tourism = data_tourism,
        h = type_horizon.value)
    
    plotter = Plotter(
        forecaster= forecaster,
        type_prediction= type_prediction,
        sector= sector,
        sector_destiny=sector_destiny,
        sector_origin=sector_origin)
    
    return plotter.create_plot()