# Standard Library
import asyncio
import json
import os
from typing import List

from aiohttp import ClientSession, TCPConnector
from aiohttp_retry import RetryClient
from aiohttp_retry.retry_options import RandomRetry
from seqslab.auth.commands import BaseAuth
from seqslab.drs import API_HOSTNAME, __version__
from seqslab.exceptions import async_exception_handler
from termcolor import cprint
from yarl import URL

"""
Copyright (C) 2022, Atgenomix Incorporated.

All Rights Reserved.

This program is an unpublished copyrighted work which is proprietary to
Atgenomix Incorporated and contains confidential information that is not to
be reproduced or disclosed to any other person or entity without prior
written consent from Atgenomix, Inc. in each and every instance.

Unauthorized reproduction of this program as well as unauthorized
preparation of derivative works based upon the program or distribution of
copies by sale, rental, lease or lending are violations of federal copyright
laws and state trade secret laws, punishable by civil and criminal penalties.
"""

DRS_SEARCH_URL = f"https://{API_HOSTNAME}/ga4gh/drs/{__version__}/objects/search/"
DRS_OBJECT_URL = f"https://{API_HOSTNAME}/ga4gh/drs/{__version__}/objects/"


@async_exception_handler
async def drs_exact_match(names: List[str], labels: List[str], **kwargs) -> dict:
    if names and labels:
        raise ValueError("one search condition, either name or label, is allowed")

    try:
        token = BaseAuth.get_token().get("tokens").get("access")
    except KeyError:
        raise KeyError("No tokens, Please signin first!")

    pl = {
        "fields": ["self_uri", "name", "id", "tags"],
        "mode": "exact",
        "reverse": True,
        "order_by": "created_time",
    }

    if names:
        pl["names"] = names
    else:
        pl["tags"] = labels

    async with ClientSession(raise_for_status=False).request(
        method="post",
        url=DRS_SEARCH_URL,
        proxy=kwargs.get("proxy", None),
        headers={"Authorization": f"Bearer {token}"},
        json=pl,
    ) as response:
        resp = await response.content.read()
    return json.loads(resp)


@async_exception_handler
async def drs_keyword_search(keyword: str, labels: List[str], **kwargs) -> dict:
    try:
        token = BaseAuth.get_token().get("tokens").get("access")
    except KeyError:
        raise KeyError("No tokens, Please signin first!")
    params = f'?page_size={kwargs["page_size"]}&page={kwargs["page"]}&'
    if keyword:
        params += f"search={keyword}&"
    if labels:
        for lb in labels:
            params += f"label={lb}&"
    if types := kwargs["file_types"]:
        for t in types:
            params += f"file_types={t}&"
    if kwargs["owner"]:
        params += "owner=true&"
    url = f"{DRS_OBJECT_URL}{params}"
    async with ClientSession(raise_for_status=False).request(
        method="get",
        url=url.rstrip("&"),
        proxy=kwargs.get("proxy", None),
        headers={"Authorization": f"Bearer {token}"},
    ) as response:
        resp = await response.content.read()
    return json.loads(resp)


@async_exception_handler
async def drs_crud(drs_id: str, method: str, sem: asyncio.Semaphore, **kwargs) -> dict:
    try:
        token = BaseAuth.get_token().get("tokens").get("access")
    except KeyError:
        raise KeyError("No tokens, Please signin first!")

    query_opts = kwargs.get("query_opts", None)
    url = (
        os.path.join(DRS_OBJECT_URL, drs_id, query_opts)
        if query_opts
        else os.path.join(DRS_OBJECT_URL, drs_id)
    )
    connector = TCPConnector(limit_per_host=kwargs.get("concurrency", 5))
    async with sem:
        async with RetryClient(
            client_session=ClientSession(raise_for_status=False),
            retry_options=RandomRetry(attempts=3),
            connector=connector,
        ).request(
            method=method,
            url=url,
            proxy=kwargs.get("proxy", None),
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            resp = await response.content.read()
    return json.loads(resp) if len(resp) else None


@async_exception_handler
async def get_by_ids(drs_ids: List[str], **kwargs):
    tasks = []
    for drs_id in drs_ids:
        tasks.append(drs_crud(drs_id, "get", **kwargs))
    resp = await asyncio.gather(*tasks, return_exceptions=True)
    return resp


@async_exception_handler
async def drs_existence(path: URL, label_check: bool = True) -> bool:
    if label_check:
        res = await drs_exact_match(names=[], labels=[str(path)])
    else:
        res = await drs_exact_match(names=[os.path.basename(str(path))], labels=[])

    if not res.get("objects"):
        return False
    else:
        return True


@async_exception_handler
async def drs_delete(ids: List[str], names: List[str], labels: List[str], **kwargs):
    search = [
        drs_exact_match(names=names, labels=[]),
        drs_exact_match(names=[], labels=labels),
    ]
    resps = await asyncio.gather(*search, return_exceptions=False)
    drs_ids = list(
        set([ob.get("id") for res in resps for ob in res.get("objects")] + ids)
    )
    if not drs_ids:
        cprint("No object to be delete")
    else:
        cprint(f"drs to be delete {drs_ids}")
    sem = asyncio.Semaphore(5)
    delete = [drs_crud(drs, "delete", sem, **kwargs) for drs in drs_ids]
    resps_delete = await asyncio.gather(*delete, return_exceptions=False)
    return resps_delete
