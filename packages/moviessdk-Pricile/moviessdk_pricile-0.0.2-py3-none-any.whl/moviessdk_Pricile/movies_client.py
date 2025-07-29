import httpx
import requests
from typing import Optional, List
from .schemas import MovieSimple, MovieDetailed, RatingSimple, TagSimple, LinkSimple, AnalyticsResponse
from .movies_config import MovieConfig
class MovieClient:
	def __init__(self, config: Optional[MovieConfig] = None):
		self.config = config or MovieConfig()
		self.movie_base_url = self.config.movie_base_url

	def health_check(self) -> dict:
		url = f"{self.movie_base_url}/"
		response = httpx.get(url)
		response.raise_for_status()
		return response.json()

	def get_movie(self, movie_id: int) -> MovieDetailed:
		url = f"{self.movie_base_url}/movies/{movie_id}"
		response = httpx.get(url)
		response.raise_for_status()
		return MovieDetailed(**response.json())

	def list_movies(self, limit: int = 10, output_format: str = "pydantic"):
		response = requests.get(f"{self.config.movie_base_url}/movies?limit={limit}")
		response.raise_for_status()
		data = response.json()

		movies = [MovieSimple(**item) for item in data]

		if output_format == "dict":
			return [m.model_dump() for m in movies]  # ou `dict(m)` si Pydantic v1
		elif output_format == "pandas":
			import pandas as pd
			return pd.DataFrame([m.model_dump() for m in movies])
		else:
			return movies  # liste d'objets Pydantic


	def get_rating(self, user_id: int, movie_id: int) -> RatingSimple:
		url = f"{self.movie_base_url}/ratings/{user_id}/{movie_id}"
		response = httpx.get(url)
		response.raise_for_status()
		return RatingSimple(**response.json())

	def list_ratings(self, skip: int = 0, limit: int = 100, movie_id: Optional[int] = None, user_id: Optional[int] = None, min_rating: Optional[float] = None) -> List[RatingSimple]:
		url = f"{self.movie_base_url}/ratings"
		params = {"skip": skip, "limit": limit}
		if movie_id:
			params["movie_id"] = movie_id
		if user_id:
			params["user_id"] = user_id
		if min_rating:
			params["min_rating"] = min_rating
		response = httpx.get(url, params=params)
		response.raise_for_status()
		return [RatingSimple(**rating) for rating in response.json()]

	def get_tag(self, user_id: int, movie_id: int, tag_text: str) -> TagSimple:
		url = f"{self.movie_base_url}/tags/{user_id}/{movie_id}/{tag_text}"
		response = httpx.get(url)
		response.raise_for_status()
		return TagSimple(**response.json())

	def list_tags(self, skip: int = 0, limit: int = 100, movie_id: Optional[int] = None, user_id: Optional[int] = None) -> List[TagSimple]:
		url = f"{self.movie_base_url}/tags"
		params = {"skip": skip, "limit": limit}
		if movie_id:
			params["movie_id"] = movie_id
		if user_id:
			params["user_id"] = user_id
		response = httpx.get(url, params=params)
		response.raise_for_status()
		return [TagSimple(**tag) for tag in response.json()]

	def get_link(self, movie_id: int) -> LinkSimple:
		url = f"{self.movie_base_url}/links/{movie_id}"
		response = httpx.get(url)
		response.raise_for_status()
		return LinkSimple(**response.json())

	def list_links(self, skip: int = 0, limit: int = 100) -> List[LinkSimple]:
		url = f"{self.movie_base_url}/links"
		params = {"skip": skip, "limit": limit}
		response = httpx.get(url, params=params)
		response.raise_for_status()
		return [LinkSimple(**link) for link in response.json()]

	def get_analytics(self) -> AnalyticsResponse:
		url = f"{self.movie_base_url}/analytics"
		response = httpx.get(url)
		response.raise_for_status()
		return AnalyticsResponse(**response.json())