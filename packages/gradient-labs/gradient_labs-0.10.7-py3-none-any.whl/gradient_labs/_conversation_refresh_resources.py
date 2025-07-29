from typing import Optional, List

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class RefreshResourcesParams:
    scopes: Optional[List[str]] = None
    refresh_strategies: Optional[List[str]] = None
    type_ids: Optional[List[str]] = None


def refresh_conversation_resources(
    *, client: HttpClient, conversation_id: str, params: RefreshResourcesParams
) -> None:
    body = {}
    if params.scopes:
        body["scopes"] = params.scopes
    if params.refresh_strategies:
        body["refresh_strategies"] = params.refresh_strategies
    if params.type_ids:
        body["type_ids"] = params.type_ids

    _ = client.post(
        f"conversations/{conversation_id}/refresh-resources",
    )
