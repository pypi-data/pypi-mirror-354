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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll1lll1_opy_,
    bstack1llll1lll11_opy_,
    bstack1lll11lllll_opy_,
    bstack1l111l11ll1_opy_,
    bstack1lll1l11ll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll1lll11_opy_
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l11111_opy_ import bstack11111lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1111_opy_ import bstack1lll11ll1ll_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1ll1l1l_opy_
bstack1l1lll1ll11_opy_ = bstack1l1ll1lll11_opy_()
bstack1l111l111ll_opy_ = 1.0
bstack1ll1111l11l_opy_ = bstack1l1lll1_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᑙ")
bstack1l1111l1l11_opy_ = bstack1l1lll1_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᑚ")
bstack1l1111l111l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᑛ")
bstack1l1111l1111_opy_ = bstack1l1lll1_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᑜ")
bstack1l1111l11ll_opy_ = bstack1l1lll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᑝ")
_1l1ll1l11l1_opy_ = set()
class bstack1llll1l111l_opy_(TestFramework):
    bstack1l11l1ll111_opy_ = bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᑞ")
    bstack1l11l11l11l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᑟ")
    bstack1l111l1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᑠ")
    bstack1l111lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᑡ")
    bstack1l11l1l1l1l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᑢ")
    bstack1l1111l1l1l_opy_: bool
    bstack1111l11111_opy_: bstack11111lll11_opy_  = None
    bstack1llll11l1l1_opy_ = None
    bstack1l1111llll1_opy_ = [
        bstack1ll1ll1lll1_opy_.BEFORE_ALL,
        bstack1ll1ll1lll1_opy_.AFTER_ALL,
        bstack1ll1ll1lll1_opy_.BEFORE_EACH,
        bstack1ll1ll1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1l111l_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᑣ")],
        bstack1111l11111_opy_: bstack11111lll11_opy_=None,
        bstack1llll11l1l1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l11l1l111l_opy_, bstack1111l11111_opy_)
        self.bstack1l1111l1l1l_opy_ = any(bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᑤ") in item.lower() for item in bstack1ll1l1l1111_opy_)
        self.bstack1llll11l1l1_opy_ = bstack1llll11l1l1_opy_
    def track_event(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll1lll1_opy_.TEST or test_framework_state in bstack1llll1l111l_opy_.bstack1l1111llll1_opy_:
            bstack1l11ll11111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll1lll1_opy_.NONE:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᑥ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠢࠣᑦ"))
            return
        if not self.bstack1l1111l1l1l_opy_:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᑧ") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack1l1lll1_opy_ (u"ࠤࠥᑨ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑩ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧᑪ"))
            return
        instance = self.__1l11l1ll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᑫ") + str(args) + bstack1l1lll1_opy_ (u"ࠨࠢᑬ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll1l111l_opy_.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll11lllll_opy_.PRE:
                bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1l1l111ll_opy_.value)
                name = str(EVENTS.bstack1l1l111ll_opy_.name)+bstack1l1lll1_opy_ (u"ࠢ࠻ࠤᑭ")+str(test_framework_state.name)
                TestFramework.bstack1l11l11l111_opy_(instance, name, bstack1ll1l11l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᑮ").format(e))
        try:
            if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1111ll11l_opy_) and test_hook_state == bstack1lll11lllll_opy_.PRE:
                test = bstack1llll1l111l_opy_.__1l1111l1ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑯ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠥࠦᑰ"))
            if test_framework_state == bstack1ll1ll1lll1_opy_.TEST:
                if test_hook_state == bstack1lll11lllll_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1llll111l_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1llll111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑱ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠧࠨᑲ"))
                elif test_hook_state == bstack1lll11lllll_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll11lll_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1lll11lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑳ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠢࠣᑴ"))
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG and test_hook_state == bstack1lll11lllll_opy_.POST:
                bstack1llll1l111l_opy_.__1l111l1lll1_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG_REPORT and test_hook_state == bstack1lll11lllll_opy_.POST:
                self.__1l111l11lll_opy_(instance, *args)
                self.__1l111lll111_opy_(instance)
            elif test_framework_state in bstack1llll1l111l_opy_.bstack1l1111llll1_opy_:
                self.__1l11ll111ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᑵ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠤࠥᑶ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111ll1111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll1l111l_opy_.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll11lllll_opy_.POST:
                name = str(EVENTS.bstack1l1l111ll_opy_.name)+bstack1l1lll1_opy_ (u"ࠥ࠾ࠧᑷ")+str(test_framework_state.name)
                bstack1ll1l11l111_opy_ = TestFramework.bstack1l11l11lll1_opy_(instance, name)
                bstack1lll11l11l1_opy_.end(EVENTS.bstack1l1l111ll_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᑸ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᑹ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᑺ").format(e))
    def bstack1l1lll1llll_opy_(self):
        return self.bstack1l1111l1l1l_opy_
    def __1l11l1l1111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1lll1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᑻ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll11ll1l_opy_(rep, [bstack1l1lll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᑼ"), bstack1l1lll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑽ"), bstack1l1lll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᑾ"), bstack1l1lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑿ"), bstack1l1lll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᒀ"), bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᒁ")])
        return None
    def __1l111l11lll_opy_(self, instance: bstack1llll1lll11_opy_, *args):
        result = self.__1l11l1l1111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l111l1_opy_ = None
        if result.get(bstack1l1lll1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᒂ"), None) == bstack1l1lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᒃ") and len(args) > 1 and getattr(args[1], bstack1l1lll1_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᒄ"), None) is not None:
            failure = [{bstack1l1lll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᒅ"): [args[1].excinfo.exconly(), result.get(bstack1l1lll1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᒆ"), None)]}]
            bstack1111l111l1_opy_ = bstack1l1lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᒇ") if bstack1l1lll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᒈ") in getattr(args[1].excinfo, bstack1l1lll1_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᒉ"), bstack1l1lll1_opy_ (u"ࠣࠤᒊ")) else bstack1l1lll1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᒋ")
        bstack1l11l1l11l1_opy_ = result.get(bstack1l1lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᒌ"), TestFramework.bstack1l11l1llll1_opy_)
        if bstack1l11l1l11l1_opy_ != TestFramework.bstack1l11l1llll1_opy_:
            TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1lll111ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111l1ll11_opy_(instance, {
            TestFramework.bstack1l1l1l1l111_opy_: failure,
            TestFramework.bstack1l11l11l1l1_opy_: bstack1111l111l1_opy_,
            TestFramework.bstack1l1l1l1l11l_opy_: bstack1l11l1l11l1_opy_,
        })
    def __1l11l1ll1ll_opy_(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll1lll1_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1111lll11_opy_ bstack1l11ll1111l_opy_ this to be bstack1l1lll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᒍ")
            if test_framework_state == bstack1ll1ll1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l1111l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1lll1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᒎ"), None), bstack1l1lll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒏ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1lll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᒐ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack111111l11l_opy_(target) if target else None
        return instance
    def __1l11ll111ll_opy_(
        self,
        instance: bstack1llll1lll11_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l1llll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1llll1l111l_opy_.bstack1l11l11l11l_opy_, {})
        if not key in bstack1l111l1llll_opy_:
            bstack1l111l1llll_opy_[key] = []
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1llll1l111l_opy_.bstack1l111l1l1l1_opy_, {})
        if not key in bstack1l111ll1l11_opy_:
            bstack1l111ll1l11_opy_[key] = []
        bstack1l111llllll_opy_ = {
            bstack1llll1l111l_opy_.bstack1l11l11l11l_opy_: bstack1l111l1llll_opy_,
            bstack1llll1l111l_opy_.bstack1l111l1l1l1_opy_: bstack1l111ll1l11_opy_,
        }
        if test_hook_state == bstack1lll11lllll_opy_.PRE:
            hook = {
                bstack1l1lll1_opy_ (u"ࠣ࡭ࡨࡽࠧᒑ"): key,
                TestFramework.bstack1l111ll111l_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1l11_opy_: TestFramework.bstack1l111ll11ll_opy_,
                TestFramework.bstack1l111l11l11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l11llll_opy_: [],
                TestFramework.bstack1l1111ll1l1_opy_: args[1] if len(args) > 1 else bstack1l1lll1_opy_ (u"ࠩࠪᒒ"),
                TestFramework.bstack1l11l1lll1l_opy_: bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()
            }
            bstack1l111l1llll_opy_[key].append(hook)
            bstack1l111llllll_opy_[bstack1llll1l111l_opy_.bstack1l111lll1l1_opy_] = key
        elif test_hook_state == bstack1lll11lllll_opy_.POST:
            bstack1l11l11l1ll_opy_ = bstack1l111l1llll_opy_.get(key, [])
            hook = bstack1l11l11l1ll_opy_.pop() if bstack1l11l11l1ll_opy_ else None
            if hook:
                result = self.__1l11l1l1111_opy_(*args)
                if result:
                    bstack1l11l111l1l_opy_ = result.get(bstack1l1lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᒓ"), TestFramework.bstack1l111ll11ll_opy_)
                    if bstack1l11l111l1l_opy_ != TestFramework.bstack1l111ll11ll_opy_:
                        hook[TestFramework.bstack1l11l1l1l11_opy_] = bstack1l11l111l1l_opy_
                hook[TestFramework.bstack1l111llll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1lll1l_opy_]= bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()
                self.bstack1l1111ll1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1111l_opy_, [])
                if logs: self.bstack1l1lllll11l_opy_(instance, logs)
                bstack1l111ll1l11_opy_[key].append(hook)
                bstack1l111llllll_opy_[bstack1llll1l111l_opy_.bstack1l11l1l1l1l_opy_] = key
        TestFramework.bstack1l111l1ll11_opy_(instance, bstack1l111llllll_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᒔ") + str(bstack1l111ll1l11_opy_) + bstack1l1lll1_opy_ (u"ࠧࠨᒕ"))
    def __1l1111l1lll_opy_(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll11ll1l_opy_(args[0], [bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒖ"), bstack1l1lll1_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᒗ"), bstack1l1lll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᒘ"), bstack1l1lll1_opy_ (u"ࠤ࡬ࡨࡸࠨᒙ"), bstack1l1lll1_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᒚ"), bstack1l1lll1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᒛ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒜ")) else fixturedef.get(bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒝ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1lll1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᒞ")) else None
        node = request.node if hasattr(request, bstack1l1lll1_opy_ (u"ࠣࡰࡲࡨࡪࠨᒟ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1lll1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᒠ")) else None
        baseid = fixturedef.get(bstack1l1lll1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᒡ"), None) or bstack1l1lll1_opy_ (u"ࠦࠧᒢ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1lll1_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᒣ")):
            target = bstack1llll1l111l_opy_.__1l111llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᒤ")) else None
            if target and not TestFramework.bstack111111l11l_opy_(target):
                self.__1l11l1111l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᒥ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠣࠤᒦ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᒧ") + str(target) + bstack1l1lll1_opy_ (u"ࠥࠦᒨ"))
            return None
        instance = TestFramework.bstack111111l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᒩ") + str(target) + bstack1l1lll1_opy_ (u"ࠧࠨᒪ"))
            return None
        bstack1l11l1111ll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1llll1l111l_opy_.bstack1l11l1ll111_opy_, {})
        if os.getenv(bstack1l1lll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᒫ"), bstack1l1lll1_opy_ (u"ࠢ࠲ࠤᒬ")) == bstack1l1lll1_opy_ (u"ࠣ࠳ࠥᒭ"):
            bstack1l11l1lllll_opy_ = bstack1l1lll1_opy_ (u"ࠤ࠽ࠦᒮ").join((scope, fixturename))
            bstack1l111l1ll1l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l11ll11_opy_ = {
                bstack1l1lll1_opy_ (u"ࠥ࡯ࡪࡿࠢᒯ"): bstack1l11l1lllll_opy_,
                bstack1l1lll1_opy_ (u"ࠦࡹࡧࡧࡴࠤᒰ"): bstack1llll1l111l_opy_.__1l11l1ll11l_opy_(request.node),
                bstack1l1lll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᒱ"): fixturedef,
                bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒲ"): scope,
                bstack1l1lll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᒳ"): None,
            }
            try:
                if test_hook_state == bstack1lll11lllll_opy_.POST and callable(getattr(args[-1], bstack1l1lll1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᒴ"), None)):
                    bstack1l11l11ll11_opy_[bstack1l1lll1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᒵ")] = TestFramework.bstack1l1ll1l1lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll11lllll_opy_.PRE:
                bstack1l11l11ll11_opy_[bstack1l1lll1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᒶ")] = uuid4().__str__()
                bstack1l11l11ll11_opy_[bstack1llll1l111l_opy_.bstack1l111l11l11_opy_] = bstack1l111l1ll1l_opy_
            elif test_hook_state == bstack1lll11lllll_opy_.POST:
                bstack1l11l11ll11_opy_[bstack1llll1l111l_opy_.bstack1l111llll11_opy_] = bstack1l111l1ll1l_opy_
            if bstack1l11l1lllll_opy_ in bstack1l11l1111ll_opy_:
                bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_].update(bstack1l11l11ll11_opy_)
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᒷ") + str(bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_]) + bstack1l1lll1_opy_ (u"ࠧࠨᒸ"))
            else:
                bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_] = bstack1l11l11ll11_opy_
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᒹ") + str(len(bstack1l11l1111ll_opy_)) + bstack1l1lll1_opy_ (u"ࠢࠣᒺ"))
        TestFramework.bstack1111111lll_opy_(instance, bstack1llll1l111l_opy_.bstack1l11l1ll111_opy_, bstack1l11l1111ll_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒻ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠤࠥᒼ"))
        return instance
    def __1l11l1111l1_opy_(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll1lll1_opy_.create_context(target)
        ob = bstack1llll1lll11_opy_(ctx, self.bstack1ll1l1l1111_opy_, self.bstack1l11l1l111l_opy_, test_framework_state)
        TestFramework.bstack1l111l1ll11_opy_(ob, {
            TestFramework.bstack1ll11llllll_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1ll1l1_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1l1ll_opy_: [],
            bstack1llll1l111l_opy_.bstack1l11l1ll111_opy_: {},
            bstack1llll1l111l_opy_.bstack1l111l1l1l1_opy_: {},
            bstack1llll1l111l_opy_.bstack1l11l11l11l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1l11l1lll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1ll1l1lllll_opy_, context.platform_index)
        TestFramework.bstack1lllllll11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᒽ") + str(TestFramework.bstack1lllllll11l_opy_.keys()) + bstack1l1lll1_opy_ (u"ࠦࠧᒾ"))
        return ob
    def bstack1l1llllll1l_opy_(self, instance: bstack1llll1lll11_opy_, bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_]):
        bstack1l11l1l1ll1_opy_ = (
            bstack1llll1l111l_opy_.bstack1l111lll1l1_opy_
            if bstack1llllll1l11_opy_[1] == bstack1lll11lllll_opy_.PRE
            else bstack1llll1l111l_opy_.bstack1l11l1l1l1l_opy_
        )
        hook = bstack1llll1l111l_opy_.bstack1l111l11111_opy_(instance, bstack1l11l1l1ll1_opy_)
        entries = hook.get(TestFramework.bstack1l11l11llll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []))
        return entries
    def bstack1ll1111111l_opy_(self, instance: bstack1llll1lll11_opy_, bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_]):
        bstack1l11l1l1ll1_opy_ = (
            bstack1llll1l111l_opy_.bstack1l111lll1l1_opy_
            if bstack1llllll1l11_opy_[1] == bstack1lll11lllll_opy_.PRE
            else bstack1llll1l111l_opy_.bstack1l11l1l1l1l_opy_
        )
        bstack1llll1l111l_opy_.bstack1l1111ll111_opy_(instance, bstack1l11l1l1ll1_opy_)
        TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []).clear()
    def bstack1l1111ll1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒿ")
        global _1l1ll1l11l1_opy_
        platform_index = os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᓀ")]
        bstack1l1llllllll_opy_ = os.path.join(bstack1l1lll1ll11_opy_, (bstack1ll1111l11l_opy_ + str(platform_index)), bstack1l1111l1111_opy_)
        if not os.path.exists(bstack1l1llllllll_opy_) or not os.path.isdir(bstack1l1llllllll_opy_):
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᓁ").format(bstack1l1llllllll_opy_))
            return
        logs = hook.get(bstack1l1lll1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᓂ"), [])
        with os.scandir(bstack1l1llllllll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l11l1_opy_:
                    self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᓃ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1lll1_opy_ (u"ࠥࠦᓄ")
                    log_entry = bstack1lll1l11ll1_opy_(
                        kind=bstack1l1lll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᓅ"),
                        message=bstack1l1lll1_opy_ (u"ࠧࠨᓆ"),
                        level=bstack1l1lll1_opy_ (u"ࠨࠢᓇ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1lllll_opy_=entry.stat().st_size,
                        bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᓈ"),
                        bstack1l1111l_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l11ll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l11l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᓉ")]
        bstack1l11ll11l1l_opy_ = os.path.join(bstack1l1lll1ll11_opy_, (bstack1ll1111l11l_opy_ + str(platform_index)), bstack1l1111l1111_opy_, bstack1l1111l11ll_opy_)
        if not os.path.exists(bstack1l11ll11l1l_opy_) or not os.path.isdir(bstack1l11ll11l1l_opy_):
            self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᓊ").format(bstack1l11ll11l1l_opy_))
        else:
            self.logger.info(bstack1l1lll1_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᓋ").format(bstack1l11ll11l1l_opy_))
            with os.scandir(bstack1l11ll11l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l11l1_opy_:
                        self.logger.info(bstack1l1lll1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᓌ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1lll1_opy_ (u"ࠧࠨᓍ")
                        log_entry = bstack1lll1l11ll1_opy_(
                            kind=bstack1l1lll1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᓎ"),
                            message=bstack1l1lll1_opy_ (u"ࠢࠣᓏ"),
                            level=bstack1l1lll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᓐ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1lllll_opy_=entry.stat().st_size,
                            bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᓑ"),
                            bstack1l1111l_opy_=os.path.abspath(entry.path),
                            bstack1l1lllll1ll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l11l1_opy_.add(abs_path)
        hook[bstack1l1lll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᓒ")] = logs
    def bstack1l1lllll11l_opy_(
        self,
        bstack1l1lll1l111_opy_: bstack1llll1lll11_opy_,
        entries: List[bstack1lll1l11ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᓓ"))
        req.platform_index = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1ll1l1lllll_opy_)
        req.execution_context.hash = str(bstack1l1lll1l111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1ll11llllll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllllll11_opy_(bstack1l1lll1l111_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.uuid = entry.bstack1l11l1l11ll_opy_
            log_entry.test_framework_state = bstack1l1lll1l111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1lll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᓔ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1lll1_opy_ (u"ࠨࠢᓕ")
            if entry.kind == bstack1l1lll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᓖ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1lllll_opy_
                log_entry.file_path = entry.bstack1l1111l_opy_
        def bstack1ll11111ll1_opy_():
            bstack11lll1ll1_opy_ = datetime.now()
            try:
                self.bstack1llll11l1l1_opy_.LogCreatedEvent(req)
                bstack1l1lll1l111_opy_.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᓗ"), datetime.now() - bstack11lll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᓘ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l11111_opy_.enqueue(bstack1ll11111ll1_opy_)
    def __1l111lll111_opy_(self, instance) -> None:
        bstack1l1lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᓙ")
        bstack1l111llllll_opy_ = {bstack1l1lll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᓚ"): bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l111l1ll11_opy_(instance, bstack1l111llllll_opy_)
    @staticmethod
    def bstack1l111l11111_opy_(instance: bstack1llll1lll11_opy_, bstack1l11l1l1ll1_opy_: str):
        bstack1l11l11ll1l_opy_ = (
            bstack1llll1l111l_opy_.bstack1l111l1l1l1_opy_
            if bstack1l11l1l1ll1_opy_ == bstack1llll1l111l_opy_.bstack1l11l1l1l1l_opy_
            else bstack1llll1l111l_opy_.bstack1l11l11l11l_opy_
        )
        bstack1l11ll11l11_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1l11l1l1ll1_opy_, None)
        bstack1l11l111lll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1l11l11ll1l_opy_, None) if bstack1l11ll11l11_opy_ else None
        return (
            bstack1l11l111lll_opy_[bstack1l11ll11l11_opy_][-1]
            if isinstance(bstack1l11l111lll_opy_, dict) and len(bstack1l11l111lll_opy_.get(bstack1l11ll11l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1111ll111_opy_(instance: bstack1llll1lll11_opy_, bstack1l11l1l1ll1_opy_: str):
        hook = bstack1llll1l111l_opy_.bstack1l111l11111_opy_(instance, bstack1l11l1l1ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l11llll_opy_, []).clear()
    @staticmethod
    def __1l111l1lll1_opy_(instance: bstack1llll1lll11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1lll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᓛ"), None)):
            return
        if os.getenv(bstack1l1lll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᓜ"), bstack1l1lll1_opy_ (u"ࠢ࠲ࠤᓝ")) != bstack1l1lll1_opy_ (u"ࠣ࠳ࠥᓞ"):
            bstack1llll1l111l_opy_.logger.warning(bstack1l1lll1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᓟ"))
            return
        bstack1l11ll111l1_opy_ = {
            bstack1l1lll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᓠ"): (bstack1llll1l111l_opy_.bstack1l111lll1l1_opy_, bstack1llll1l111l_opy_.bstack1l11l11l11l_opy_),
            bstack1l1lll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓡ"): (bstack1llll1l111l_opy_.bstack1l11l1l1l1l_opy_, bstack1llll1l111l_opy_.bstack1l111l1l1l1_opy_),
        }
        for when in (bstack1l1lll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓢ"), bstack1l1lll1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᓣ"), bstack1l1lll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓤ")):
            bstack1l1111lll1l_opy_ = args[1].get_records(when)
            if not bstack1l1111lll1l_opy_:
                continue
            records = [
                bstack1lll1l11ll1_opy_(
                    kind=TestFramework.bstack1l1lll1l1l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1lll1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᓥ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1lll1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᓦ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1111lll1l_opy_
                if isinstance(getattr(r, bstack1l1lll1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᓧ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l1ll1l1_opy_, bstack1l11l11ll1l_opy_ = bstack1l11ll111l1_opy_.get(when, (None, None))
            bstack1l11l1l1lll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1l11l1ll1l1_opy_, None) if bstack1l11l1ll1l1_opy_ else None
            bstack1l11l111lll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, bstack1l11l11ll1l_opy_, None) if bstack1l11l1l1lll_opy_ else None
            if isinstance(bstack1l11l111lll_opy_, dict) and len(bstack1l11l111lll_opy_.get(bstack1l11l1l1lll_opy_, [])) > 0:
                hook = bstack1l11l111lll_opy_[bstack1l11l1l1lll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l11llll_opy_ in hook:
                    hook[TestFramework.bstack1l11l11llll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1111l1ll1_opy_(test) -> Dict[str, Any]:
        bstack11lll111_opy_ = bstack1llll1l111l_opy_.__1l111llll1l_opy_(test.location) if hasattr(test, bstack1l1lll1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᓨ")) else getattr(test, bstack1l1lll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᓩ"), None)
        test_name = test.name if hasattr(test, bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓪ")) else None
        bstack1l111lllll1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1lll1_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢᓫ")) and test.fspath else None
        if not bstack11lll111_opy_ or not test_name or not bstack1l111lllll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1lll1_opy_ (u"ࠣࡱࡥ࡮ࠧᓬ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l11111llll_opy_ = []
        try:
            bstack1l11111llll_opy_ = bstack11l1ll1l1l_opy_.bstack111l11l1ll_opy_(test)
        except:
            bstack1llll1l111l_opy_.logger.warning(bstack1l1lll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳ࠭ࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡨࡷࡴࡲࡶࡦࡦࠣ࡭ࡳࠦࡃࡍࡋࠥᓭ"))
        return {
            TestFramework.bstack1ll1l11l11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111ll11l_opy_: bstack11lll111_opy_,
            TestFramework.bstack1ll11l1llll_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: getattr(test, bstack1l1lll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᓮ"), None),
            TestFramework.bstack1l11l111ll1_opy_: bstack1l111lllll1_opy_,
            TestFramework.bstack1l111ll11l1_opy_: bstack1llll1l111l_opy_.__1l11l1ll11l_opy_(test),
            TestFramework.bstack1l11l111l11_opy_: code,
            TestFramework.bstack1l1l1l1l11l_opy_: TestFramework.bstack1l11l1llll1_opy_,
            TestFramework.bstack1l11lll1ll1_opy_: bstack11lll111_opy_,
            TestFramework.bstack1l1111l11l1_opy_: bstack1l11111llll_opy_
        }
    @staticmethod
    def __1l11l1ll11l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1lll1_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᓯ"), [])
            markers.extend([getattr(m, bstack1l1lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᓰ"), None) for m in own_markers if getattr(m, bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓱ"), None)])
            current = getattr(current, bstack1l1lll1_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᓲ"), None)
        return markers
    @staticmethod
    def __1l111llll1l_opy_(location):
        return bstack1l1lll1_opy_ (u"ࠣ࠼࠽ࠦᓳ").join(filter(lambda x: isinstance(x, str), location))