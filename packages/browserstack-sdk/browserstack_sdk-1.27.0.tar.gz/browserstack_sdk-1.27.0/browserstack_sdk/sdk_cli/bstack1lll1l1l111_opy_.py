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
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
from bstack_utils.constants import EVENTS
class bstack1lll11l1l11_opy_(bstack11111l1l1l_opy_):
    bstack1l11ll1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᓴ")
    NAME = bstack1l1lll1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᓵ")
    bstack1l1l1lll111_opy_ = bstack1l1lll1_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧᓶ")
    bstack1l1l1lll1ll_opy_ = bstack1l1lll1_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᓷ")
    bstack1l11111l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠨࡩ࡯ࡲࡸࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᓸ")
    bstack1l1l1ll1111_opy_ = bstack1l1lll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓹ")
    bstack1l11llll1ll_opy_ = bstack1l1lll1_opy_ (u"ࠣ࡫ࡶࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡬ࡺࡨࠢᓺ")
    bstack1l11111ll11_opy_ = bstack1l1lll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᓻ")
    bstack1l11111ll1l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡩࡳࡪࡥࡥࡡࡤࡸࠧᓼ")
    bstack1ll1l1lllll_opy_ = bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᓽ")
    bstack1l11lllllll_opy_ = bstack1l1lll1_opy_ (u"ࠧࡴࡥࡸࡵࡨࡷࡸ࡯࡯࡯ࠤᓾ")
    bstack1l111111l1l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡧࡦࡶࠥᓿ")
    bstack1l1ll1ll11l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᔀ")
    bstack1l11ll1ll1l_opy_ = bstack1l1lll1_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࠦᔁ")
    bstack1l11ll1l111_opy_ = bstack1l1lll1_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࡦࡹࡹ࡯ࡥࠥᔂ")
    bstack1l11111l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᔃ")
    bstack1l11111lll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1l11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1111ll_opy_: Any
    bstack1l11lll1111_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1l11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll1111ll_opy_: Dict[str, Any],
        methods=[bstack1l1lll1_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᔄ"), bstack1l1lll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᔅ"), bstack1l1lll1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᔆ"), bstack1l1lll1_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᔇ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.platform_index = platform_index
        self.bstack1lllll1ll1l_opy_(methods)
        self.bstack1llll1111ll_opy_ = bstack1llll1111ll_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111l1l1l_opy_.get_data(bstack1lll11l1l11_opy_.bstack1l1l1lll1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111l1l1l_opy_.get_data(bstack1lll11l1l11_opy_.bstack1l1l1lll111_opy_, target, strict)
    @staticmethod
    def bstack1l11111l11l_opy_(target: object, strict=True):
        return bstack11111l1l1l_opy_.get_data(bstack1lll11l1l11_opy_.bstack1l11111l1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111l1l1l_opy_.get_data(bstack1lll11l1l11_opy_.bstack1l1l1ll1111_opy_, target, strict)
    @staticmethod
    def bstack1ll111l1l1l_opy_(instance: bstack1lllllll1ll_opy_) -> bool:
        return bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1l11llll1ll_opy_, False)
    @staticmethod
    def bstack1ll11l1lll1_opy_(instance: bstack1lllllll1ll_opy_, default_value=None):
        return bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll1l111l1l_opy_(instance: bstack1lllllll1ll_opy_, default_value=None):
        return bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1l1l1ll1111_opy_, default_value)
    @staticmethod
    def bstack1ll11l1111l_opy_(hub_url: str, bstack1l11111l111_opy_=bstack1l1lll1_opy_ (u"ࠣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠧᔈ")):
        try:
            bstack1l111111lll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l111111lll_opy_.endswith(bstack1l11111l111_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l11l1ll_opy_(method_name: str):
        return method_name == bstack1l1lll1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᔉ")
    @staticmethod
    def bstack1ll11ll111l_opy_(method_name: str, *args):
        return (
            bstack1lll11l1l11_opy_.bstack1ll1l11l1ll_opy_(method_name)
            and bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args) == bstack1lll11l1l11_opy_.bstack1l11lllllll_opy_
        )
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str, *args):
        if not bstack1lll11l1l11_opy_.bstack1ll1l11l1ll_opy_(method_name):
            return False
        if not bstack1lll11l1l11_opy_.bstack1l11ll1ll1l_opy_ in bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args):
            return False
        bstack1ll11l111l1_opy_ = bstack1lll11l1l11_opy_.bstack1ll11l1l111_opy_(*args)
        return bstack1ll11l111l1_opy_ and bstack1l1lll1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᔊ") in bstack1ll11l111l1_opy_ and bstack1l1lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔋ") in bstack1ll11l111l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᔌ")]
    @staticmethod
    def bstack1ll11ll1l1l_opy_(method_name: str, *args):
        if not bstack1lll11l1l11_opy_.bstack1ll1l11l1ll_opy_(method_name):
            return False
        if not bstack1lll11l1l11_opy_.bstack1l11ll1ll1l_opy_ in bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args):
            return False
        bstack1ll11l111l1_opy_ = bstack1lll11l1l11_opy_.bstack1ll11l1l111_opy_(*args)
        return (
            bstack1ll11l111l1_opy_
            and bstack1l1lll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᔍ") in bstack1ll11l111l1_opy_
            and bstack1l1lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡨࡸࡩࡱࡶࠥᔎ") in bstack1ll11l111l1_opy_[bstack1l1lll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᔏ")]
        )
    @staticmethod
    def bstack1l1l111ll11_opy_(*args):
        return str(bstack1lll11l1l11_opy_.bstack1ll1l111111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l111111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l1l111_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1l1l1l1_opy_(driver):
        command_executor = getattr(driver, bstack1l1lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔐ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1lll1_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᔑ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1lll1_opy_ (u"ࠦࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠧᔒ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1lll1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡤࡹࡥࡳࡸࡨࡶࡤࡧࡤࡥࡴࠥᔓ"), None)
        return hub_url
    def bstack1l1l11l1lll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1lll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᔔ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔕ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1lll1_opy_ (u"ࠣࡡࡸࡶࡱࠨᔖ")):
                setattr(command_executor, bstack1l1lll1_opy_ (u"ࠤࡢࡹࡷࡲࠢᔗ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1l11_opy_ = hub_url
            bstack1lll11l1l11_opy_.bstack1111111lll_opy_(instance, bstack1lll11l1l11_opy_.bstack1l1l1lll111_opy_, hub_url)
            bstack1lll11l1l11_opy_.bstack1111111lll_opy_(
                instance, bstack1lll11l1l11_opy_.bstack1l11llll1ll_opy_, bstack1lll11l1l11_opy_.bstack1ll11l1111l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_]):
        return bstack1l1lll1_opy_ (u"ࠥ࠾ࠧᔘ").join((bstack1llllll111l_opy_(bstack1llllll1l11_opy_[0]).name, bstack1llllll1l1l_opy_(bstack1llllll1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1lll1l_opy_(bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11ll11lll_opy_ = bstack1lll11l1l11_opy_.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        if not bstack1l11ll11lll_opy_ in bstack1lll11l1l11_opy_.bstack1l11111lll1_opy_:
            bstack1lll11l1l11_opy_.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_] = []
        bstack1lll11l1l11_opy_.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_].append(callback)
    def bstack111111l1l1_opy_(self, instance: bstack1lllllll1ll_opy_, method_name: str, bstack111111lll1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1lll1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᔙ")):
            return
        cmd = args[0] if method_name == bstack1l1lll1_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᔚ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l111111ll1_opy_ = bstack1l1lll1_opy_ (u"ࠨ࠺ࠣᔛ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠣᔜ") + bstack1l111111ll1_opy_, bstack111111lll1_opy_)
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
        bstack1l11ll11lll_opy_ = bstack1lll11l1l11_opy_.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡱࡱࡣ࡭ࡵ࡯࡬࠼ࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔝ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠤࠥᔞ"))
        if bstack11111l111l_opy_ == bstack1llllll111l_opy_.QUIT:
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE:
                bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack11ll1l1l_opy_.value)
                bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, EVENTS.bstack11ll1l1l_opy_.value, bstack1ll1l11l111_opy_)
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠥ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᔟ").format(instance, method_name, bstack11111l111l_opy_, bstack1l11ll1llll_opy_))
        if bstack11111l111l_opy_ == bstack1llllll111l_opy_.bstack1llllllll1l_opy_:
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and not bstack1lll11l1l11_opy_.bstack1l1l1lll1ll_opy_ in instance.data:
                session_id = getattr(target, bstack1l1lll1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᔠ"), None)
                if session_id:
                    instance.data[bstack1lll11l1l11_opy_.bstack1l1l1lll1ll_opy_] = session_id
        elif (
            bstack11111l111l_opy_ == bstack1llllll111l_opy_.bstack111111111l_opy_
            and bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args) == bstack1lll11l1l11_opy_.bstack1l11lllllll_opy_
        ):
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE:
                hub_url = bstack1lll11l1l11_opy_.bstack1l1l1l1l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll11l1l11_opy_.bstack1l1l1lll111_opy_: hub_url,
                            bstack1lll11l1l11_opy_.bstack1l11llll1ll_opy_: bstack1lll11l1l11_opy_.bstack1ll11l1111l_opy_(hub_url),
                            bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_: int(
                                os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᔡ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l111l1_opy_ = bstack1lll11l1l11_opy_.bstack1ll11l1l111_opy_(*args)
                bstack1l11111l11l_opy_ = bstack1ll11l111l1_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᔢ"), None) if bstack1ll11l111l1_opy_ else None
                if isinstance(bstack1l11111l11l_opy_, dict):
                    instance.data[bstack1lll11l1l11_opy_.bstack1l11111l1ll_opy_] = copy.deepcopy(bstack1l11111l11l_opy_)
                    instance.data[bstack1lll11l1l11_opy_.bstack1l1l1ll1111_opy_] = bstack1l11111l11l_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1lll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᔣ"), dict()).get(bstack1l1lll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦᔤ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll11l1l11_opy_.bstack1l1l1lll1ll_opy_: framework_session_id,
                                bstack1lll11l1l11_opy_.bstack1l11111ll11_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack11111l111l_opy_ == bstack1llllll111l_opy_.bstack111111111l_opy_
            and bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args) == bstack1lll11l1l11_opy_.bstack1l11111l1l1_opy_
            and bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST
        ):
            instance.data[bstack1lll11l1l11_opy_.bstack1l11111ll1l_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11ll11lll_opy_ in bstack1lll11l1l11_opy_.bstack1l11111lll1_opy_:
            bstack1l11ll1l11l_opy_ = None
            for callback in bstack1lll11l1l11_opy_.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_]:
                try:
                    bstack1l11ll1ll11_opy_ = callback(self, target, exec, bstack1llllll1l11_opy_, result, *args, **kwargs)
                    if bstack1l11ll1l11l_opy_ == None:
                        bstack1l11ll1l11l_opy_ = bstack1l11ll1ll11_opy_
                except Exception as e:
                    self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᔥ") + str(e) + bstack1l1lll1_opy_ (u"ࠥࠦᔦ"))
                    traceback.print_exc()
            if bstack11111l111l_opy_ == bstack1llllll111l_opy_.QUIT:
                if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST:
                    bstack1ll1l11l111_opy_ = bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, EVENTS.bstack11ll1l1l_opy_.value)
                    if bstack1ll1l11l111_opy_!=None:
                        bstack1lll11l11l1_opy_.end(EVENTS.bstack11ll1l1l_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔧ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔨ"), True, None)
            if bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11ll1l11l_opy_):
                return bstack1l11ll1l11l_opy_
            elif bstack1l11ll1llll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11ll1l11l_opy_:
                return bstack1l11ll1l11l_opy_
    def bstack1lllll1ll11_opy_(
        self, method_name, previous_state: bstack1llllll111l_opy_, *args, **kwargs
    ) -> bstack1llllll111l_opy_:
        if method_name == bstack1l1lll1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᔩ") or method_name == bstack1l1lll1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᔪ"):
            return bstack1llllll111l_opy_.bstack1llllllll1l_opy_
        if method_name == bstack1l1lll1_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᔫ"):
            return bstack1llllll111l_opy_.QUIT
        if method_name == bstack1l1lll1_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᔬ"):
            if previous_state != bstack1llllll111l_opy_.NONE:
                bstack1ll1l1l11ll_opy_ = bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args)
                if bstack1ll1l1l11ll_opy_ == bstack1lll11l1l11_opy_.bstack1l11lllllll_opy_:
                    return bstack1llllll111l_opy_.bstack1llllllll1l_opy_
            return bstack1llllll111l_opy_.bstack111111111l_opy_
        return bstack1llllll111l_opy_.NONE