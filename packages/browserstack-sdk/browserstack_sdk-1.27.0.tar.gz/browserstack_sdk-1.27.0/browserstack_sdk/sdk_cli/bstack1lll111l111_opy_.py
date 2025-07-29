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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from bstack_utils.helper import  bstack1l1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll1lll1_opy_, bstack1llll1lll11_opy_, bstack1lll11lllll_opy_, bstack1lll1l11ll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1111l111_opy_ import bstack1ll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1ll1lll1lll_opy_
from bstack_utils.percy import bstack111lll11l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lllll1l1ll_opy_(bstack1lll1llll1l_opy_):
    def __init__(self, bstack1l1ll11111l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll11111l_opy_ = bstack1l1ll11111l_opy_
        self.percy = bstack111lll11l_opy_()
        self.bstack1l1l11l11_opy_ = bstack1ll1ll11ll_opy_()
        self.bstack1l1ll111ll1_opy_()
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1llllll_opy_)
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), self.bstack1ll11l1ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11llll_opy_(self, instance: bstack1lllllll1ll_opy_, driver: object):
        bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1lllllll1l1_opy_(instance.context)
        for t in bstack1l1ll1l1ll1_opy_:
            bstack1l1lll11l11_opy_ = TestFramework.bstack1llllllll11_opy_(t, bstack1ll1lll1lll_opy_.bstack1l1llll1l11_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11l11_opy_) or instance == driver:
                return t
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll11l1l11_opy_.bstack1ll1l11l1ll_opy_(method_name):
                return
            platform_index = f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0)
            bstack1l1lll1l111_opy_ = self.bstack1l1ll11llll_opy_(instance, driver)
            bstack1l1ll111l1l_opy_ = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1l1ll111l11_opy_, None)
            if not bstack1l1ll111l1l_opy_:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦቖ"))
                return
            driver_command = f.bstack1ll1l111111_opy_(*args)
            for command in bstack1l111l1l11_opy_:
                if command == driver_command:
                    self.bstack1ll11ll1_opy_(driver, platform_index)
            bstack11ll1111ll_opy_ = self.percy.bstack1l1ll111_opy_()
            if driver_command in bstack11lllll1ll_opy_[bstack11ll1111ll_opy_]:
                self.bstack1l1l11l11_opy_.bstack1lll1l111_opy_(bstack1l1ll111l1l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨ቗"), e)
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
        bstack1l1lll11l11_opy_ = f.bstack1llllllll11_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1llll1l11_opy_, [])
        if not bstack1l1lll11l11_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቘ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠢࠣ቙"))
            return
        if len(bstack1l1lll11l11_opy_) > 1:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቚ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠤࠥቛ"))
        bstack1l1ll11l1ll_opy_, bstack1l1ll11l111_opy_ = bstack1l1lll11l11_opy_[0]
        driver = bstack1l1ll11l1ll_opy_()
        if not driver:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቜ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧቝ"))
            return
        bstack1l1ll111lll_opy_ = {
            TestFramework.bstack1ll11l1llll_opy_: bstack1l1lll1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣ቞"),
            TestFramework.bstack1ll1l11l11l_opy_: bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤ቟"),
            TestFramework.bstack1l1ll111l11_opy_: bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤበ")
        }
        bstack1l1ll1111ll_opy_ = { key: f.bstack1llllllll11_opy_(instance, key) for key in bstack1l1ll111lll_opy_ }
        bstack1l1ll1111l1_opy_ = [key for key, value in bstack1l1ll1111ll_opy_.items() if not value]
        if bstack1l1ll1111l1_opy_:
            for key in bstack1l1ll1111l1_opy_:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦቡ") + str(key) + bstack1l1lll1_opy_ (u"ࠤࠥቢ"))
            return
        platform_index = f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0)
        if self.bstack1l1ll11111l_opy_.percy_capture_mode == bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧባ"):
            bstack111l11l1_opy_ = bstack1l1ll1111ll_opy_.get(TestFramework.bstack1l1ll111l11_opy_) + bstack1l1lll1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢቤ")
            bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1l1ll111111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111l11l1_opy_,
                bstack11llll1111_opy_=bstack1l1ll1111ll_opy_[TestFramework.bstack1ll11l1llll_opy_],
                bstack11l1ll1l11_opy_=bstack1l1ll1111ll_opy_[TestFramework.bstack1ll1l11l11l_opy_],
                bstack1lll11111l_opy_=platform_index
            )
            bstack1lll11l11l1_opy_.end(EVENTS.bstack1l1ll111111_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧብ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦቦ"), True, None, None, None, None, test_name=bstack111l11l1_opy_)
    def bstack1ll11ll1_opy_(self, driver, platform_index):
        if self.bstack1l1l11l11_opy_.bstack11l111ll11_opy_() is True or self.bstack1l1l11l11_opy_.capturing() is True:
            return
        self.bstack1l1l11l11_opy_.bstack1l111ll1ll_opy_()
        while not self.bstack1l1l11l11_opy_.bstack11l111ll11_opy_():
            bstack1l1ll111l1l_opy_ = self.bstack1l1l11l11_opy_.bstack11ll1l11_opy_()
            self.bstack11l11111_opy_(driver, bstack1l1ll111l1l_opy_, platform_index)
        self.bstack1l1l11l11_opy_.bstack11l1lll1l_opy_()
    def bstack11l11111_opy_(self, driver, bstack111l1111l_opy_, platform_index, test=None):
        from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
        bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack11ll111lll_opy_.value)
        if test != None:
            bstack11llll1111_opy_ = getattr(test, bstack1l1lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬቧ"), None)
            bstack11l1ll1l11_opy_ = getattr(test, bstack1l1lll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ቨ"), None)
            PercySDK.screenshot(driver, bstack111l1111l_opy_, bstack11llll1111_opy_=bstack11llll1111_opy_, bstack11l1ll1l11_opy_=bstack11l1ll1l11_opy_, bstack1lll11111l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack111l1111l_opy_)
        bstack1lll11l11l1_opy_.end(EVENTS.bstack11ll111lll_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤቩ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣቪ"), True, None, None, None, None, test_name=bstack111l1111l_opy_)
    def bstack1l1ll111ll1_opy_(self):
        os.environ[bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩቫ")] = str(self.bstack1l1ll11111l_opy_.success)
        os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩቬ")] = str(self.bstack1l1ll11111l_opy_.percy_capture_mode)
        self.percy.bstack1l1ll11l1l1_opy_(self.bstack1l1ll11111l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll11l11l_opy_(self.bstack1l1ll11111l_opy_.percy_build_id)