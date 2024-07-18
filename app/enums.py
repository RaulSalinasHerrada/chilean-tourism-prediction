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

