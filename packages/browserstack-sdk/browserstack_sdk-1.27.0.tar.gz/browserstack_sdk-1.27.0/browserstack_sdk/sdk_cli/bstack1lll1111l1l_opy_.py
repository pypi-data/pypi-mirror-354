# coding: UTF-8
import sys
bstack11lllll_opy_ = sys.version_info [0] == 2
bstack1l1l1_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack1l1lll1_opy_ (bstack1l1l11_opy_):
    global bstack11lll_opy_
    bstack11llll_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack111ll1l_opy_ = bstack1l1l11_opy_ [:-1]
    bstack1l1l_opy_ = bstack11llll_opy_ % len (bstack111ll1l_opy_)
    bstack1ll11l1_opy_ = bstack111ll1l_opy_ [:bstack1l1l_opy_] + bstack111ll1l_opy_ [bstack1l1l_opy_:]
    if bstack11lllll_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1_opy_ - (bstack1lll_opy_ + bstack11llll_opy_) % bstack1ll1l1_opy_) for bstack1lll_opy_, char in enumerate (bstack1ll11l1_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1_opy_ - (bstack1lll_opy_ + bstack11llll_opy_) % bstack1ll1l1_opy_) for bstack1lll_opy_, char in enumerate (bstack1ll11l1_opy_)])
    return eval (bstack11lll11_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1ll1lllllll_opy_ import bstack1ll1ll1llll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1111l1lll_opy_
from bstack_utils.helper import bstack1l1llll1111_opy_
import threading
import os
import urllib.parse
class bstack1lll1l111ll_opy_(bstack1lll1llll1l_opy_):
    def __init__(self, bstack1llll1l1l1l_opy_):
        super().__init__()
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1ll1lll_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1l1lll1_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111l111_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1ll1l1l_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1lll1l1_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1l1llll_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.QUIT, bstack1llllll1l1l_opy_.PRE), self.on_close)
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1lll_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        bstack1l1l1llll1l_opy_: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨቭ"):
            return
        if not bstack1l1llll1111_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቮ"))
            return
        def wrapped(bstack1l1l1llll1l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1lll11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1lll1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቯ"): True}).encode(bstack1l1lll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣተ")))
            if response is not None and response.capabilities:
                if not bstack1l1llll1111_opy_():
                    browser = launch(bstack1l1l1llll1l_opy_)
                    return browser
                bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1lll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤቱ")))
                if not bstack1l1l1ll11l1_opy_: # empty caps bstack1l1l1l1ll11_opy_ bstack1l1l1l1ll1l_opy_ bstack1l1l1lllll1_opy_ bstack1lll1llllll_opy_ or error in processing
                    return
                bstack1l1l1llll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1ll11l1_opy_))
                f.bstack1111111lll_opy_(instance, bstack1ll1ll1llll_opy_.bstack1l1l1lll111_opy_, bstack1l1l1llll11_opy_)
                f.bstack1111111lll_opy_(instance, bstack1ll1ll1llll_opy_.bstack1l1l1ll1111_opy_, bstack1l1l1ll11l1_opy_)
                browser = bstack1l1l1llll1l_opy_.connect(bstack1l1l1llll11_opy_)
                return browser
        return wrapped
    def bstack1l1l1ll1l1l_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨቲ"):
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦታ"))
            return
        if not bstack1l1llll1111_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1lll1_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ቴ"), {}).get(bstack1l1lll1_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩት")):
                    bstack1l1l1ll1l11_opy_ = args[0][bstack1l1lll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣቶ")][bstack1l1lll1_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦቷ")]
                    session_id = bstack1l1l1ll1l11_opy_.get(bstack1l1lll1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨቸ"))
                    f.bstack1111111lll_opy_(instance, bstack1ll1ll1llll_opy_.bstack1l1l1lll1ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢቹ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1l1llll_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        bstack1l1l1llll1l_opy_: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨቺ"):
            return
        if not bstack1l1llll1111_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቻ"))
            return
        def wrapped(bstack1l1l1llll1l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1lll11l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1lll1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቼ"): True}).encode(bstack1l1lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢች")))
            if response is not None and response.capabilities:
                bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1lll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቾ")))
                if not bstack1l1l1ll11l1_opy_:
                    return
                bstack1l1l1llll11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1ll11l1_opy_))
                if bstack1l1l1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩቿ")):
                    browser = bstack1l1l1llll1l_opy_.bstack1l1l1ll1ll1_opy_(bstack1l1l1llll11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1l1llll11_opy_
                    return connect(bstack1l1l1llll1l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1l1lll1_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        bstack1ll111lll1l_opy_: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨኀ"):
            return
        if not bstack1l1llll1111_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦኁ"))
            return
        def wrapped(bstack1ll111lll1l_opy_, bstack1l1l1ll11ll_opy_, *args, **kwargs):
            contexts = bstack1ll111lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l1lll1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦኂ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1ll11ll_opy_(bstack1ll111lll1l_opy_)
        return wrapped
    def bstack1l1l1lll11l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧኃ") + str(req) + bstack1l1lll1_opy_ (u"ࠣࠤኄ"))
        try:
            r = self.bstack1llll11l1l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧኅ") + str(r.success) + bstack1l1lll1_opy_ (u"ࠥࠦኆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤኇ") + str(e) + bstack1l1lll1_opy_ (u"ࠧࠨኈ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1lll1l1_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        Connection: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤ኉"):
            return
        if not bstack1l1llll1111_opy_():
            return
        def wrapped(Connection, bstack1l1l1ll111l_opy_, *args, **kwargs):
            return bstack1l1l1ll111l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1ll1llll_opy_,
        bstack1l1l1llll1l_opy_: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨኊ"):
            return
        if not bstack1l1llll1111_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦኋ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped