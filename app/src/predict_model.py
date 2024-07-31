from src.datamodel import DataTourism

from dataclasses import dataclass, field
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.base import ForecastingHorizon
from pandas import DataFrame, Series
from numpy import arange


@dataclass
class Forecaster(object):
    
    data_tourism: DataTourism
    h: int
    
    forecast_series: Series = field(init=False)
    forecast_series_interval: DataFrame = field(init=False)
    forecaster: ThetaForecaster = field(init=False)
    
    
    def __post_init__(self):
        
        self.forecaster = self._fit_forecaster(self.training_series)
        self.forecast_series = self.predict()
        self.forecast_series_interval = self.predict_interval()
    
    @property
    def sector(self):
        return self.data_tourism.sector
    
    @property
    def training_series(self):
        return self.data_tourism.training_data
        
    @property
    def horizon(self):
        return ForecastingHorizon(arange(1,self.h + 1),  is_relative= True)
    
    def predict(self):        
        
        self.forecaster.check_is_fitted()
        return self.forecaster.predict()
    
    def predict_interval(self)-> DataFrame:
        
        self.forecaster.check_is_fitted()
        return self.forecaster.predict_interval()

    def _fit_forecaster(self, training_data: Series) -> ThetaForecaster:
        
        forecaster = ThetaForecaster(
            sp=self.h).fit(
                y = training_data,
                fh = self.horizon)
        return forecaster
    