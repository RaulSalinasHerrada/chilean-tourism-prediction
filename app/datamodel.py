
from dataclasses import dataclass, field
from pandas import DataFrame
from typing import Self
import pandas as pd
import numpy as np
from enums import Sector

@dataclass
class DataTourism(object):
    
    data: DataFrame
    sector: Sector = field(default= Sector.Region)
    
    def __post_init__(self):
        self.data = self._preprocess_data(self.data)
    
    @classmethod
    def from_path(cls, path: str, sector = Sector.Region) -> Self:
        
        data = cls._load_data(path)
        return cls(data=data, sector = sector)
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
        sector: Sector = Sector.Region) -> pd.DataFrame:
    
        data.columns = [x.strip() for x in data.columns]
        
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
            to_date_row,axis = 1)
        
        unused_date_cols = ["Anio", "month_name", "month_value"]
        
        data_long.drop(columns= unused_date_cols, inplace=True)
        
        sector_name = sector.name
        
        cut_sector = ["CUT {} Origen", "CUT {} Destino"]
        
        col_sector = [x.format(sector_name) for x in cut_sector]
        kv = ["time_stamp", "value"]
        
        cols = col_sector.copy()
        
        for lcol in kv:
            cols.append(lcol)
        
        data_sector = data_long[cols].copy()
        
        col_sector.append("time_stamp")
        data_agg = data_sector.groupby(by = col_sector).sum()
        data_agg.value = np.int32(data_agg.value.values)
        data_agg.query("value > 0", inplace = True)
        
        data_agg.reset_index(inplace=True)
        data_agg.set_index("time_stamp", inplace=True)
        data_agg = data_agg.to_period("M")
        
        renamer = {
        data_agg.columns[0]: "sector_origin",
        data_agg.columns[1]: "sector_destiny",

        }
        
        data_agg.rename(columns=renamer, inplace=True)
        data_agg.reset_index(inplace=True)
        
        cols_index = ["sector_origin", "sector_destiny", "time_stamp"]
        
        data_agg.set_index(cols_index, inplace=True)
        
        return data_agg

