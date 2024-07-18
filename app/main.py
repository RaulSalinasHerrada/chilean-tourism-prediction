
import matplotlib

import gradio as gr
import os

from datamodel import DataTourism
from predict_model import Forecaster
from plotter import Plotter
from enums import TypePrediction

matplotlib.use("Agg")

def pipeline(sector_origin: int,
    sector_destiny: int,
    input_type: str
    ):
    
    type_prediction = TypePrediction.from_value(input_type)
    
    if type_prediction == TypePrediction.Origin:
        sector_destiny = None
    
    if type_prediction == TypePrediction.Destiny:
        sector_origin = None
    
    
    data_path = "./data/trips.csv"
    data_tourism = DataTourism.from_path(data_path)
    forecaster = Forecaster(data_tourism = data_tourism)
    plotter = Plotter(forecaster, sector_destiny, sector_origin)
    
    return plotter.create_plot()


def run(argv = None):
    
    params_slider = {
        "minimum": 1,
        "maximum": 16,
        "step": 1
    }
    
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7860))
    
    type_choices = TypePrediction.choices()
    
    with gr.Blocks() as app:
        
        input_type = gr.components.Radio(
            choices = type_choices,
            value   = type_choices[-1],
            type    = "value",
            label   = "Prediction Aggregation")
        
        with gr.Tab("Region"):
            
            input_origin = gr.components.Slider(
                **params_slider, label = "Origin"
            )
            
            input_destiny = gr.components.Slider(
                **params_slider, label= "Destiny")
        
            predict_region_btn = gr.Button("Forecast")
        
        output_plot = gr.Plot()
        
        predict_region_btn.click(
            fn = pipeline,
            inputs = [input_origin, input_destiny, input_type],
            outputs = output_plot,
            api_name= "predict_region",
        )
    
    app.launch(
    server_name= "0.0.0.0", # for using on make up
    server_port=port,
    share=False)

if __name__ == "__main__":
    run()