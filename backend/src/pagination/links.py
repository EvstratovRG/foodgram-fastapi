from typing import Optional, Mapping, Any
from fastapi import Request


class LinkCreator:

    @staticmethod
    def create_link(
        link: Optional[Mapping[str, Any]],
        request: Request
    ) -> Any:
        url = str(request.url)
        url = url.rsplit('?')[0] + '?page=' + str(link['page'])
        return url

    @staticmethod
    def generate_links(
        page: int,
        limit: int,
        total: int,
        request: Request
    ) -> Any:
        links = {}
        if page * limit < total:
            links["next"] = LinkCreator.create_link(
                request=request,
                link={"page": page + 1}
            )
        else:
            links["next"] = None
        if page > 1:
            links["previous"] = LinkCreator.create_link(
                request=request,
                link={"page": page - 1}
            )
        else:
            links["previous"] = None
        return links
