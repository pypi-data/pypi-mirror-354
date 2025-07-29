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
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll1ll_opy_,
    bstack1lllllll111_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1llll1111_opy_, bstack1l1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_, bstack1llll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllllll_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l11l1_opy_ import bstack1ll111ll1l1_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1lll11llll_opy_ import bstack1ll1l11ll_opy_, bstack1l111ll1l_opy_, bstack1lll1llll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1ll1lll1l11_opy_(bstack1ll111ll1l1_opy_):
    bstack1l1l11ll1ll_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣኌ")
    bstack1l1llll1l11_opy_ = bstack1l1lll1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤኍ")
    bstack1l1l1l1l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨ኎")
    bstack1l1l1l1111l_opy_ = bstack1l1lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧ኏")
    bstack1l1l1l11lll_opy_ = bstack1l1lll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥነ")
    bstack1l1ll1lll1l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨኑ")
    bstack1l1l11llll1_opy_ = bstack1l1lll1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦኒ")
    bstack1l1l1l11l1l_opy_ = bstack1l1lll1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢና")
    def __init__(self):
        super().__init__(bstack1ll111l11ll_opy_=self.bstack1l1l11ll1ll_opy_, frameworks=[bstack1lll11l1l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.BEFORE_EACH, bstack1lll11lllll_opy_.POST), self.bstack1l1l1l111l1_opy_)
        if bstack1l1ll1lll1_opy_():
            TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), self.bstack1ll1l11111l_opy_)
        else:
            TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.PRE), self.bstack1ll1l11111l_opy_)
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), self.bstack1ll11l1ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l111ll_opy_ = self.bstack1l1l11lll11_opy_(instance.context)
        if not bstack1l1l1l111ll_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣኔ") + str(bstack1llllll1l11_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧን"))
            return
        f.bstack1111111lll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1llll1l11_opy_, bstack1l1l1l111ll_opy_)
    def bstack1l1l11lll11_opy_(self, context: bstack1lllllll111_opy_, bstack1l1l1l11111_opy_= True):
        if bstack1l1l1l11111_opy_:
            bstack1l1l1l111ll_opy_ = self.bstack1ll111lll11_opy_(context, reverse=True)
        else:
            bstack1l1l1l111ll_opy_ = self.bstack1ll111ll111_opy_(context, reverse=True)
        return [f for f in bstack1l1l1l111ll_opy_ if f[1].state != bstack1llllll111l_opy_.QUIT]
    def bstack1ll1l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l111l1_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        if not bstack1l1llll1111_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኖ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠨࠢኗ"))
            return
        bstack1l1l1l111ll_opy_ = f.bstack1llllllll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1llll1l11_opy_, [])
        if not bstack1l1l1l111ll_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኘ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠣࠤኙ"))
            return
        if len(bstack1l1l1l111ll_opy_) > 1:
            self.logger.debug(
                bstack1ll1lll1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦኚ"))
        bstack1l1l11lllll_opy_, bstack1l1ll11l111_opy_ = bstack1l1l1l111ll_opy_[0]
        page = bstack1l1l11lllll_opy_()
        if not page:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኛ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧኜ"))
            return
        bstack1ll1llllll_opy_ = getattr(args[0], bstack1l1lll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧኝ"), None)
        try:
            page.evaluate(bstack1l1lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢኞ"),
                        bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫኟ") + json.dumps(
                            bstack1ll1llllll_opy_) + bstack1l1lll1_opy_ (u"ࠣࡿࢀࠦአ"))
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢኡ"), e)
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l111l1_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        if not bstack1l1llll1111_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኢ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧኣ"))
            return
        bstack1l1l1l111ll_opy_ = f.bstack1llllllll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1llll1l11_opy_, [])
        if not bstack1l1l1l111ll_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኤ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠨࠢእ"))
            return
        if len(bstack1l1l1l111ll_opy_) > 1:
            self.logger.debug(
                bstack1ll1lll1ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤኦ"))
        bstack1l1l11lllll_opy_, bstack1l1ll11l111_opy_ = bstack1l1l1l111ll_opy_[0]
        page = bstack1l1l11lllll_opy_()
        if not page:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኧ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠤࠥከ"))
            return
        status = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1l1l1l11l_opy_, None)
        if not status:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨኩ") + str(bstack1llllll1l11_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧኪ"))
            return
        bstack1l1l11ll1l1_opy_ = {bstack1l1lll1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧካ"): status.lower()}
        bstack1l1l1l11l11_opy_ = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1l1l1l111_opy_, None)
        if status.lower() == bstack1l1lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኬ") and bstack1l1l1l11l11_opy_ is not None:
            bstack1l1l11ll1l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧክ")] = bstack1l1l1l11l11_opy_[0][bstack1l1lll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫኮ")][0] if isinstance(bstack1l1l1l11l11_opy_, list) else str(bstack1l1l1l11l11_opy_)
        try:
              page.evaluate(
                    bstack1l1lll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥኯ"),
                    bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨኰ")
                    + json.dumps(bstack1l1l11ll1l1_opy_)
                    + bstack1l1lll1_opy_ (u"ࠦࢂࠨ኱")
                )
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧኲ"), e)
    def bstack1l1lll111l1_opy_(
        self,
        instance: bstack1llll1lll11_opy_,
        f: TestFramework,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l111l1_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        if not bstack1l1llll1111_opy_:
            self.logger.debug(
                bstack1ll1lll1ll1_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢኳ"))
            return
        bstack1l1l1l111ll_opy_ = f.bstack1llllllll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1llll1l11_opy_, [])
        if not bstack1l1l1l111ll_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኴ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠣࠤኵ"))
            return
        if len(bstack1l1l1l111ll_opy_) > 1:
            self.logger.debug(
                bstack1ll1lll1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦ኶"))
        bstack1l1l11lllll_opy_, bstack1l1ll11l111_opy_ = bstack1l1l1l111ll_opy_[0]
        page = bstack1l1l11lllll_opy_()
        if not page:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ኷") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧኸ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1lll1_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥኹ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢኺ"),
                bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬኻ").format(
                    json.dumps(
                        {
                            bstack1l1lll1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣኼ"): bstack1l1lll1_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦኽ"),
                            bstack1l1lll1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨኾ"): {
                                bstack1l1lll1_opy_ (u"ࠦࡹࡿࡰࡦࠤ኿"): bstack1l1lll1_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤዀ"),
                                bstack1l1lll1_opy_ (u"ࠨࡤࡢࡶࡤࠦ዁"): data,
                                bstack1l1lll1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨዂ"): bstack1l1lll1_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢዃ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦዄ"), e)
    def bstack1ll1111ll1l_opy_(
        self,
        instance: bstack1llll1lll11_opy_,
        f: TestFramework,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l111l1_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        if f.bstack1llllllll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1ll1lll1l_opy_, False):
            return
        self.bstack1ll1l1111ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l1lllll_opy_)
        req.test_framework_name = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll11llllll_opy_)
        req.test_framework_version = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_state = bstack1llllll1l11_opy_[0].name
        req.test_hook_state = bstack1llllll1l11_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l11l11l_opy_)
        for bstack1l1l1l1l1l1_opy_ in bstack1ll1ll1llll_opy_.bstack1lllllll11l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤዅ")
                if bstack1l1llll1111_opy_
                else bstack1l1lll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥ዆")
            )
            session.ref = bstack1l1l1l1l1l1_opy_.ref()
            session.hub_url = bstack1ll1ll1llll_opy_.bstack1llllllll11_opy_(bstack1l1l1l1l1l1_opy_, bstack1ll1ll1llll_opy_.bstack1l1l1lll111_opy_, bstack1l1lll1_opy_ (u"ࠧࠨ዇"))
            session.framework_name = bstack1l1l1l1l1l1_opy_.framework_name
            session.framework_version = bstack1l1l1l1l1l1_opy_.framework_version
            session.framework_session_id = bstack1ll1ll1llll_opy_.bstack1llllllll11_opy_(bstack1l1l1l1l1l1_opy_, bstack1ll1ll1llll_opy_.bstack1l1l1lll1ll_opy_, bstack1l1lll1_opy_ (u"ࠨࠢወ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1l111ll_opy_ = f.bstack1llllllll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l1llll1l11_opy_, [])
        if not bstack1l1l1l111ll_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዉ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠣࠤዊ"))
            return
        if len(bstack1l1l1l111ll_opy_) > 1:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዋ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠥࠦዌ"))
        bstack1l1l11lllll_opy_, bstack1l1ll11l111_opy_ = bstack1l1l1l111ll_opy_[0]
        page = bstack1l1l11lllll_opy_()
        if not page:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦው") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠧࠨዎ"))
            return
        return page
    def bstack1ll1l111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l11lll1l_opy_ = {}
        for bstack1l1l1l1l1l1_opy_ in bstack1ll1ll1llll_opy_.bstack1lllllll11l_opy_.values():
            caps = bstack1ll1ll1llll_opy_.bstack1llllllll11_opy_(bstack1l1l1l1l1l1_opy_, bstack1ll1ll1llll_opy_.bstack1l1l1ll1111_opy_, bstack1l1lll1_opy_ (u"ࠨࠢዏ"))
        bstack1l1l11lll1l_opy_[bstack1l1lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧዐ")] = caps.get(bstack1l1lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤዑ"), bstack1l1lll1_opy_ (u"ࠤࠥዒ"))
        bstack1l1l11lll1l_opy_[bstack1l1lll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤዓ")] = caps.get(bstack1l1lll1_opy_ (u"ࠦࡴࡹࠢዔ"), bstack1l1lll1_opy_ (u"ࠧࠨዕ"))
        bstack1l1l11lll1l_opy_[bstack1l1lll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣዖ")] = caps.get(bstack1l1lll1_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ዗"), bstack1l1lll1_opy_ (u"ࠣࠤዘ"))
        bstack1l1l11lll1l_opy_[bstack1l1lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥዙ")] = caps.get(bstack1l1lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧዚ"), bstack1l1lll1_opy_ (u"ࠦࠧዛ"))
        return bstack1l1l11lll1l_opy_
    def bstack1ll11ll1111_opy_(self, page: object, bstack1ll1l1l11l1_opy_, args={}):
        try:
            bstack1l1l1l11ll1_opy_ = bstack1l1lll1_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡻࡧࡰࡢࡦࡴࡪࡹࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦዜ")
            bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_.replace(bstack1l1lll1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤዝ"), bstack1l1lll1_opy_ (u"ࠢࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠢዞ"))
            script = bstack1l1l1l11ll1_opy_.format(fn_body=bstack1ll1l1l11l1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠣࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡇࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸ࠱ࠦࠢዟ") + str(e) + bstack1l1lll1_opy_ (u"ࠤࠥዠ"))