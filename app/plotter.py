from enums import TypePrediction
from predict_model import Forecaster
import pandas as pd
from sktime.utils.plotting import plot_series
from matplotlib.figure import Figure
from dataclasses import dataclass

@dataclass
class Plotter(object):
    forecaster: Forecaster
    type_prediction: TypePrediction

    sector_destiny: int | None
    sector_origin: int | None
    
    @property
    def is_multi(self):
        return self.sector_destiny is not None and self.sector_origin is not None
    
    @property
    def training_series(self):
        return self.forecaster.training_series
    
    @property
    def forecast_series(self):
        return self.forecaster.forecast_series
    
    def create_plot(self) -> Figure:
        
        # x = self.to_series_plot(self.data_agg)
        # y = self.to_series_plot(self.pred)
        
        x = self.training_series
        y = self.forecast_series
        
        type_prediction = self.type_prediction
        sector_destiny = self.sector_destiny
        sector_origin = self.sector_origin
        
        if type_prediction == TypePrediction.Destiny:
            
            title = "Total monthly touristic travels to region {}".format(sector_destiny)
        
        if type_prediction == TypePrediction.Origin:
            title = "Total monthly touristic travels from region {}".format(sector_origin)
        
        elif type_prediction == TypePrediction.OriginDestiny:
            
            title = "Monthly touristic travels from region {} to region {}".format(
                sector_origin, sector_destiny)
            
        fig, _ = plot_series(x,y,labels=["value", "forecast"],title=title)
        
        return fig
    
    # def to_series_plot(self,
    #     data: pd.DataFrame,
    #     ) -> pd.DataFrame:
        
    #     type_prediction = self.type_prediction
    #     sector_destiny = self.sector_destiny
    #     sector_origin = self.sector_origin
        
    #     df = data.reset_index().copy()
    #     if type_prediction == TypePrediction.Destiny.value:
    #         qry = "sector_destiny == {}".format(sector_destiny)
        
    #     elif type_prediction == TypePrediction.Origin.value:
    #         qry = "sector_origin == {}".format(sector_origin)
        
    #     else:
    #         qry  = "sector_origin == {} & sector_destiny == {}".format(sector_origin, sector_destiny)
        
    #     if not self.is_multi:
    #         df.query(qry, inplace=True)
        
    #     else:
    #         df = df[(df.iloc[:, 0] == sector_origin) & (df.iloc[:, 1] == sector_destiny)]
        
    #     if type_prediction == TypePrediction.Origin.value:
    #         df = df.groupby(["sector_origin", "time_stamp"]).sum(numeric_only= True).reset_index()
        
    #     elif type_prediction == TypePrediction.Destiny.value:
    #         df = df.groupby(["sector_destiny", "time_stamp"]).sum(numeric_only=True).reset_index()
        
    #     drop_cols = ["sector_origin", "sector_destiny"]
        
    #     if self.is_multi:
    #         drop_cols = [(x, "", "") for x in drop_cols]
        
    #     return df.drop(columns=drop_cols).set_index("time_stamp").squeeze()        
        
    

