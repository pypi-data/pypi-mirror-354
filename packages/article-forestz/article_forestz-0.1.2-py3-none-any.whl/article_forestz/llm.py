from llmada import BianXieAdapter
import json

class MyLocalLLMClient():
    
    def __init__(self,model_name:str):
        self.bx = BianXieAdapter()
        self.bx.set_model(model_name)
    
    def generate_response(self,text):
        return self.bx.product(text)