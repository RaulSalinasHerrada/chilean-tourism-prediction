from src.enums import TypePrediction, Sector
from src.predict_model import Forecaster
from sktime.utils.plotting import plot_series
from matplotlib.figure import Figure
from dataclasses import dataclass

@dataclass
class Plotter(object):
    forecaster: Forecaster
    type_prediction: TypePrediction
    sector: Sector
    sector_destiny: int | None
    sector_origin: int | None
    
    @property
    def is_multi(self):
        return self.sector_destiny is not None and self.sector_origin is not None
    
    @property
    def training_series(self):
        return self.forecaster.training_series
    
    @property
    def forecast_series_interval(self):
        return self.forecast_series_interval
    
    @property
    def forecast_series(self):
        return self.forecaster.forecast_series
    
    def create_plot(self) -> Figure:
        
        
        x = self.training_series
        y = self.forecast_series
        
        type_prediction = self.type_prediction
        sector_destiny = self.sector_destiny
        sector_origin = self.sector_origin
        sector_type = self.sector.value
        
        
        if type_prediction == TypePrediction.Destiny:
            
            title = f"Total monthly touristic travels to {sector_type} {sector_destiny}"
        
        if type_prediction == TypePrediction.Origin:
            title = f"Total monthly touristic travels from {sector_type} {sector_origin}"
        
        elif type_prediction == TypePrediction.OriginDestiny:
            
            title = f"Monthly touristic travels from {sector_type} {sector_origin} to {sector_type} {sector_destiny}".format(
                sector_origin, sector_destiny)
            
        fig, _ = plot_series(x,y,labels=["value", "forecast"],title=title,)
        
        return fig

