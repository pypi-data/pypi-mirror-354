import os
from dotenv import load_dotenv

load_dotenv()

class MovieConfig:
    """Classe de configuration contenant des arguments pour le client SDK.
    Contient la configuration de l'URL de base et du backoff progressif.
    """
    
    def __init__(
        self,
        movie_base_url: str = None,
        backoff: bool = True,
        backoff_max_time: int = 30,
    ):
        """Constructeur pour la classe de configuration.
        Args:
            movie_base_url (optional): L'URL de base pour les appels d'API.
            backoff: Réessayer les appels API en cas d'erreur.
            backoff_max_time: Durée max avant d’abandonner les tentatives.
        """
        self.movie_base_url = movie_base_url or os.getenv("MOVIE_API_BASE_URL")
        print(f"MOVIE_API_BASE_URL in MovieConfig init: {self.movie_base_url}") 
        if not self.movie_base_url:
            raise ValueError("L'URL de base est requise. Définissez la variable d'environnement MOVIE_API_BASE_URL.")
        self.movie_backoff = backoff
        self.movie_backoff_max_time = backoff_max_time

    def __str__(self):
        """Représentation de l'objet MovieConfig sous forme de chaîne"""
        return f"{self.movie_base_url} {self.movie_backoff} {self.movie_backoff_max_time}"
