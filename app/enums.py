from enum import Enum

class Sector(Enum):
    Region = "Region"
    Provincia = "Provincia"
    Comuna = "Comuna"
    
    @classmethod
    def choices(cls):
        return [x.value for x in cls]

class TypePrediction(Enum):
    Origin  = "Total Origin"
    Destiny = "Total Destiny"
    OriginDestiny = "Origin and Destiny"
    @classmethod
    def choices(cls):
        return [x.value for x in cls]
    
    @classmethod
    def from_value(cls, value: str):
        
        for type_prediction in TypePrediction:
            if value == type_prediction.value:
                return type_prediction
        raise ValueError("Bad value on Type Prediction enum")
    
    @classmethod
    def from_sectors(cls, origin, destiny):
        
        if origin is not None and destiny is not None:
            return TypePrediction.OriginDestiny
        
        if origin is None:
            return TypePrediction.Destiny
        
        if destiny is None:
            return TypePrediction.Origin
        
        raise ValueError("origin and destiny can't be both none")
