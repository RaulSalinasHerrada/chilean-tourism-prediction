from datamodel import DataTourism

from dataclasses import dataclass, field
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.base import ForecastingHorizon
from sktime.exceptions import NotFittedError
from pandas import DataFrame, Series
from numpy import arange

from typing import Self

@dataclass
class Forecaster(object):
    
    data_tourism: DataTourism
    h: int = field(default=12)
    prd: int = field(default=24)
    
    training_data: Series = field(init=False)
    forecaster: ThetaForecaster = field(init=False)
    forecast_data: DataFrame = field(init=False)
    
    
    def __post_init__(self):
        
        self.training_data = self._filter_old(self.data_tourism.data)
        self.forecaster = self._fit_forecaster(self.training_data)
        self.forecast_data = self.forecast
    
    @property
    def sector(self):
        return self.data_tourism.sector
    
    @property
    def horizon(self):
        
        # cutoff = self.training_data.index[-1]
        fh = ForecastingHorizon(arange(1,self.h),  is_relative= True)
        # fh.to_absolute(cutoff)
        return fh
    
    @property
    def forecast(self):        
        if self.forecaster.is_fitted:    
            return self.forecaster.predict()
        
        raise NotFittedError("Model has not been fitted")
    
    def _filter_old(self, training_data: Series):

        training_data.sort_index(inplace=True)
        
        
        
        return training_data
    
    def _fit_forecaster(self, training_data: Series) -> ThetaForecaster:
        
        vals = training_data.values
        print(vals)
        forecaster = ThetaForecaster(sp=self.h).fit(vals, self.horizon)
        return forecaster
    
    @classmethod
    def load(cls, path: str) -> Self:
        raise NotImplementedError("not able to load from path")
