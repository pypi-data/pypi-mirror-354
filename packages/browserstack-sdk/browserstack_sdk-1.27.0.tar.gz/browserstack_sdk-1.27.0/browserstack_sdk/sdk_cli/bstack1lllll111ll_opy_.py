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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack11111l1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_, bstack1llll1lll11_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllllll_opy_ import bstack1ll1ll1llll_opy_
from bstack_utils.helper import bstack1ll11llll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
import grpc
import traceback
import json
class bstack1lll11l111l_opy_(bstack1lll1llll1l_opy_):
    bstack1ll1l11llll_opy_ = False
    bstack1ll1l1llll1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᄠ")
    bstack1ll1l11l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᄡ")
    bstack1ll11llll1l_opy_ = bstack1l1lll1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤᄢ")
    bstack1ll1l1ll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥᄣ")
    bstack1ll1l1111l1_opy_ = bstack1l1lll1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢᄤ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1llll111111_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l11ll1l_opy_ = bstack1llll1l1l1l_opy_
        bstack1llll111111_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll1l1l1lll_opy_)
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.PRE), self.bstack1ll1l11111l_opy_)
        TestFramework.bstack1ll1l1lll1l_opy_((bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST), self.bstack1ll11l1ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11ll11_opy_(instance, args)
        test_framework = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll11llllll_opy_)
        if bstack1l1lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᄥ") in instance.bstack1ll1l1l1111_opy_:
            platform_index = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l1lllll_opy_)
            self.accessibility = self.bstack1ll1l1ll11l_opy_(tags, self.config[bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄦ")][platform_index])
        else:
            capabilities = self.bstack1ll1l11ll1l_opy_.bstack1ll1l111l11_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᄧ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠥࠦᄨ"))
                return
            self.accessibility = self.bstack1ll1l1ll11l_opy_(tags, capabilities)
        if self.bstack1ll1l11ll1l_opy_.pages and self.bstack1ll1l11ll1l_opy_.pages.values():
            bstack1ll1ll1111l_opy_ = list(self.bstack1ll1l11ll1l_opy_.pages.values())
            if bstack1ll1ll1111l_opy_ and isinstance(bstack1ll1ll1111l_opy_[0], (list, tuple)) and bstack1ll1ll1111l_opy_[0]:
                bstack1ll11ll11ll_opy_ = bstack1ll1ll1111l_opy_[0][0]
                if callable(bstack1ll11ll11ll_opy_):
                    page = bstack1ll11ll11ll_opy_()
                    def bstack1l1l11ll_opy_():
                        self.get_accessibility_results(page, bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄩ"))
                    def bstack1ll1l111ll1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᄪ"))
                    setattr(page, bstack1l1lll1_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤᄫ"), bstack1l1l11ll_opy_)
                    setattr(page, bstack1l1lll1_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤᄬ"), bstack1ll1l111ll1_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧᄭ") + str(self.accessibility) + bstack1l1lll1_opy_ (u"ࠤࠥᄮ"))
    def bstack1ll1l1l1lll_opy_(
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
            bstack11lll1ll1_opy_ = datetime.now()
            self.bstack1ll1l1l1l11_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᄯ"), datetime.now() - bstack11lll1ll1_opy_)
            if (
                not f.bstack1ll1l11l1ll_opy_(method_name)
                or f.bstack1ll1l11lll1_opy_(method_name, *args)
                or f.bstack1ll11ll1l1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllllll11_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll1l_opy_, False):
                if not bstack1lll11l111l_opy_.bstack1ll1l11llll_opy_:
                    self.logger.warning(bstack1l1lll1_opy_ (u"ࠦࡠࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢᄰ") + str(f.platform_index) + bstack1l1lll1_opy_ (u"ࠧࡣࠠࡢ࠳࠴ࡽࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡭ࡧࡶࡦࠢࡱࡳࡹࠦࡢࡦࡧࡱࠤࡸ࡫ࡴࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡷࡪࡹࡳࡪࡱࡱࠦᄱ"))
                    bstack1lll11l111l_opy_.bstack1ll1l11llll_opy_ = True
                return
            bstack1ll11l1l1l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l1l1l1_opy_:
                platform_index = f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0)
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᄲ") + str(f.framework_name) + bstack1l1lll1_opy_ (u"ࠢࠣᄳ"))
                return
            bstack1ll1l1l11ll_opy_ = f.bstack1ll1l111111_opy_(*args)
            if not bstack1ll1l1l11ll_opy_:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄴ") + str(method_name) + bstack1l1lll1_opy_ (u"ࠤࠥᄵ"))
                return
            bstack1ll11l1l1ll_opy_ = f.bstack1llllllll11_opy_(instance, bstack1lll11l111l_opy_.bstack1ll1l1111l1_opy_, False)
            if bstack1ll1l1l11ll_opy_ == bstack1l1lll1_opy_ (u"ࠥ࡫ࡪࡺࠢᄶ") and not bstack1ll11l1l1ll_opy_:
                f.bstack1111111lll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll1l1111l1_opy_, True)
                bstack1ll11l1l1ll_opy_ = True
            if not bstack1ll11l1l1ll_opy_:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡳࡵࠠࡖࡔࡏࠤࡱࡵࡡࡥࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄷ") + str(bstack1ll1l1l11ll_opy_) + bstack1l1lll1_opy_ (u"ࠧࠨᄸ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l1l11ll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᄹ") + str(bstack1ll1l1l11ll_opy_) + bstack1l1lll1_opy_ (u"ࠢࠣᄺ"))
                return
            self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡴࡥࡵ࡭ࡵࡺࡳࡠࡶࡲࡣࡷࡻ࡮ࠪࡿࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄻ") + str(bstack1ll1l1l11ll_opy_) + bstack1l1lll1_opy_ (u"ࠤࠥᄼ"))
            scripts = [(s, bstack1ll11l1l1l1_opy_[s]) for s in scripts_to_run if s in bstack1ll11l1l1l1_opy_]
            for script_name, bstack1ll1l1l11l1_opy_ in scripts:
                try:
                    bstack11lll1ll1_opy_ = datetime.now()
                    if script_name == bstack1l1lll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᄽ"):
                        result = self.perform_scan(driver, method=bstack1ll1l1l11ll_opy_, framework_name=f.framework_name)
                    instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᄾ") + script_name, datetime.now() - bstack11lll1ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1lll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄿ"), True):
                        self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᅀ") + str(result) + bstack1l1lll1_opy_ (u"ࠢࠣᅁ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1lll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᅂ") + str(e) + bstack1l1lll1_opy_ (u"ࠤࠥᅃ"))
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᅄ") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧᅅ"))
    def bstack1ll11l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11ll11_opy_(instance, args)
        capabilities = self.bstack1ll1l11ll1l_opy_.bstack1ll1l111l11_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1l1ll11l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᅆ"))
            return
        driver = self.bstack1ll1l11ll1l_opy_.bstack1ll11l1ll11_opy_(f, instance, bstack1llllll1l11_opy_, *args, **kwargs)
        test_name = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll11l1llll_opy_)
        if not test_name:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᅇ"))
            return
        test_uuid = f.bstack1llllllll11_opy_(instance, TestFramework.bstack1ll1l11l11l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᅈ"))
            return
        if isinstance(self.bstack1ll1l11ll1l_opy_, bstack1ll1lll1l11_opy_):
            framework_name = bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᅉ")
        else:
            framework_name = bstack1l1lll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᅊ")
        self.bstack1l11ll1lll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1ll11llll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᅋ"))
            return
        bstack11lll1ll1_opy_ = datetime.now()
        bstack1ll1l1l11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1lll1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᅌ"), None)
        if not bstack1ll1l1l11l1_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅍ") + str(framework_name) + bstack1l1lll1_opy_ (u"ࠨࠠࠣᅎ"))
            return
        instance = bstack11111l1l1l_opy_.bstack111111l11l_opy_(driver)
        if instance:
            if not bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, bstack1lll11l111l_opy_.bstack1ll1l1ll1l1_opy_, False):
                bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll1l1ll1l1_opy_, True)
            else:
                self.logger.info(bstack1l1lll1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᅏ") + str(method) + bstack1l1lll1_opy_ (u"ࠣࠤᅐ"))
                return
        self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᅑ") + str(method) + bstack1l1lll1_opy_ (u"ࠥࠦᅒ"))
        if framework_name == bstack1l1lll1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅓ"):
            result = self.bstack1ll1l11ll1l_opy_.bstack1ll11ll1111_opy_(driver, bstack1ll1l1l11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l11l1_opy_, {bstack1l1lll1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᅔ"): method if method else bstack1l1lll1_opy_ (u"ࠨࠢᅕ")})
        bstack1lll11l11l1_opy_.end(EVENTS.bstack1ll11llll1_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᅖ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᅗ"), True, None, command=method)
        if instance:
            bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll1l1ll1l1_opy_, False)
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨᅘ"), datetime.now() - bstack11lll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack111l11ll1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᅙ"))
            return
        bstack1ll1l1l11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1lll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᅚ"), None)
        if not bstack1ll1l1l11l1_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅛ") + str(framework_name) + bstack1l1lll1_opy_ (u"ࠨࠢᅜ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11lll1ll1_opy_ = datetime.now()
        if framework_name == bstack1l1lll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᅝ"):
            result = self.bstack1ll1l11ll1l_opy_.bstack1ll11ll1111_opy_(driver, bstack1ll1l1l11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l11l1_opy_)
        instance = bstack11111l1l1l_opy_.bstack111111l11l_opy_(driver)
        if instance:
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᅞ"), datetime.now() - bstack11lll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack11llll11l1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᅟ"))
            return
        bstack1ll1l1l11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1lll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᅠ"), None)
        if not bstack1ll1l1l11l1_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᅡ") + str(framework_name) + bstack1l1lll1_opy_ (u"ࠧࠨᅢ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11lll1ll1_opy_ = datetime.now()
        if framework_name == bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅣ"):
            result = self.bstack1ll1l11ll1l_opy_.bstack1ll11ll1111_opy_(driver, bstack1ll1l1l11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l11l1_opy_)
        instance = bstack11111l1l1l_opy_.bstack111111l11l_opy_(driver)
        if instance:
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼࠦᅤ"), datetime.now() - bstack11lll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1l1l1l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1ll11ll1lll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llll11l1l1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᅥ") + str(r) + bstack1l1lll1_opy_ (u"ࠤࠥᅦ"))
            else:
                self.bstack1ll11lll11l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᅧ") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧᅨ"))
            traceback.print_exc()
            raise e
    def bstack1ll11lll11l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡲ࡯ࡢࡦࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᅩ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11lllll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l1llll1_opy_ and command.module == self.bstack1ll1l11l1l1_opy_:
                        if command.method and not command.method in bstack1ll11lllll1_opy_:
                            bstack1ll11lllll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11lllll1_opy_[command.method]:
                            bstack1ll11lllll1_opy_[command.method][command.name] = list()
                        bstack1ll11lllll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11lllll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l1l1l11_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l11ll1l_opy_, bstack1ll1lll1l11_opy_) and method_name != bstack1l1lll1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᅪ"):
            return
        if bstack11111l1l1l_opy_.bstack11111ll11l_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll1l_opy_):
            return
        if f.bstack1ll11ll111l_opy_(method_name, *args):
            bstack1ll11l1l11l_opy_ = False
            desired_capabilities = f.bstack1ll1l111l1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11l1lll1_opy_(instance)
                platform_index = f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0)
                bstack1ll1l1lll11_opy_ = datetime.now()
                r = self.bstack1ll11ll1lll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᅫ"), datetime.now() - bstack1ll1l1lll11_opy_)
                bstack1ll11l1l11l_opy_ = r.success
            else:
                self.logger.error(bstack1l1lll1_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥᅬ") + str(desired_capabilities) + bstack1l1lll1_opy_ (u"ࠤࠥᅭ"))
            f.bstack1111111lll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll1l_opy_, bstack1ll11l1l11l_opy_)
    def bstack11lll1111_opy_(self, test_tags):
        bstack1ll11ll1lll_opy_ = self.config.get(bstack1l1lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᅮ"))
        if not bstack1ll11ll1lll_opy_:
            return True
        try:
            include_tags = bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅯ")] if bstack1l1lll1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅰ") in bstack1ll11ll1lll_opy_ and isinstance(bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅱ")], list) else []
            exclude_tags = bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅲ")] if bstack1l1lll1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅳ") in bstack1ll11ll1lll_opy_ and isinstance(bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅴ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᅵ") + str(error))
        return False
    def bstack1ll111ll1l_opy_(self, caps):
        try:
            bstack1ll1ll11111_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᅶ"), {}).get(bstack1l1lll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᅷ"), caps.get(bstack1l1lll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᅸ"), bstack1l1lll1_opy_ (u"ࠧࠨᅹ")))
            if bstack1ll1ll11111_opy_:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᅺ"))
                return False
            browser = caps.get(bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᅻ"), bstack1l1lll1_opy_ (u"ࠪࠫᅼ")).lower()
            if browser != bstack1l1lll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᅽ"):
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᅾ"))
                return False
            bstack1ll1l111lll_opy_ = bstack1ll11lll1l1_opy_
            if not self.config.get(bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᅿ")) or self.config.get(bstack1l1lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᆀ")):
                bstack1ll1l111lll_opy_ = bstack1ll1l1ll111_opy_
            browser_version = caps.get(bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᆁ"))
            if not browser_version:
                browser_version = caps.get(bstack1l1lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᆂ"), {}).get(bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᆃ"), bstack1l1lll1_opy_ (u"ࠫࠬᆄ"))
            if browser_version and browser_version != bstack1l1lll1_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᆅ") and int(browser_version.split(bstack1l1lll1_opy_ (u"࠭࠮ࠨᆆ"))[0]) <= bstack1ll1l111lll_opy_:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࠤᆇ") + str(bstack1ll1l111lll_opy_) + bstack1l1lll1_opy_ (u"ࠣ࠰ࠥᆈ"))
                return False
            bstack1ll1l1l111l_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᆉ"), {}).get(bstack1l1lll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᆊ"))
            if not bstack1ll1l1l111l_opy_:
                bstack1ll1l1l111l_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᆋ"), {})
            if bstack1ll1l1l111l_opy_ and bstack1l1lll1_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᆌ") in bstack1ll1l1l111l_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫᆍ"), []):
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᆎ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᆏ") + str(error))
            return False
    def bstack1ll11lll1ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l1ll1ll_opy_ = {
            bstack1l1lll1_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᆐ"): test_uuid,
        }
        bstack1ll1l1l1ll1_opy_ = {}
        if result.success:
            bstack1ll1l1l1ll1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll11llll11_opy_(bstack1ll1l1ll1ll_opy_, bstack1ll1l1l1ll1_opy_)
    def bstack1l11ll1lll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1l11l111_opy_ = None
        try:
            self.bstack1ll1l1111ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1lll1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᆑ")
            req.script_name = bstack1l1lll1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᆒ")
            r = self.bstack1llll11l1l1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆓ") + str(r.error) + bstack1l1lll1_opy_ (u"ࠨࠢᆔ"))
            else:
                bstack1ll1l1ll1ll_opy_ = self.bstack1ll11lll1ll_opy_(test_uuid, r)
                bstack1ll1l1l11l1_opy_ = r.script
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᆕ") + str(bstack1ll1l1ll1ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l1l11l1_opy_:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆖ") + str(framework_name) + bstack1l1lll1_opy_ (u"ࠤࠣࠦᆗ"))
                return
            bstack1ll1l11l111_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1ll11ll1l11_opy_.value)
            self.bstack1ll11ll11l1_opy_(driver, bstack1ll1l1l11l1_opy_, bstack1ll1l1ll1ll_opy_, framework_name)
            self.logger.info(bstack1l1lll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᆘ"))
            bstack1lll11l11l1_opy_.end(EVENTS.bstack1ll11ll1l11_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᆙ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᆚ"), True, None, command=bstack1l1lll1_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᆛ"),test_name=name)
        except Exception as bstack1ll11lll111_opy_:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᆜ") + bstack1l1lll1_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦᆝ") + bstack1l1lll1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᆞ") + str(bstack1ll11lll111_opy_))
            bstack1lll11l11l1_opy_.end(EVENTS.bstack1ll11ll1l11_opy_.value, bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᆟ"), bstack1ll1l11l111_opy_+bstack1l1lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᆠ"), False, bstack1ll11lll111_opy_, command=bstack1l1lll1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᆡ"),test_name=name)
    def bstack1ll11ll11l1_opy_(self, driver, bstack1ll1l1l11l1_opy_, bstack1ll1l1ll1ll_opy_, framework_name):
        if framework_name == bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᆢ"):
            self.bstack1ll1l11ll1l_opy_.bstack1ll11ll1111_opy_(driver, bstack1ll1l1l11l1_opy_, bstack1ll1l1ll1ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l1l11l1_opy_, bstack1ll1l1ll1ll_opy_))
    def _1ll1l11ll11_opy_(self, instance: bstack1llll1lll11_opy_, args: Tuple) -> list:
        bstack1l1lll1_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᆣ")
        if bstack1l1lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᆤ") in instance.bstack1ll1l1l1111_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1lll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᆥ")) else []
        if hasattr(args[0], bstack1l1lll1_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᆦ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1l1ll11l_opy_(self, tags, capabilities):
        return self.bstack11lll1111_opy_(tags) and self.bstack1ll111ll1l_opy_(capabilities)