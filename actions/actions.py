from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ActionBusquedaConocimiento(Action):
    def __init__(self):
        # Cargar el modelo de embeddings multilingual
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Cargar la base de conocimiento desde JSON
        with open('D:/ProyectoEstudiantes/Asistente/knowledge/base_conocimiento_oohel.json', 'r', encoding='utf-8') as f:
            self.conocimiento = json.load(f)  
        
        # Preparar las preguntas y generar embeddings
        self.preguntas = [item['pregunta'] for item in self.conocimiento]
        self.respuestas = [item['respuesta'] for item in self.conocimiento]
        
        # Generar embeddings para todas las preguntas
        self.embeddings = self.model.encode(self.preguntas)
    
    def name(self) -> Text:
        return "action_busqueda_conocimiento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener la consulta del usuario
        consulta = tracker.latest_message.get('text')
        
        # Generar embedding para la consulta
        consulta_embedding = self.model.encode([consulta])
        
        # Calcular similitud con todas las preguntas
        similarities = cosine_similarity(consulta_embedding, self.embeddings)[0]
        
        # Encontrar la pregunta más similar
        max_idx = np.argmax(similarities)
        max_similarity = similarities[max_idx]
        
        # Si la similitud supera el umbral, devolver la respuesta correspondiente
        if max_similarity > 0.5:
            respuesta = self.respuestas[max_idx]
            dispatcher.utter_message(text=respuesta)
        else:
            dispatcher.utter_message(text="Lo siento, no tengo información específica sobre eso. ¿Puedes reformular la pregunta?")
        
        return []