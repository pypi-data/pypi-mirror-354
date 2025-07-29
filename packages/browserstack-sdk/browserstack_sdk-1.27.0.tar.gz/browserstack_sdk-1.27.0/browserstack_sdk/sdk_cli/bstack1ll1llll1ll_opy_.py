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
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll111l11_opy_(bstack1lll1llll1l_opy_):
    bstack1ll1l11llll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l11l11_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11l1111l_opy_(hub_url):
            if not bstack1llll111l11_opy_.bstack1ll1l11llll_opy_:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᆧ") + str(hub_url) + bstack1l1lll1_opy_ (u"ࠧࠨᆨ"))
                bstack1llll111l11_opy_.bstack1ll1l11llll_opy_ = True
            return
        bstack1ll1l1l11ll_opy_ = f.bstack1ll1l111111_opy_(*args)
        bstack1ll11l111l1_opy_ = f.bstack1ll11l1l111_opy_(*args)
        if bstack1ll1l1l11ll_opy_ and bstack1ll1l1l11ll_opy_.lower() == bstack1l1lll1_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦᆩ") and bstack1ll11l111l1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11l111l1_opy_.get(bstack1l1lll1_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᆪ"), None), bstack1ll11l111l1_opy_.get(bstack1l1lll1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᆫ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢᆬ") + str(locator_value) + bstack1l1lll1_opy_ (u"ࠥࠦᆭ"))
                return
            def bstack11111l1ll1_opy_(driver, bstack1ll11l11111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l11111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll111lllll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1lll1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢᆮ") + str(locator_value) + bstack1l1lll1_opy_ (u"ࠧࠨᆯ"))
                    else:
                        self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᆰ") + str(response) + bstack1l1lll1_opy_ (u"ࠢࠣᆱ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11l111ll_opy_(
                        driver, bstack1ll11l11111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack11111l1ll1_opy_.__name__ = bstack1ll1l1l11ll_opy_
            return bstack11111l1ll1_opy_
    def __1ll11l111ll_opy_(
        self,
        driver,
        bstack1ll11l11111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll111lllll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᆲ") + str(locator_value) + bstack1l1lll1_opy_ (u"ࠤࠥᆳ"))
                bstack1ll11l11l1l_opy_ = self.bstack1ll111llll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥᆴ") + str(bstack1ll11l11l1l_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧᆵ"))
                if bstack1ll11l11l1l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1lll1_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᆶ"): bstack1ll11l11l1l_opy_.locator_type,
                            bstack1l1lll1_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᆷ"): bstack1ll11l11l1l_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l11111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣᆸ"), False):
                    self.logger.info(bstack1ll1lll1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨᆹ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1lll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧᆺ") + str(response) + bstack1l1lll1_opy_ (u"ࠥࠦᆻ"))
        except Exception as err:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣᆼ") + str(err) + bstack1l1lll1_opy_ (u"ࠧࠨᆽ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11l11lll_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1ll111lllll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1lll1_opy_ (u"ࠨ࠰ࠣᆾ"),
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1lll1_opy_ (u"ࠢࠣᆿ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll11l1l1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇀ") + str(r) + bstack1l1lll1_opy_ (u"ࠤࠥᇁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇂ") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧᇃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l11ll1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1ll111llll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1lll1_opy_ (u"ࠧ࠶ࠢᇄ")):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll11l1l1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1lll1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᇅ") + str(r) + bstack1l1lll1_opy_ (u"ࠢࠣᇆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᇇ") + str(e) + bstack1l1lll1_opy_ (u"ࠤࠥᇈ"))
            traceback.print_exc()
            raise e