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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1lllllll1ll_opy_,
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1ll1ll1llll_opy_(bstack11111l1l1l_opy_):
    bstack1l11ll1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᎋ")
    bstack1l1l1lll1ll_opy_ = bstack1l1lll1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᎌ")
    bstack1l1l1lll111_opy_ = bstack1l1lll1_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᎍ")
    bstack1l1l1ll1111_opy_ = bstack1l1lll1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎎ")
    bstack1l11ll1ll1l_opy_ = bstack1l1lll1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᎏ")
    bstack1l11ll1l111_opy_ = bstack1l1lll1_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦ᎐")
    NAME = bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᎑")
    bstack1l11ll1l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1111ll_opy_: Any
    bstack1l11lll1111_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1lll1_opy_ (u"ࠧࡲࡡࡶࡰࡦ࡬ࠧ᎒"), bstack1l1lll1_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺࠢ᎓"), bstack1l1lll1_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤ᎔"), bstack1l1lll1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢ᎕"), bstack1l1lll1_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦ᎖")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1lllll1ll1l_opy_(methods)
    def bstack111111l1l1_opy_(self, instance: bstack1lllllll1ll_opy_, method_name: str, bstack111111lll1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1llllll11l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack11111l111l_opy_, bstack1l11ll1llll_opy_ = bstack1llllll1l11_opy_
        bstack1l11ll11lll_opy_ = bstack1ll1ll1llll_opy_.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        if bstack1l11ll11lll_opy_ in bstack1ll1ll1llll_opy_.bstack1l11ll1l1ll_opy_:
            bstack1l11ll1l11l_opy_ = None
            for callback in bstack1ll1ll1llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11ll11lll_opy_]:
                try:
                    bstack1l11ll1ll11_opy_ = callback(self, target, exec, bstack1llllll1l11_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l11l_opy_ == None:
                        bstack1l11ll1l11l_opy_ = bstack1l11ll1ll11_opy_
                except Exception as e:
                    self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣ᎗") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧ᎘"))
                    traceback.print_exc()
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11ll1l11l_opy_):
                return bstack1l11ll1l11l_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11ll1l11l_opy_:
                return bstack1l11ll1l11l_opy_
    def bstack1lllll1ll11_opy_(
        self, method_name, previous_state: bstack1llllll111l_opy_, *args, **kwargs
    ) -> bstack1llllll111l_opy_:
        if method_name == bstack1l1lll1_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬ࠬ᎙") or method_name == bstack1l1lll1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧ᎚") or method_name == bstack1l1lll1_opy_ (u"ࠧ࡯ࡧࡺࡣࡵࡧࡧࡦࠩ᎛"):
            return bstack1llllll111l_opy_.bstack1llllllll1l_opy_
        if method_name == bstack1l1lll1_opy_ (u"ࠨࡦ࡬ࡷࡵࡧࡴࡤࡪࠪ᎜"):
            return bstack1llllll111l_opy_.bstack111111l111_opy_
        if method_name == bstack1l1lll1_opy_ (u"ࠩࡦࡰࡴࡹࡥࠨ᎝"):
            return bstack1llllll111l_opy_.QUIT
        return bstack1llllll111l_opy_.NONE
    @staticmethod
    def bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_]):
        return bstack1l1lll1_opy_ (u"ࠥ࠾ࠧ᎞").join((bstack1llllll111l_opy_(bstack1llllll1l11_opy_[0]).name, bstack1llllll1l1l_opy_(bstack1llllll1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1lll1l_opy_(bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11ll11lll_opy_ = bstack1ll1ll1llll_opy_.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        if not bstack1l11ll11lll_opy_ in bstack1ll1ll1llll_opy_.bstack1l11ll1l1ll_opy_:
            bstack1ll1ll1llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11ll11lll_opy_] = []
        bstack1ll1ll1llll_opy_.bstack1l11ll1l1ll_opy_[bstack1l11ll11lll_opy_].append(callback)
    @staticmethod
    def bstack1ll1l11l1ll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111l1l_opy_(instance: bstack1lllllll1ll_opy_, default_value=None):
        return bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1ll1ll1llll_opy_.bstack1l1l1ll1111_opy_, default_value)
    @staticmethod
    def bstack1ll111l1l1l_opy_(instance: bstack1lllllll1ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11l1lll1_opy_(instance: bstack1lllllll1ll_opy_, default_value=None):
        return bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1ll1ll1llll_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str, *args):
        if not bstack1ll1ll1llll_opy_.bstack1ll1l11l1ll_opy_(method_name):
            return False
        if not bstack1ll1ll1llll_opy_.bstack1l11ll1ll1l_opy_ in bstack1ll1ll1llll_opy_.bstack1l1l111ll11_opy_(*args):
            return False
        bstack1ll11l111l1_opy_ = bstack1ll1ll1llll_opy_.bstack1ll11l1l111_opy_(*args)
        return bstack1ll11l111l1_opy_ and bstack1l1lll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ᎟") in bstack1ll11l111l1_opy_ and bstack1l1lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᎠ") in bstack1ll11l111l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᎡ")]
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str, *args):
        if not bstack1ll1ll1llll_opy_.bstack1ll1l11l1ll_opy_(method_name):
            return False
        if not bstack1ll1ll1llll_opy_.bstack1l11ll1ll1l_opy_ in bstack1ll1ll1llll_opy_.bstack1l1l111ll11_opy_(*args):
            return False
        bstack1ll11l111l1_opy_ = bstack1ll1ll1llll_opy_.bstack1ll11l1l111_opy_(*args)
        return (
            bstack1ll11l111l1_opy_
            and bstack1l1lll1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᎢ") in bstack1ll11l111l1_opy_
            and bstack1l1lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᎣ") in bstack1ll11l111l1_opy_[bstack1l1lll1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᎤ")]
        )
    @staticmethod
    def bstack1l1l111ll11_opy_(*args):
        return str(bstack1ll1ll1llll_opy_.bstack1ll1l111111_opy_(*args)).lower()