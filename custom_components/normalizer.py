import re
import unicodedata
from typing import Any, Dict, List, Text, Optional

# Importaciones actualizadas para Rasa 3.x
from rasa.engine.graph.component import Component
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.featurizers.featurizer import Featurizer


class SpanishTextNormalizer(Component):
    """Componente personalizado para normalizar texto en español."""
    
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: Dict[Text, Any],
    ) -> "SpanishTextNormalizer":
        return cls(config)
        
    def __init__(self, config: Optional[Dict[Text, Any]] = None) -> None:
        """Inicializa el normalizador."""
        self.config = config if config else {}
        
    def train(self, training_data: TrainingData) -> Resource:
        """Normaliza los ejemplos de entrenamiento."""
        for example in training_data.training_examples:
            if example.get("text"):
                example.set("text", self._normalize_text(example.get("text")))
        
        return self._resource
                
    def process(self, messages: List[Message]) -> List[Message]:
        """Normaliza el texto de entrada."""
        for message in messages:
            if message.get("text"):
                message.set("text", self._normalize_text(message.get("text")))
        
        return messages
        
    @staticmethod
    def _normalize_text(text: Text) -> Text:
        """
        Normaliza el texto:
        - Convierte a minúsculas
        - Elimina acentos y caracteres especiales
        - Elimina signos de puntuación
        - Normaliza espacios
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar acentos
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                      if unicodedata.category(c) != 'Mn')
        
        # Eliminar signos de puntuación conservando solo lo necesario
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Normalizar espacios (convertir múltiples espacios en uno solo)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text