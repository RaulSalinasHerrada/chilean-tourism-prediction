from enum import Enum

class Sector(Enum):
    Region = "Region"
    Province = "Province"
    Commune = "Commune"
    
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

class Horizon(Enum):
    Months3 = 3
    Months6 = 6
    Months9 = 9
    Months12 = 12

    def to_str(self):
        return f"{self.value} months"
    
    @classmethod
    def choices(cls):
        return [ x.to_str() for x in cls]
        
    @classmethod
    def default_choice(cls):
        return cls.Months6.to_str()
    
    @classmethod
    def from_value(cls, value: str):
            
        for type_prediction in cls:
            if value == type_prediction.to_str():
                return type_prediction
            
        raise ValueError("Bad value on Horizon enum")
    