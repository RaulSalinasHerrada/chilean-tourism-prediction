
from dataclasses import dataclass, field
from pandas import DataFrame, Series
from typing import Self
import pandas as pd
from src.enums import Sector, TypePrediction

@dataclass
class DataTourism(object):
    
    data: DataFrame
    sector_origin: int | None
    sector_destiny: int | None
    sector: Sector = field(default= Sector.Region)
    training_data: Series = field(init=False)
    
    def __post_init__(self):
        self.training_data = self._preprocess_data(
            self.data, self.sector_origin, self.sector_destiny, self.sector )
    
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
        return pd.read_parquet(path)
    
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
        ) -> Series:

        type_prediction = TypePrediction.from_sectors(
            sector_origin, sector_destiny)
        
        data.columns = [x.strip() for x in data.columns]
        
        sector_name = sector.name
        
        col_sector = [x for x in data.columns if f"CUT {sector_name}" in x] 
        
        origin_name = "sector_origin"
        destiny_name = "sector_destiny"
        
        renamer = {
        col_sector[0]: origin_name,
        col_sector[1]: destiny_name,
        }


        data.rename(columns=renamer, inplace=True)
        
        qry_destiny = f"{destiny_name} == {sector_destiny}"
        qry_origin = f"{origin_name} == {sector_origin}"
        
        query_mapper = {
            TypePrediction.Destiny: qry_destiny,
            TypePrediction.Origin: qry_origin,
            TypePrediction.OriginDestiny: " & ".join([qry_origin, qry_destiny])
        }
        
        slice_query = query_mapper[type_prediction]
        
        data.query(slice_query, inplace=True)
        
        col_melt = list(data.columns[-12:]) #months as cols
        col_maintain = data.columns[:-12]
        
        
        year = "Anio"
        month = "month"
        ts = "time_stamp"
        value = "value"
        
        data = data.melt(
            id_vars=col_maintain,
            value_vars= col_melt,
            var_name= month,
        )
        
        month_replacer = {month: {k: v for (k,v) in zip(col_melt, range(1, 13) )}
        }
        
        data.replace(month_replacer,inplace=True)
        
        data[ts] = data.apply(lambda row: cls._to_date(row[month], row[year]), axis= 1)
        
        col_interest = [ts, value]
        
        data = data[col_interest].groupby(
            ts).sum(
                min_count=1).reset_index().set_index(ts)
        
        data.dropna(inplace=True)
        data = data.to_period("M")
        
        return data[value]