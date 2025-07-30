"""
nullbr-python: Python SDK for Nullbr API

A Python SDK for accessing the Nullbr API to search and retrieve information
about movies, TV shows, collections, and their resources.
"""

__version__ = "0.1.1"
__author__ = "nullbr-python"
__license__ = "MIT"

import httpx

from .models.base import MediaItem
from .models.collection import Collection115Response, CollectionResponse
from .models.movie import (
    Movie115Item,
    Movie115Response,
    MovieEd2kItem,
    MovieEd2kResponse,
    MovieMagnetItem,
    MovieMagnetResponse,
    MovieResponse,
)
from .models.search import ListResponse, SearchResponse
from .models.tv import (
    TV115Response,
    TVResponse,
    TVSeasonMagnetResponse,
    TVSeasonResponse,
)

# 导出主要的类和函数
__all__ = [
    "NullbrSDK",
    "MediaItem",
    "SearchResponse",
    "ListResponse",
    "MovieResponse",
    "Movie115Response",
    "MovieMagnetResponse",
    "MovieEd2kResponse",
    "TVResponse",
    "TV115Response",
    "TVSeasonResponse",
    "TVSeasonMagnetResponse",
    "CollectionResponse",
    "Collection115Response",
]


class NullbrSDK:
    def __init__(
        self,
        app_id: str,
        api_key: str = None,
        base_url: str = "https://api.nullbr.eu.org",
    ):
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = httpx.Client()
        self.session.headers.update({"X-APP-ID": app_id})
        if api_key:
            self.session.headers.update({"X-API-KEY": api_key})

    def _request(self, method: str, url: str, params: dict = None) -> dict:
        """
        统一的API请求方法，包含日志记录

        Args:
            method: HTTP方法 (GET/POST等)
            url: 请求URL
            params: 请求参数

        Returns:
            响应的JSON数据

        Raises:
            httpx.HTTPError: 当API返回非200状态码时
        """
        import logging

        logger = logging.getLogger(__name__)

        logger.info(f"Requesting {method} {url}")
        if params is not None:
            logger.debug(f"Request params: {params}")

        response = self.session.request(method, url, params=params)
        if not response.is_success:
            logger.error(f"API returned {response.status_code}")
            logger.error(f"Response data: {response.json()}")
            response.raise_for_status()
        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response data: {response.json()}")

        return response.json()

    def search(self, query: str, page: int = 1) -> SearchResponse:
        """搜索合集、电影、剧集、人物

        Args:
            query: 搜索关键词
            page: 页码，默认为1

        Returns:
            SearchResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request(
            "GET", f"{self.base_url}/search", {"query": query, "page": page}
        )

        items = [
            MediaItem(
                media_type=item["media_type"],
                tmdbid=item["tmdbid"],
                poster="https://image.tmdb.org/t/p/w154/" + item["poster"],
                title=item["title"],
                overview=item["overview"],
                vote_average=item.get("vote_average"),
                release_date=item.get("release_date"),
                rank=item.get("rank"),
            )
            for item in data["items"]
        ]

        return SearchResponse(
            page=data["page"],
            total_pages=data["total_pages"],
            total_results=data["total_results"],
            items=items,
        )

    def get_list(self, listid: int, page: int = 1) -> ListResponse:
        """获取列表详细信息

        Args:
            listid: 列表id
            page: 页码，默认为1

        Returns:
            ListResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request("GET", f"{self.base_url}/list/{listid}", {"page": page})

        items = [
            MediaItem(
                media_type=item["media_type"],
                tmdbid=item["tmdbid"],
                poster="https://image.tmdb.org/t/p/w154/" + item["poster"],
                title=item["title"],
                overview=item["overview"],
                vote_average=item.get("vote_average"),
                release_date=item.get("release_date"),
            )
            for item in data["items"]
        ]

        return ListResponse(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            updated_dt=data["updated_dt"],
            page=data["page"],
            total_page=data["total_page"],
            items=items,
        )

    def get_movie(self, tmdbid: int) -> MovieResponse:
        """获取电影详细信息

        Args:
            tmdbid: 电影的TMDB ID

        Returns:
            MovieResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request("GET", f"{self.base_url}/movie/{tmdbid}")

        return MovieResponse(
            id=data["id"],
            poster="https://image.tmdb.org/t/p/w154/" + data["poster"],
            title=data["title"],
            overview=data["overview"],
            vote=data["vote"],
            release_date=data["release_date"],
            has_115=bool(data["115-flg"]),
            has_magnet=bool(data["magnet-flg"]),
            has_ed2k=bool(data["ed2k-flg"]),
            has_video=bool(data["video-flg"]),
        )

    def get_movie_115(self, tmdbid: int, page: int = 1) -> Movie115Response:
        """获取电影网盘资源

        Args:
            tmdbid: 电影的TMDB ID
            page: 页码，默认为1

        Returns:
            Movie115Response 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        if not self.api_key:
            raise ValueError("API KEY is required for this operation")

        data = self._request(
            "GET", f"{self.base_url}/movie/{tmdbid}/115", {"page": page}
        )

        items = [
            Movie115Item(
                title=item["title"], size=item["size"], share_link=item["share_link"]
            )
            for item in data["115"]
        ]

        return Movie115Response(
            id=data["id"],
            media_type=data["media_type"],
            page=data["page"],
            total_page=data["total_page"],
            items=items,
        )

    def get_movie_magnet(self, tmdbid: int) -> MovieMagnetResponse:
        """获取电影磁力资源

        Args:
            tmdbid: 电影的TMDB ID

        Returns:
            MovieMagnetResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        data = self._request("GET", f"{self.base_url}/movie/{tmdbid}/magnet")

        items = [
            MovieMagnetItem(
                title=item["title"], size=item["size"], magnet=item["magnet"]
            )
            for item in data["magnet"]
        ]

        return MovieMagnetResponse(
            id=data["id"], media_type=data["media_type"], items=items
        )

    def get_movie_ed2k(self, tmdbid: int) -> MovieEd2kResponse:
        """获取电影电驴资源

        Args:
            tmdbid: 电影的TMDB ID

        Returns:
            MovieEd2kResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        data = self._request("GET", f"{self.base_url}/movie/{tmdbid}/ed2k")

        items = [
            MovieEd2kItem(title=item["title"], size=item["size"], ed2k=item["ed2k"])
            for item in data["ed2k"]
        ]

        return MovieEd2kResponse(
            id=data["id"], media_type=data["media_type"], items=items
        )

    def get_collection(self, tmdbid: int) -> CollectionResponse:
        """获取合集详细信息

        Args:
            tmdbid: 合集的TMDB ID

        Returns:
            CollectionResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request("GET", f"{self.base_url}/collection/{tmdbid}")

        return CollectionResponse(
            id=data["id"],
            name=data["name"],
            overview=data["overview"],
            poster="https://image.tmdb.org/t/p/w154/" + data["poster"],
            backdrop="https://image.tmdb.org/t/p/w300/" + data["backdrop"],
            has_115=bool(data["115-flg"]),
        )

    def get_tv(self, tmdbid: int) -> TVResponse:
        """获取剧集详细信息

        Args:
            tmdbid: 剧集的TMDB ID

        Returns:
            TVResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request("GET", f"{self.base_url}/tv/{tmdbid}")

        return TVResponse(
            id=data["id"],
            poster="https://image.tmdb.org/t/p/w154/" + data["poster"],
            name=data["name"],
            overview=data["overview"],
            vote=data["vote"],
            first_air_date=data["first_air_date"],
            has_115=bool(data["115-flg"]),
        )

    def get_tv_115(self, tmdbid: int, page: int = 1) -> TV115Response:
        """获取剧集网盘资源

        Args:
            tmdbid: 剧集的TMDB ID
            page: 页码，默认为1

        Returns:
            TV115Response 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        if not self.api_key:
            raise ValueError("API KEY is required for this operation")

        data = self._request("GET", f"{self.base_url}/tv/{tmdbid}/115", {"page": page})

        items = [
            Movie115Item(
                title=item["title"], size=item["size"], share_link=item["share_link"]
            )
            for item in data["115"]
        ]

        return TV115Response(
            id=data["id"],
            media_type=data["media_type"],
            page=data["page"],
            total_page=data["total_page"],
            items=items,
        )

    def get_collection_115(self, tmdbid: int, page: int = 1) -> Collection115Response:
        """获取合集网盘资源

        Args:
            tmdbid: 合集的TMDB ID
            page: 页码，默认为1

        Returns:
            Collection115Response 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        if not self.api_key:
            raise ValueError("API KEY is required for this operation")

        data = self._request(
            "GET", f"{self.base_url}/collection/{tmdbid}/115", {"page": page}
        )

        items = [
            Movie115Item(
                title=item["title"], size=item["size"], share_link=item["share_link"]
            )
            for item in data["115"]
        ]

        return Collection115Response(
            id=data["id"],
            media_type=data["media_type"],
            page=data["page"],
            total_page=data["total_page"],
            items=items,
        )

    def get_tv_season(self, tmdbid: int, season_number: int) -> TVSeasonResponse:
        """获取剧集某一季的详细信息

        Args:
            tmdbid: 剧集的TMDB ID
            season_number: 季数

        Returns:
            TVSeasonResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
        """
        data = self._request(
            "GET", f"{self.base_url}/tv/{tmdbid}/season/{season_number}"
        )

        return TVSeasonResponse(
            season_number=data["season_number"],
            name=data["name"],
            overview=data["overview"],
            poster="https://image.tmdb.org/t/p/w154/" + data["poster"],
            air_date=data["air_date"],
            episode_count=data["episode_count"],
            vote_average=data["vote_average"],
            has_magnet=bool(data["magnet-flg"]),
        )

    def get_tv_season_magnet(
        self, tmdbid: int, season_number: int
    ) -> TVSeasonMagnetResponse:
        """获取剧集某一季的磁力资源

        Args:
            tmdbid: 剧集的TMDB ID
            season_number: 季数

        Returns:
            TVSeasonMagnetResponse 对象

        Raises:
            requests.exceptions.HTTPError: 当API返回非200状态码时
            ValueError: 当未设置API KEY时
        """
        if not self.api_key:
            raise ValueError("API KEY is required for this operation")

        data = self._request(
            "GET", f"{self.base_url}/tv/{tmdbid}/season/{season_number}/magnet"
        )

        items = [
            MovieMagnetItem(
                title=item["title"], size=item["size"], magnet=item["magnet"]
            )
            for item in data["magnet"]
        ]

        return TVSeasonMagnetResponse(
            season_number=data["season_number"],
            media_type=data["media_type"],
            items=items,
        )
