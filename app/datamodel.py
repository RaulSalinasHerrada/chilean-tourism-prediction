
from dataclasses import dataclass, field
from pandas import DataFrame
from typing import Self
import pandas as pd
import numpy as np
from enums import Sector, TypePrediction

@dataclass
class DataTourism(object):
    
    data: DataFrame
    sector_origin: int | None
    sector_destiny: int | None
    sector: Sector = field(default= Sector.Region)
    
    def __post_init__(self):
        self.data = self._preprocess_data(
            self.data, self.sector_origin, self.sector_destiny)
    
    @classmethod
    def from_path(
        cls: Self, path: str,
        sector_origin: int | None,
        sector_destiny: int | None,
        sector = Sector.Region,
        ) -> Self:
        
        data = cls._load_data(path)
        
        return cls(
            data=data,
            sector_origin = sector_origin,
            sector_destiny = sector_destiny,
            sector = sector)
        
    @staticmethod
    def _load_data(path) -> DataFrame:

        read_params = {
            "encoding": "latin_1",
            "sep": ";",
            "decimal": ","
        }
        return pd.read_csv(path, **read_params)
    
    @staticmethod
    def _to_date(month: int,year:int):
        return pd.Timestamp(day=1, month=month, year = year)
    
    @classmethod
    def _preprocess_data(
        cls, 
        data: pd.DataFrame,
        sector_origin: int  | None ,
        sector_destiny: int | None,
        sector: Sector = Sector.Region,
        ) -> pd.DataFrame:

        type_prediction = TypePrediction.from_sectors(
            sector_origin, sector_destiny)
        
        data.columns = [x.strip() for x in data.columns]
        sector_name = sector.name
        
        col_sector = [x for x in data.columns if f"CUT {sector_name}" in x] 
        
        
        renamer = {
        col_sector[0]: "sector_origin",
        col_sector[1]: "sector_destiny",
        }


        data.rename(columns=renamer, inplace=True)
        
        slice_query: str
        
        if type_prediction == TypePrediction.Destiny.value:
            slice_query = "sector_destiny == {}".format(sector_destiny)
        
        elif type_prediction == TypePrediction.Origin.value:
            slice_query = "sector_origin == {}".format(sector_origin)
        
        else:
            slice_query  = "sector_origin == {} & sector_destiny == {}".format(sector_origin, sector_destiny)        
        
        data.query(slice_query, inplace=True)

        
        col_melt = list(data.columns[-12:]) #months as cols
        col_maintain = list(data.columns[:-12])
        
        mn = "month_name"
        m_val = "month_value"
        code_month = pd.DataFrame.from_dict(
            data={
                mn: col_melt,
                m_val: list(range(1,13))}) # 12 months
        
        data_long = data.melt(
            id_vars=col_maintain,
            value_vars=col_melt,
            var_name=mn).merge(
                code_month,
                how="left",
                on=mn)
        
        def to_date_row(row):
            month = row[m_val]
            year = row["Anio"]
            return cls._to_date(month, year)

        
        
        data_long["time_stamp"] = data_long.apply(
            to_date_row, axis = 1)
        
        unused_date_cols = ["Anio", "month_name", "month_value"]
        
        data_long.drop(columns= unused_date_cols, inplace=True)
                
        time_value = ["time_stamp", "value"]
        
        
        cols = ["sector_origin", "sector_destiny"]
        cols.extend(time_value)
        
        data_sector = data_long[cols].copy()
        
        
        
        data_agg = data_sector.groupby(by = "time_stamp").sum()
        
        data_agg.value = np.int32(data_agg.value.values)
        data_agg.reset_index(inplace=True)
        
        data_agg.query("value > 0", inplace=True)
        data_agg.set_index("time_stamp", inplace=True)
        data_agg = data_agg.to_period("M")
        
        print("time series", data_agg["value"].to_string())
        
        return data_agg["value"]

