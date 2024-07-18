from datamodel import DataTourism

from dataclasses import dataclass, field
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.base import ForecastingHorizon
from sktime.exceptions import NotFittedError
from pandas import DataFrame
from numpy import arange

from typing import Self

@dataclass
class Forecaster(object):
    
    data_tourism: DataTourism
    h: int = field(default=12)
    prd: int = field(default=24)
    
    training_data: DataFrame = field(init=False)
    forecast_data: DataFrame = field(init=False)
    forecaster: ThetaForecaster = field(init=False)
    
    
    def __post_init__(self):
        
        self.training_data = self._flatten_data(self.data_tourism.data)
        self.forecaster = self._fit_forecaster(self.training_data)
        self.forecast_data = self.forecaster.predict()
    
    @property
    def sector(self):
        return self.data_tourism.sector
    
    @property
    def horizon(self):
        return ForecastingHorizon(arange(1,self.h),  is_relative= True)

    @property
    def forecast(self):        
        if self.forecaster.is_fitted:    
            return self.forecaster.predict()
        
        raise NotFittedError("Model has not been fitted")
    
    def _flatten_data(self, data_agg: DataFrame):
        cols_index = ["sector_origin", "sector_destiny", "time_stamp"]
        prd = self.prd
        
        data_flat = data_agg.reset_index().copy()
        periods = data_flat["time_stamp"].unique()
        last_2years = periods[-prd:]
        data_flat = data_flat[data_flat["time_stamp"].isin(last_2years)]
        data_flat.set_index(cols_index, inplace=True)
        
        return data_flat
    
    def _fit_forecaster(self, data_flat: DataFrame) -> ThetaForecaster:
        forecaster = ThetaForecaster(sp=self.h).fit(data_flat, self.horizon)
        return forecaster
    
    
    @classmethod
    def load(cls, path: str) -> Self:
        raise NotImplementedError("not able to load from path")
