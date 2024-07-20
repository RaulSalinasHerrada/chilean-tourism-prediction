
import matplotlib

import gradio as gr
import os

from datamodel import DataTourism
from predict_model import Forecaster
from plotter import Plotter
from enums import TypePrediction, Horizon, Sector

matplotlib.use("nbAgg")

# matplotlib.use("Agg")

def pipeline(sector_origin: int,
    sector_destiny: int,
    input_type: str,
    horizon_type: str,
    
    ):
    
    sector_origin = int(sector_origin)
    sector_destiny = int(sector_destiny)
    sector = Sector.Region
    
    type_prediction = TypePrediction.from_value(input_type)
    type_horizon = Horizon.from_value(horizon_type)
    
    if type_prediction == TypePrediction.Origin:
        sector_destiny = None
    
    if type_prediction == TypePrediction.Destiny:
        sector_origin = None
    
    
    data_path = "./data/trips.csv"
    data_tourism = DataTourism.from_path(
        path = data_path,
        sector_origin = sector_origin,
        sector_destiny = sector_destiny)
    
    forecaster = Forecaster(
        data_tourism = data_tourism,
        h = type_horizon.value)
    
    plotter = Plotter(
        forecaster= forecaster,
        type_prediction= type_prediction,
        sector= sector,
        sector_destiny=sector_destiny,
        sector_origin=sector_origin)
    
    return plotter.create_plot()


def run(argv = None):
    
    params_slider = {
        "minimum": 1,
        "maximum": 16,
        "step": 1
    }
    
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7861))
    
    type_choices = TypePrediction.choices()
    horizon_choices = Horizon.choices()
    
    with gr.Blocks() as app:
        
        input_type = gr.components.Radio(
            choices = type_choices,
            value   = type_choices[-1],
            type    = "value",
            label   = "Type of model prediction")
        
        horizon_type = gr.components.Radio(
            choices= horizon_choices,
            value = Horizon.default_choice(),
            type = "value",
            label = "Forecast Horizon"
        )
        with gr.Tab("Region"):
            
            input_origin = gr.components.Slider(
                **params_slider, label = "Origin"
            )
            
            input_destiny = gr.components.Slider(
                **params_slider, label= "Destiny")
        
            predict_region_btn = gr.Button("Forecast")
        
        output_plot = gr.Plot(scale= 2)
        
        predict_region_btn.click(
            fn = pipeline,
            inputs = [input_origin, input_destiny, input_type, horizon_type],
            outputs = output_plot,
            api_name= "predict_region",
        )
    
    app.launch(
    server_name= "0.0.0.0", # for using on make up
    server_port=port,
    favicon_path= "./favicon.ico",
    share=False)

if __name__ == "__main__":
    run()