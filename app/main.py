
import matplotlib

import gradio as gr
import os

from src.run import pipeline
from src.enums import TypePrediction, Horizon
matplotlib.use("Agg")

def run(argv = None):
    
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7860))
    
    params_slider = {
        "minimum": 1,
        "maximum": 16,
        "step": 1
    }
    
    with gr.Blocks() as app:
        
        
        input_type = gr.components.Radio(
            choices = TypePrediction.choices(),
            value   = TypePrediction.default_choice(),
            type    = "value",
            label   = "Type of model prediction")
        
        horizon_type = gr.components.Radio(
            choices= Horizon.choices(),
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
        
        
        output_plot = gr.Plot()
        
        predict_region_btn.click(
            fn = pipeline,
            inputs = [input_origin, input_destiny, input_type, horizon_type],
            outputs = output_plot,
            api_name= "predict_region",
        )
    
    app.launch(
    server_name= "0.0.0.0", # for using on make up
    server_port=port,
    favicon_path= "favicon.ico",
    share=False)

if __name__ == "__main__":
    run()