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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll1lll1_opy_,
    bstack1llll1lll11_opy_,
    bstack1lll11lllll_opy_,
    bstack1l111l11ll1_opy_,
    bstack1lll1l11ll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll1lll11_opy_
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1111_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111l11111_opy_ import bstack11111lll11_opy_
bstack1l1lll1ll11_opy_ = bstack1l1ll1lll11_opy_()
bstack1ll1111l11l_opy_ = bstack1l1lll1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᎥ")
bstack1l111l111l1_opy_ = bstack1l1lll1_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᎦ")
bstack1l111lll1ll_opy_ = bstack1l1lll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᎧ")
bstack1l111l111ll_opy_ = 1.0
_1l1ll1l11l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1ll111_opy_ = bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᎨ")
    bstack1l11l11l11l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᎩ")
    bstack1l111l1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᎪ")
    bstack1l111lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᎫ")
    bstack1l11l1l1l1l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᎬ")
    bstack1l1111l1l1l_opy_: bool
    bstack1111l11111_opy_: bstack11111lll11_opy_  = None
    bstack1l1111llll1_opy_ = [
        bstack1ll1ll1lll1_opy_.BEFORE_ALL,
        bstack1ll1ll1lll1_opy_.AFTER_ALL,
        bstack1ll1ll1lll1_opy_.BEFORE_EACH,
        bstack1ll1ll1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1l111l_opy_: Dict[str, str],
        bstack1ll1l1l1111_opy_: List[str]=[bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᎭ")],
        bstack1111l11111_opy_: bstack11111lll11_opy_ = None,
        bstack1llll11l1l1_opy_=None
    ):
        super().__init__(bstack1ll1l1l1111_opy_, bstack1l11l1l111l_opy_, bstack1111l11111_opy_)
        self.bstack1l1111l1l1l_opy_ = any(bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᎮ") in item.lower() for item in bstack1ll1l1l1111_opy_)
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
        if test_framework_state == bstack1ll1ll1lll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_:
            bstack1l11ll11111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll1lll1_opy_.NONE:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᎯ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠢࠣᎰ"))
            return
        if not self.bstack1l1111l1l1l_opy_:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᎱ") + str(str(self.bstack1ll1l1l1111_opy_)) + bstack1l1lll1_opy_ (u"ࠤࠥᎲ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᎳ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠦࠧᎴ"))
            return
        instance = self.__1l11l1ll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᎵ") + str(args) + bstack1l1lll1_opy_ (u"ࠨࠢᎶ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll11lllll_opy_.PRE:
                bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1l1l111ll_opy_.value)
                name = str(EVENTS.bstack1l1l111ll_opy_.name)+bstack1l1lll1_opy_ (u"ࠢ࠻ࠤᎷ")+str(test_framework_state.name)
                TestFramework.bstack1l11l11l111_opy_(instance, name, bstack1ll1l11l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᎸ").format(e))
        try:
            if test_framework_state == bstack1ll1ll1lll1_opy_.TEST:
                if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1111ll11l_opy_) and test_hook_state == bstack1lll11lllll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1111l1ll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1lll1_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᎹ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠥࠦᎺ"))
                if test_hook_state == bstack1lll11lllll_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1llll111l_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1llll111l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l111l1l111_opy_(instance, args)
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᎻ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠧࠨᎼ"))
                elif test_hook_state == bstack1lll11lllll_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lll11lll_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1lll11lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᎽ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠢࠣᎾ"))
            elif test_framework_state == bstack1ll1ll1lll1_opy_.STEP:
                if test_hook_state == bstack1lll11lllll_opy_.PRE:
                    PytestBDDFramework.__1l11l111111_opy_(instance, args)
                elif test_hook_state == bstack1lll11lllll_opy_.POST:
                    PytestBDDFramework.__1l111ll1l1l_opy_(instance, args)
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG and test_hook_state == bstack1lll11lllll_opy_.POST:
                PytestBDDFramework.__1l111l1lll1_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG_REPORT and test_hook_state == bstack1lll11lllll_opy_.POST:
                self.__1l111l11lll_opy_(instance, *args)
                self.__1l111lll111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_:
                self.__1l11ll111ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᎿ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠤࠥᏀ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111ll1111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll11lllll_opy_.POST:
                name = str(EVENTS.bstack1l1l111ll_opy_.name)+bstack1l1lll1_opy_ (u"ࠥ࠾ࠧᏁ")+str(test_framework_state.name)
                bstack1ll1l11l111_opy_ = TestFramework.bstack1l11l11lll1_opy_(instance, name)
                bstack1lll11l11l1_opy_.end(EVENTS.bstack1l1l111ll_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᏂ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᏃ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᏄ").format(e))
    def bstack1l1lll1llll_opy_(self):
        return self.bstack1l1111l1l1l_opy_
    def __1l11l1l1111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1lll1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᏅ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll11ll1l_opy_(rep, [bstack1l1lll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᏆ"), bstack1l1lll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᏇ"), bstack1l1lll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᏈ"), bstack1l1lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᏉ"), bstack1l1lll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᏊ"), bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᏋ")])
        return None
    def __1l111l11lll_opy_(self, instance: bstack1llll1lll11_opy_, *args):
        result = self.__1l11l1l1111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l111l1_opy_ = None
        if result.get(bstack1l1lll1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᏌ"), None) == bstack1l1lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᏍ") and len(args) > 1 and getattr(args[1], bstack1l1lll1_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᏎ"), None) is not None:
            failure = [{bstack1l1lll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭Ꮟ"): [args[1].excinfo.exconly(), result.get(bstack1l1lll1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᏐ"), None)]}]
            bstack1111l111l1_opy_ = bstack1l1lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᏑ") if bstack1l1lll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᏒ") in getattr(args[1].excinfo, bstack1l1lll1_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᏓ"), bstack1l1lll1_opy_ (u"ࠣࠤᏔ")) else bstack1l1lll1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᏕ")
        bstack1l11l1l11l1_opy_ = result.get(bstack1l1lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᏖ"), TestFramework.bstack1l11l1llll1_opy_)
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
            target = None # bstack1l1111lll11_opy_ bstack1l11ll1111l_opy_ this to be bstack1l1lll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᏗ")
            if test_framework_state == bstack1ll1ll1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l1111l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1lll1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᏘ"), None), bstack1l1lll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᏙ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1lll1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᏚ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1lll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᏛ"), None):
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
        bstack1l111l1llll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, PytestBDDFramework.bstack1l11l11l11l_opy_, {})
        if not key in bstack1l111l1llll_opy_:
            bstack1l111l1llll_opy_[key] = []
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllllll11_opy_(instance, PytestBDDFramework.bstack1l111l1l1l1_opy_, {})
        if not key in bstack1l111ll1l11_opy_:
            bstack1l111ll1l11_opy_[key] = []
        bstack1l111llllll_opy_ = {
            PytestBDDFramework.bstack1l11l11l11l_opy_: bstack1l111l1llll_opy_,
            PytestBDDFramework.bstack1l111l1l1l1_opy_: bstack1l111ll1l11_opy_,
        }
        if test_hook_state == bstack1lll11lllll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1lll1_opy_ (u"ࠤ࡮ࡩࡾࠨᏜ"): key,
                TestFramework.bstack1l111ll111l_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1l11_opy_: TestFramework.bstack1l111ll11ll_opy_,
                TestFramework.bstack1l111l11l11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l11llll_opy_: [],
                TestFramework.bstack1l1111ll1l1_opy_: hook_name,
                TestFramework.bstack1l11l1lll1l_opy_: bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()
            }
            bstack1l111l1llll_opy_[key].append(hook)
            bstack1l111llllll_opy_[PytestBDDFramework.bstack1l111lll1l1_opy_] = key
        elif test_hook_state == bstack1lll11lllll_opy_.POST:
            bstack1l11l11l1ll_opy_ = bstack1l111l1llll_opy_.get(key, [])
            hook = bstack1l11l11l1ll_opy_.pop() if bstack1l11l11l1ll_opy_ else None
            if hook:
                result = self.__1l11l1l1111_opy_(*args)
                if result:
                    bstack1l11l111l1l_opy_ = result.get(bstack1l1lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᏝ"), TestFramework.bstack1l111ll11ll_opy_)
                    if bstack1l11l111l1l_opy_ != TestFramework.bstack1l111ll11ll_opy_:
                        hook[TestFramework.bstack1l11l1l1l11_opy_] = bstack1l11l111l1l_opy_
                hook[TestFramework.bstack1l111llll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1lll1l_opy_] = bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()
                self.bstack1l1111ll1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1111l_opy_, [])
                self.bstack1l1lllll11l_opy_(instance, logs)
                bstack1l111ll1l11_opy_[key].append(hook)
                bstack1l111llllll_opy_[PytestBDDFramework.bstack1l11l1l1l1l_opy_] = key
        TestFramework.bstack1l111l1ll11_opy_(instance, bstack1l111llllll_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᏞ") + str(bstack1l111ll1l11_opy_) + bstack1l1lll1_opy_ (u"ࠧࠨᏟ"))
    def __1l1111l1lll_opy_(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll11ll1l_opy_(args[0], [bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏠ"), bstack1l1lll1_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᏡ"), bstack1l1lll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᏢ"), bstack1l1lll1_opy_ (u"ࠤ࡬ࡨࡸࠨᏣ"), bstack1l1lll1_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᏤ"), bstack1l1lll1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᏥ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᏦ")) else fixturedef.get(bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏧ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1lll1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᏨ")) else None
        node = request.node if hasattr(request, bstack1l1lll1_opy_ (u"ࠣࡰࡲࡨࡪࠨᏩ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1lll1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏪ")) else None
        baseid = fixturedef.get(bstack1l1lll1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᏫ"), None) or bstack1l1lll1_opy_ (u"ࠦࠧᏬ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1lll1_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᏭ")):
            target = PytestBDDFramework.__1l111llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᏮ")) else None
            if target and not TestFramework.bstack111111l11l_opy_(target):
                self.__1l11l1111l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᏯ") + str(test_hook_state) + bstack1l1lll1_opy_ (u"ࠣࠤᏰ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᏱ") + str(target) + bstack1l1lll1_opy_ (u"ࠥࠦᏲ"))
            return None
        instance = TestFramework.bstack111111l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᏳ") + str(target) + bstack1l1lll1_opy_ (u"ࠧࠨᏴ"))
            return None
        bstack1l11l1111ll_opy_ = TestFramework.bstack1llllllll11_opy_(instance, PytestBDDFramework.bstack1l11l1ll111_opy_, {})
        if os.getenv(bstack1l1lll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᏵ"), bstack1l1lll1_opy_ (u"ࠢ࠲ࠤ᏶")) == bstack1l1lll1_opy_ (u"ࠣ࠳ࠥ᏷"):
            bstack1l11l1lllll_opy_ = bstack1l1lll1_opy_ (u"ࠤ࠽ࠦᏸ").join((scope, fixturename))
            bstack1l111l1ll1l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l11ll11_opy_ = {
                bstack1l1lll1_opy_ (u"ࠥ࡯ࡪࡿࠢᏹ"): bstack1l11l1lllll_opy_,
                bstack1l1lll1_opy_ (u"ࠦࡹࡧࡧࡴࠤᏺ"): PytestBDDFramework.__1l11l1ll11l_opy_(request.node, scenario),
                bstack1l1lll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᏻ"): fixturedef,
                bstack1l1lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏼ"): scope,
                bstack1l1lll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᏽ"): None,
            }
            try:
                if test_hook_state == bstack1lll11lllll_opy_.POST and callable(getattr(args[-1], bstack1l1lll1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧ᏾"), None)):
                    bstack1l11l11ll11_opy_[bstack1l1lll1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᏿")] = TestFramework.bstack1l1ll1l1lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll11lllll_opy_.PRE:
                bstack1l11l11ll11_opy_[bstack1l1lll1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ᐀")] = uuid4().__str__()
                bstack1l11l11ll11_opy_[PytestBDDFramework.bstack1l111l11l11_opy_] = bstack1l111l1ll1l_opy_
            elif test_hook_state == bstack1lll11lllll_opy_.POST:
                bstack1l11l11ll11_opy_[PytestBDDFramework.bstack1l111llll11_opy_] = bstack1l111l1ll1l_opy_
            if bstack1l11l1lllll_opy_ in bstack1l11l1111ll_opy_:
                bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_].update(bstack1l11l11ll11_opy_)
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᐁ") + str(bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_]) + bstack1l1lll1_opy_ (u"ࠧࠨᐂ"))
            else:
                bstack1l11l1111ll_opy_[bstack1l11l1lllll_opy_] = bstack1l11l11ll11_opy_
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᐃ") + str(len(bstack1l11l1111ll_opy_)) + bstack1l1lll1_opy_ (u"ࠢࠣᐄ"))
        TestFramework.bstack1111111lll_opy_(instance, PytestBDDFramework.bstack1l11l1ll111_opy_, bstack1l11l1111ll_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᐅ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠤࠥᐆ"))
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
            PytestBDDFramework.bstack1l11l1ll111_opy_: {},
            PytestBDDFramework.bstack1l111l1l1l1_opy_: {},
            PytestBDDFramework.bstack1l11l11l11l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1l11l1lll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1ll1l1lllll_opy_, context.platform_index)
        TestFramework.bstack1lllllll11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᐇ") + str(TestFramework.bstack1lllllll11l_opy_.keys()) + bstack1l1lll1_opy_ (u"ࠦࠧᐈ"))
        return ob
    @staticmethod
    def __1l111l1l111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1lll1_opy_ (u"ࠬ࡯ࡤࠨᐉ"): id(step),
                bstack1l1lll1_opy_ (u"࠭ࡴࡦࡺࡷࠫᐊ"): step.name,
                bstack1l1lll1_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᐋ"): step.keyword,
            })
        meta = {
            bstack1l1lll1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᐌ"): {
                bstack1l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐍ"): feature.name,
                bstack1l1lll1_opy_ (u"ࠪࡴࡦࡺࡨࠨᐎ"): feature.filename,
                bstack1l1lll1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᐏ"): feature.description
            },
            bstack1l1lll1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᐐ"): {
                bstack1l1lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᐑ"): scenario.name
            },
            bstack1l1lll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐒ"): steps,
            bstack1l1lll1_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᐓ"): PytestBDDFramework.__1l111ll1ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l11l1l_opy_: meta
            }
        )
    def bstack1l1111ll1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᐔ")
        global _1l1ll1l11l1_opy_
        platform_index = os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᐕ")]
        bstack1l1llllllll_opy_ = os.path.join(bstack1l1lll1ll11_opy_, (bstack1ll1111l11l_opy_ + str(platform_index)), bstack1l111l111l1_opy_)
        if not os.path.exists(bstack1l1llllllll_opy_) or not os.path.isdir(bstack1l1llllllll_opy_):
            return
        logs = hook.get(bstack1l1lll1_opy_ (u"ࠦࡱࡵࡧࡴࠤᐖ"), [])
        with os.scandir(bstack1l1llllllll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l11l1_opy_:
                    self.logger.info(bstack1l1lll1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᐗ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1lll1_opy_ (u"ࠨࠢᐘ")
                    log_entry = bstack1lll1l11ll1_opy_(
                        kind=bstack1l1lll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᐙ"),
                        message=bstack1l1lll1_opy_ (u"ࠣࠤᐚ"),
                        level=bstack1l1lll1_opy_ (u"ࠤࠥᐛ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1lllll_opy_=entry.stat().st_size,
                        bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᐜ"),
                        bstack1l1111l_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l11ll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l11l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐝ")]
        bstack1l11ll11l1l_opy_ = os.path.join(bstack1l1lll1ll11_opy_, (bstack1ll1111l11l_opy_ + str(platform_index)), bstack1l111l111l1_opy_, bstack1l111lll1ll_opy_)
        if not os.path.exists(bstack1l11ll11l1l_opy_) or not os.path.isdir(bstack1l11ll11l1l_opy_):
            self.logger.info(bstack1l1lll1_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᐞ").format(bstack1l11ll11l1l_opy_))
        else:
            self.logger.info(bstack1l1lll1_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᐟ").format(bstack1l11ll11l1l_opy_))
            with os.scandir(bstack1l11ll11l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l11l1_opy_:
                        self.logger.info(bstack1l1lll1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᐠ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1lll1_opy_ (u"ࠣࠤᐡ")
                        log_entry = bstack1lll1l11ll1_opy_(
                            kind=bstack1l1lll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᐢ"),
                            message=bstack1l1lll1_opy_ (u"ࠥࠦᐣ"),
                            level=bstack1l1lll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᐤ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1lllll_opy_=entry.stat().st_size,
                            bstack1l1lll11111_opy_=bstack1l1lll1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᐥ"),
                            bstack1l1111l_opy_=os.path.abspath(entry.path),
                            bstack1l1lllll1ll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l11l1_opy_.add(abs_path)
        hook[bstack1l1lll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᐦ")] = logs
    def bstack1l1lllll11l_opy_(
        self,
        bstack1l1lll1l111_opy_: bstack1llll1lll11_opy_,
        entries: List[bstack1lll1l11ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᐧ"))
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
            log_entry.message = entry.message.encode(bstack1l1lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᐨ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1lll1_opy_ (u"ࠤࠥᐩ")
            if entry.kind == bstack1l1lll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᐪ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1lllll_opy_
                log_entry.file_path = entry.bstack1l1111l_opy_
        def bstack1ll11111ll1_opy_():
            bstack11lll1ll1_opy_ = datetime.now()
            try:
                self.bstack1llll11l1l1_opy_.LogCreatedEvent(req)
                bstack1l1lll1l111_opy_.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᐫ"), datetime.now() - bstack11lll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᐬ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l11111_opy_.enqueue(bstack1ll11111ll1_opy_)
    def __1l111lll111_opy_(self, instance) -> None:
        bstack1l1lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐭ")
        bstack1l111llllll_opy_ = {bstack1l1lll1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᐮ"): bstack1lll11ll1ll_opy_.bstack1l1111lllll_opy_()}
        TestFramework.bstack1l111l1ll11_opy_(instance, bstack1l111llllll_opy_)
    @staticmethod
    def __1l11l111111_opy_(instance, args):
        request, bstack1l11ll11ll1_opy_ = args
        bstack1l111ll1lll_opy_ = id(bstack1l11ll11ll1_opy_)
        bstack1l111l1l11l_opy_ = instance.data[TestFramework.bstack1l111l11l1l_opy_]
        step = next(filter(lambda st: st[bstack1l1lll1_opy_ (u"ࠨ࡫ࡧࠫᐯ")] == bstack1l111ll1lll_opy_, bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐰ")]), None)
        step.update({
            bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐱ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐲ")]) if st[bstack1l1lll1_opy_ (u"ࠬ࡯ࡤࠨᐳ")] == step[bstack1l1lll1_opy_ (u"࠭ࡩࡥࠩᐴ")]), None)
        if index is not None:
            bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐵ")][index] = step
        instance.data[TestFramework.bstack1l111l11l1l_opy_] = bstack1l111l1l11l_opy_
    @staticmethod
    def __1l111ll1l1l_opy_(instance, args):
        bstack1l1lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡨࡦࡰࠣࡰࡪࡴࠠࡢࡴࡪࡷࠥ࡯ࡳࠡ࠴࠯ࠤ࡮ࡺࠠࡴ࡫ࡪࡲ࡮࡬ࡩࡦࡵࠣࡸ࡭࡫ࡲࡦࠢ࡬ࡷࠥࡴ࡯ࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠲࡛ࠦࡳࡧࡴࡹࡪࡹࡴ࠭ࠢࡶࡸࡪࡶ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠴ࠢࡷ࡬ࡪࡴࠠࡵࡪࡨࠤࡱࡧࡳࡵࠢࡹࡥࡱࡻࡥࠡ࡫ࡶࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐶ")
        bstack1l111lll11l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11ll11ll1_opy_ = args[1]
        bstack1l111ll1lll_opy_ = id(bstack1l11ll11ll1_opy_)
        bstack1l111l1l11l_opy_ = instance.data[TestFramework.bstack1l111l11l1l_opy_]
        step = None
        if bstack1l111ll1lll_opy_ is not None and bstack1l111l1l11l_opy_.get(bstack1l1lll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐷ")):
            step = next(filter(lambda st: st[bstack1l1lll1_opy_ (u"ࠪ࡭ࡩ࠭ᐸ")] == bstack1l111ll1lll_opy_, bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐹ")]), None)
            step.update({
                bstack1l1lll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᐺ"): bstack1l111lll11l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1lll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐻ"): bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐼ"),
                bstack1l1lll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᐽ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1lll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐾ"): bstack1l1lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᐿ"),
                })
        index = next((i for i, st in enumerate(bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑀ")]) if st[bstack1l1lll1_opy_ (u"ࠬ࡯ࡤࠨᑁ")] == step[bstack1l1lll1_opy_ (u"࠭ࡩࡥࠩᑂ")]), None)
        if index is not None:
            bstack1l111l1l11l_opy_[bstack1l1lll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᑃ")][index] = step
        instance.data[TestFramework.bstack1l111l11l1l_opy_] = bstack1l111l1l11l_opy_
    @staticmethod
    def __1l111ll1ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1lll1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᑄ")):
                examples = list(node.callspec.params[bstack1l1lll1_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᑅ")].values())
            return examples
        except:
            return []
    def bstack1l1llllll1l_opy_(self, instance: bstack1llll1lll11_opy_, bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_]):
        bstack1l11l1l1ll1_opy_ = (
            PytestBDDFramework.bstack1l111lll1l1_opy_
            if bstack1llllll1l11_opy_[1] == bstack1lll11lllll_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1l1l_opy_
        )
        hook = PytestBDDFramework.bstack1l111l11111_opy_(instance, bstack1l11l1l1ll1_opy_)
        entries = hook.get(TestFramework.bstack1l11l11llll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []))
        return entries
    def bstack1ll1111111l_opy_(self, instance: bstack1llll1lll11_opy_, bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_]):
        bstack1l11l1l1ll1_opy_ = (
            PytestBDDFramework.bstack1l111lll1l1_opy_
            if bstack1llllll1l11_opy_[1] == bstack1lll11lllll_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1l1l_opy_
        )
        PytestBDDFramework.bstack1l1111ll111_opy_(instance, bstack1l11l1l1ll1_opy_)
        TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []).clear()
    @staticmethod
    def bstack1l111l11111_opy_(instance: bstack1llll1lll11_opy_, bstack1l11l1l1ll1_opy_: str):
        bstack1l11l11ll1l_opy_ = (
            PytestBDDFramework.bstack1l111l1l1l1_opy_
            if bstack1l11l1l1ll1_opy_ == PytestBDDFramework.bstack1l11l1l1l1l_opy_
            else PytestBDDFramework.bstack1l11l11l11l_opy_
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
        hook = PytestBDDFramework.bstack1l111l11111_opy_(instance, bstack1l11l1l1ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l11llll_opy_, []).clear()
    @staticmethod
    def __1l111l1lll1_opy_(instance: bstack1llll1lll11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1lll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᑆ"), None)):
            return
        if os.getenv(bstack1l1lll1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᑇ"), bstack1l1lll1_opy_ (u"ࠧ࠷ࠢᑈ")) != bstack1l1lll1_opy_ (u"ࠨ࠱ࠣᑉ"):
            PytestBDDFramework.logger.warning(bstack1l1lll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᑊ"))
            return
        bstack1l11ll111l1_opy_ = {
            bstack1l1lll1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᑋ"): (PytestBDDFramework.bstack1l111lll1l1_opy_, PytestBDDFramework.bstack1l11l11l11l_opy_),
            bstack1l1lll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᑌ"): (PytestBDDFramework.bstack1l11l1l1l1l_opy_, PytestBDDFramework.bstack1l111l1l1l1_opy_),
        }
        for when in (bstack1l1lll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᑍ"), bstack1l1lll1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᑎ"), bstack1l1lll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᑏ")):
            bstack1l1111lll1l_opy_ = args[1].get_records(when)
            if not bstack1l1111lll1l_opy_:
                continue
            records = [
                bstack1lll1l11ll1_opy_(
                    kind=TestFramework.bstack1l1lll1l1l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1lll1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᑐ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1lll1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᑑ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1111lll1l_opy_
                if isinstance(getattr(r, bstack1l1lll1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᑒ"), None), str) and r.message.strip()
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
    def __1l1111l1ll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11lll111_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l11111l_opy_(request.node, scenario)
        bstack1l111lllll1_opy_ = feature.filename
        if not bstack11lll111_opy_ or not test_name or not bstack1l111lllll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l11l11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111ll11l_opy_: bstack11lll111_opy_,
            TestFramework.bstack1ll11l1llll_opy_: test_name,
            TestFramework.bstack1l1ll111l11_opy_: bstack11lll111_opy_,
            TestFramework.bstack1l11l111ll1_opy_: bstack1l111lllll1_opy_,
            TestFramework.bstack1l111ll11l1_opy_: PytestBDDFramework.__1l11l1ll11l_opy_(feature, scenario),
            TestFramework.bstack1l11l111l11_opy_: code,
            TestFramework.bstack1l1l1l1l11l_opy_: TestFramework.bstack1l11l1llll1_opy_,
            TestFramework.bstack1l11lll1ll1_opy_: test_name
        }
    @staticmethod
    def __1l11l11111l_opy_(node, scenario):
        if hasattr(node, bstack1l1lll1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᑓ")):
            parts = node.nodeid.rsplit(bstack1l1lll1_opy_ (u"ࠥ࡟ࠧᑔ"))
            params = parts[-1]
            return bstack1l1lll1_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᑕ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1ll11l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1lll1_opy_ (u"ࠬࡺࡡࡨࡵࠪᑖ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1lll1_opy_ (u"࠭ࡴࡢࡩࡶࠫᑗ")) else [])
    @staticmethod
    def __1l111llll1l_opy_(location):
        return bstack1l1lll1_opy_ (u"ࠢ࠻࠼ࠥᑘ").join(filter(lambda x: isinstance(x, str), location))