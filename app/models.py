from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self):
        self.setup()

    @abstractmethod
    def setup(self):
        """Set up the model, load weights, etc."""
        pass

    @abstractmethod
    def infer(self, text: str):
        """Perform inference on the input text."""
        pass


class DefaultModel(Model):
    
    def __init__(self):
        self.nlp = None
        self.setup()
    
    def setup(self):
        import spacy
        self.nlp = spacy.load("en_core_web_sm")

    def infer(self, input_text: str):
        # Perform NER prediction
        doc = self.nlp(input_text)
        prediction = [(entity.text, entity.label_) for entity in doc.ents]
        
        return prediction
