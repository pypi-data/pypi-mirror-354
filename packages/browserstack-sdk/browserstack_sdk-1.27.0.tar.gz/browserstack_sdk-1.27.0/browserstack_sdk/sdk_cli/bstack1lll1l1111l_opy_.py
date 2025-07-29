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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import bstack1lllllll1ll_opy_, bstack1llllll111l_opy_, bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll1lll1_opy_, bstack1llll1lll11_opy_, bstack1lll11lllll_opy_, bstack1lll1l11ll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1llll1111_opy_, bstack1l1ll1lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1lll1_opy_ = [bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇚ"), bstack1l1lll1_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᇛ"), bstack1l1lll1_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᇜ"), bstack1l1lll1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᇝ"), bstack1l1lll1_opy_ (u"ࠥࡴࡦࡺࡨࠣᇞ")]
bstack1l1lll1ll11_opy_ = bstack1l1ll1lll11_opy_()
bstack1ll1111l11l_opy_ = bstack1l1lll1_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᇟ")
bstack1l1lllll1l1_opy_ = {
    bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᇠ"): bstack1l1lll1lll1_opy_,
    bstack1l1lll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᇡ"): bstack1l1lll1lll1_opy_,
    bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᇢ"): bstack1l1lll1lll1_opy_,
    bstack1l1lll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᇣ"): bstack1l1lll1lll1_opy_,
    bstack1l1lll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᇤ"): bstack1l1lll1lll1_opy_
    + [
        bstack1l1lll1_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᇥ"),
        bstack1l1lll1_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᇦ"),
        bstack1l1lll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᇧ"),
        bstack1l1lll1_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᇨ"),
        bstack1l1lll1_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᇩ"),
        bstack1l1lll1_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᇪ"),
        bstack1l1lll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᇫ"),
        bstack1l1lll1_opy_ (u"ࠥࡷࡹࡵࡰࠣᇬ"),
        bstack1l1lll1_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᇭ"),
        bstack1l1lll1_opy_ (u"ࠧࡽࡨࡦࡰࠥᇮ"),
    ],
    bstack1l1lll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᇯ"): [bstack1l1lll1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᇰ"), bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᇱ"), bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᇲ"), bstack1l1lll1_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᇳ")],
    bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᇴ"): [bstack1l1lll1_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᇵ"), bstack1l1lll1_opy_ (u"ࠨࡡࡳࡩࡶࠦᇶ")],
    bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᇷ"): [bstack1l1lll1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᇸ"), bstack1l1lll1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᇹ"), bstack1l1lll1_opy_ (u"ࠥࡪࡺࡴࡣࠣᇺ"), bstack1l1lll1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᇻ"), bstack1l1lll1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᇼ"), bstack1l1lll1_opy_ (u"ࠨࡩࡥࡵࠥᇽ")],
    bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᇾ"): [bstack1l1lll1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᇿ"), bstack1l1lll1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣሀ"), bstack1l1lll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣሁ")],
    bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨሂ"): [bstack1l1lll1_opy_ (u"ࠧࡽࡨࡦࡰࠥሃ"), bstack1l1lll1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨሄ")],
    bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣህ"): [bstack1l1lll1_opy_ (u"ࠣࡰࡲࡨࡪࠨሆ"), bstack1l1lll1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤሇ")],
    bstack1l1lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥለ"): [bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሉ"), bstack1l1lll1_opy_ (u"ࠧࡧࡲࡨࡵࠥሊ"), bstack1l1lll1_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨላ")],
}
_1l1ll1l11l1_opy_ = set()
class bstack1llll1lllll_opy_(bstack1lll1llll1l_opy_):
    bstack1l1ll11lll1_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢሌ")
    bstack1l1lll1l11l_opy_ = bstack1l1lll1_opy_ (u"ࠣࡋࡑࡊࡔࠨል")
    bstack1ll1111ll11_opy_ = bstack1l1lll1_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣሎ")
    bstack1l1lll1ll1l_opy_: Callable
    bstack1l1lll1l1ll_opy_: Callable
    def __init__(self, bstack1llll111111_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.bstack1ll1l11ll1l_opy_ = bstack1llll1l1l1l_opy_
        if os.getenv(bstack1l1lll1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢሏ"), bstack1l1lll1_opy_ (u"ࠦ࠶ࠨሐ")) != bstack1l1lll1_opy_ (u"ࠧ࠷ࠢሑ") or not self.is_enabled():
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࠢሒ") + str(self.__class__.__name__) + bstack1l1lll1_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥሓ"))
            return
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.PRE), self.bstack1ll1l11111l_opy_)
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), self.bstack1ll11l1ll1l_opy_)
        for event in bstack1ll1ll1lll1_opy_:
            for state in bstack1lll11lllll_opy_:
                TestFramework.bstack1ll1l1lll1l_opy_((event, state), self.bstack1ll1111lll1_opy_)
        bstack1llll111111_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1ll1llll1_opy_)
        self.bstack1l1lll1ll1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll111111ll_opy_(bstack1llll1lllll_opy_.bstack1l1lll1l11l_opy_, self.bstack1l1lll1ll1l_opy_)
        self.bstack1l1lll1l1ll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll111111ll_opy_(bstack1llll1lllll_opy_.bstack1ll1111ll11_opy_, self.bstack1l1lll1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll1llll_opy_() and instance:
            bstack1l1lll11l1l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllll1l11_opy_
            if test_framework_state == bstack1ll1ll1lll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG:
                bstack11lll1ll1_opy_ = datetime.now()
                entries = f.bstack1l1llllll1l_opy_(instance, bstack1llllll1l11_opy_)
                if entries:
                    self.bstack1l1lllll11l_opy_(instance, entries)
                    instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣሔ"), datetime.now() - bstack11lll1ll1_opy_)
                    f.bstack1ll1111111l_opy_(instance, bstack1llllll1l11_opy_)
                instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧሕ"), datetime.now() - bstack1l1lll11l1l_opy_)
                return # bstack1l1ll1l1111_opy_ not send this event with the bstack1l1ll1ll111_opy_ bstack1l1lllllll1_opy_
            elif (
                test_framework_state == bstack1ll1ll1lll1_opy_.TEST
                and test_hook_state == bstack1lll11lllll_opy_.POST
                and not f.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
            ):
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣሖ") + str(TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)) + bstack1l1lll1_opy_ (u"ࠦࠧሗ"))
                f.bstack1111111lll_opy_(instance, bstack1llll1lllll_opy_.bstack1l1ll11lll1_opy_, True)
                return # bstack1l1ll1l1111_opy_ not send this event bstack1ll111111l1_opy_ bstack1ll11111l1l_opy_
            elif (
                f.bstack1llllllll11_opy_(instance, bstack1llll1lllll_opy_.bstack1l1ll11lll1_opy_, False)
                and test_framework_state == bstack1ll1ll1lll1_opy_.LOG_REPORT
                and test_hook_state == bstack1lll11lllll_opy_.POST
                and f.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
            ):
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦመ") + str(TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)) + bstack1l1lll1_opy_ (u"ࠨࠢሙ"))
                self.bstack1ll1111lll1_opy_(f, instance, (bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), *args, **kwargs)
            bstack11lll1ll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll1l1l11_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1lll1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥሚ"), None), data.pop(bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣማ"), {}).values()),
                key=lambda x: x[bstack1l1lll1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧሜ")],
            )
            if bstack1ll1lll1lll_opy_.bstack1l1llll1l11_opy_ in data:
                data.pop(bstack1ll1lll1lll_opy_.bstack1l1llll1l11_opy_)
            data.update({bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥም"): bstack1l1ll1l1l11_opy_})
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤሞ"), datetime.now() - bstack11lll1ll1_opy_)
            bstack11lll1ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll11111l11_opy_)
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣሟ"), datetime.now() - bstack11lll1ll1_opy_)
            self.bstack1l1lllllll1_opy_(instance, bstack1llllll1l11_opy_, event_json=event_json)
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤሠ"), datetime.now() - bstack1l1lll11l1l_opy_)
    def bstack1ll1l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
        bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1l11ll1l1l_opy_.value)
        self.bstack1ll1l11ll1l_opy_.bstack1l1lll111l1_opy_(instance, f, bstack1llllll1l11_opy_, *args, **kwargs)
        bstack1lll11l11l1_opy_.end(EVENTS.bstack1l11ll1l1l_opy_.value, bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢሡ"), bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨሢ"), status=True, failure=None, test_name=None)
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l11ll1l_opy_.bstack1ll1111ll1l_opy_(instance, f, bstack1llllll1l11_opy_, *args, **kwargs)
        self.bstack1ll1111l111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lllll111_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1ll1111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧሣ"))
            return
        bstack11lll1ll1_opy_ = datetime.now()
        try:
            r = self.bstack1llll11l1l1_opy_.TestSessionEvent(req)
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦሤ"), datetime.now() - bstack11lll1ll1_opy_)
            f.bstack1111111lll_opy_(instance, self.bstack1ll1l11ll1l_opy_.bstack1l1ll1lll1l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1lll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨሥ") + str(r) + bstack1l1lll1_opy_ (u"ࠧࠨሦ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦሧ") + str(e) + bstack1l1lll1_opy_ (u"ࠢࠣረ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1llll1_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        _driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        _1ll11111lll_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll11l1l11_opy_.bstack1ll1l11l1ll_opy_(method_name):
            return
        if f.bstack1ll1l111111_opy_(*args) == bstack1lll11l1l11_opy_.bstack1l1ll1ll11l_opy_:
            bstack1l1lll11l1l_opy_ = datetime.now()
            screenshot = result.get(bstack1l1lll1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢሩ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥሪ"))
                return
            bstack1l1lll1l111_opy_ = self.bstack1l1ll11llll_opy_(instance)
            if bstack1l1lll1l111_opy_:
                entry = bstack1lll1l11ll1_opy_(TestFramework.bstack1l1llll11ll_opy_, screenshot)
                self.bstack1l1lllll11l_opy_(bstack1l1lll1l111_opy_, [entry])
                instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦራ"), datetime.now() - bstack1l1lll11l1l_opy_)
            else:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤሬ").format(instance.ref()))
        event = {}
        bstack1l1lll1l111_opy_ = self.bstack1l1ll11llll_opy_(instance)
        if bstack1l1lll1l111_opy_:
            self.bstack1ll1111l1ll_opy_(event, bstack1l1lll1l111_opy_)
            if event.get(bstack1l1lll1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥር")):
                self.bstack1l1lllll11l_opy_(bstack1l1lll1l111_opy_, event[bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሮ")])
            else:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦሯ"))
    @measure(event_name=EVENTS.bstack1ll1111l1l1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1lllll11l_opy_(
        self,
        bstack1l1lll1l111_opy_: bstack1llll1lll11_opy_,
        entries: List[bstack1lll1l11ll1_opy_],
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1ll1l1lllll_opy_)
        req.execution_context.hash = str(bstack1l1lll1l111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1ll11llllll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.uuid = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1ll1l11l11l_opy_)
            log_entry.test_framework_state = bstack1l1lll1l111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢሰ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1lll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦሱ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1lllll_opy_
                log_entry.file_path = entry.bstack1l1111l_opy_
        def bstack1ll11111ll1_opy_():
            bstack11lll1ll1_opy_ = datetime.now()
            try:
                self.bstack1llll11l1l1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1llll11ll_opy_:
                    bstack1l1lll1l111_opy_.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢሲ"), datetime.now() - bstack11lll1ll1_opy_)
                elif entry.kind == TestFramework.bstack1l1lll11ll1_opy_:
                    bstack1l1lll1l111_opy_.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣሳ"), datetime.now() - bstack11lll1ll1_opy_)
                else:
                    bstack1l1lll1l111_opy_.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤሴ"), datetime.now() - bstack11lll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦስ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l11111_opy_.enqueue(bstack1ll11111ll1_opy_)
    @measure(event_name=EVENTS.bstack1l1ll1l1l1l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1lllllll1_opy_(
        self,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        event_json=None,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l1lllll_opy_)
        req.test_framework_name = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll11llllll_opy_)
        req.test_framework_version = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_state = bstack1llllll1l11_opy_[0].name
        req.test_hook_state = bstack1llllll1l11_opy_[1].name
        started_at = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1llll111l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1lll11lll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll11111l11_opy_)).encode(bstack1l1lll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨሶ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll11111ll1_opy_():
            bstack11lll1ll1_opy_ = datetime.now()
            try:
                self.bstack1llll11l1l1_opy_.TestFrameworkEvent(req)
                instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦሷ"), datetime.now() - bstack11lll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሸ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l11111_opy_.enqueue(bstack1ll11111ll1_opy_)
    def bstack1l1ll11llll_opy_(self, instance: bstack1lllllll1ll_opy_):
        bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1lllllll1l1_opy_(instance.context)
        for t in bstack1l1ll1l1ll1_opy_:
            bstack1l1lll11l11_opy_ = TestFramework.bstack1llllllll11_opy_(t, bstack1ll1lll1lll_opy_.bstack1l1llll1l11_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11l11_opy_):
                return t
    def bstack1l1ll1l11ll_opy_(self, message):
        self.bstack1l1lll1ll1l_opy_(message + bstack1l1lll1_opy_ (u"ࠥࡠࡳࠨሹ"))
    def log_error(self, message):
        self.bstack1l1lll1l1ll_opy_(message + bstack1l1lll1_opy_ (u"ࠦࡡࡴࠢሺ"))
    def bstack1ll111111ll_opy_(self, level, original_func):
        def bstack1l1llll1ll1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1l1llllll11_opy_()
            if not bstack1l1ll1l1ll1_opy_:
                return return_value
            bstack1l1lll1l111_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1l1ll1_opy_
                    if TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll1l11l11l_opy_)
                ),
                None,
            )
            if not bstack1l1lll1l111_opy_:
                return
            entry = bstack1lll1l11ll1_opy_(TestFramework.bstack1l1lll1l1l1_opy_, message, level)
            self.bstack1l1lllll11l_opy_(bstack1l1lll1l111_opy_, [entry])
            return return_value
        return bstack1l1llll1ll1_opy_
    def bstack1ll1111l1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1l11l1_opy_
        levels = [bstack1l1lll1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣሻ"), bstack1l1lll1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥሼ")]
        bstack1l1lll1111l_opy_ = bstack1l1lll1_opy_ (u"ࠢࠣሽ")
        if instance is not None:
            try:
                bstack1l1lll1111l_opy_ = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l11l11l_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡸ࡭ࡩࠦࡦࡳࡱࡰࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨሾ").format(e))
        bstack1l1ll1l111l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሿ")]
                bstack1l1llllllll_opy_ = os.path.join(bstack1l1lll1ll11_opy_, (bstack1ll1111l11l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1llllllll_opy_):
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡮ࡰࡶࠣࡴࡷ࡫ࡳࡦࡰࡷࠤ࡫ࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡚ࠥࡥࡴࡶࠣࡥࡳࡪࠠࡃࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨቀ").format(bstack1l1llllllll_opy_))
                    continue
                file_names = os.listdir(bstack1l1llllllll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1llllllll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1l11l1_opy_:
                        self.logger.info(bstack1l1lll1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤቁ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll11ll11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll11ll11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1lll1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣቂ"):
                                entry = bstack1lll1l11ll1_opy_(
                                    kind=bstack1l1lll1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣቃ"),
                                    message=bstack1l1lll1_opy_ (u"ࠢࠣቄ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1lllll_opy_=file_size,
                                    bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣቅ"),
                                    bstack1l1111l_opy_=os.path.abspath(file_path),
                                    bstack11lll1llll_opy_=bstack1l1lll1111l_opy_
                                )
                            elif level == bstack1l1lll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨቆ"):
                                entry = bstack1lll1l11ll1_opy_(
                                    kind=bstack1l1lll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧቇ"),
                                    message=bstack1l1lll1_opy_ (u"ࠦࠧቈ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1lllll_opy_=file_size,
                                    bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧ቉"),
                                    bstack1l1111l_opy_=os.path.abspath(file_path),
                                    bstack1l1lllll1ll_opy_=bstack1l1lll1111l_opy_
                                )
                            bstack1l1ll1l111l_opy_.append(entry)
                            _1l1ll1l11l1_opy_.add(abs_path)
                        except Exception as bstack1ll11111111_opy_:
                            self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧቊ").format(bstack1ll11111111_opy_))
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨቋ").format(e))
        event[bstack1l1lll1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨቌ")] = bstack1l1ll1l111l_opy_
class bstack1ll11111l11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1llll11l1_opy_ = set()
        kwargs[bstack1l1lll1_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦቍ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1ll1ll_opy_(obj, self.bstack1l1llll11l1_opy_)
def bstack1l1llll1l1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1ll1ll_opy_(obj, bstack1l1llll11l1_opy_=None, max_depth=3):
    if bstack1l1llll11l1_opy_ is None:
        bstack1l1llll11l1_opy_ = set()
    if id(obj) in bstack1l1llll11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1llll11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1lll_opy_ = TestFramework.bstack1l1ll1l1lll_opy_(obj)
    bstack1ll1111llll_opy_ = next((k.lower() in bstack1l1llll1lll_opy_.lower() for k in bstack1l1lllll1l1_opy_.keys()), None)
    if bstack1ll1111llll_opy_:
        obj = TestFramework.bstack1l1ll11ll1l_opy_(obj, bstack1l1lllll1l1_opy_[bstack1ll1111llll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1lll1_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨ቎")):
            keys = getattr(obj, bstack1l1lll1_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢ቏"), [])
        elif hasattr(obj, bstack1l1lll1_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢቐ")):
            keys = getattr(obj, bstack1l1lll1_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣቑ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1lll1_opy_ (u"ࠢࡠࠤቒ"))}
        if not obj and bstack1l1llll1lll_opy_ == bstack1l1lll1_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧቓ"):
            obj = {bstack1l1lll1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢቔ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1llll1l1l_opy_(key) or str(key).startswith(bstack1l1lll1_opy_ (u"ࠥࡣࠧቕ")):
            continue
        if value is not None and bstack1l1llll1l1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1ll1ll_opy_(value, bstack1l1llll11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1ll1ll_opy_(o, bstack1l1llll11l1_opy_, max_depth) for o in value]))
    return result or None