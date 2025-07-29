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
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1111l1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
class bstack1llll1l1lll_opy_(bstack1lll1llll1l_opy_):
    bstack1l1l11ll111_opy_ = bstack1l1lll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥዡ")
    bstack1l1l11l11l1_opy_ = bstack1l1lll1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧዢ")
    bstack1l1l111llll_opy_ = bstack1l1lll1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧዣ")
    def __init__(self, bstack1lllll111ll_opy_):
        super().__init__()
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l111l11l_opy_)
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1l11l1111_opy_)
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1l11l1ll1_opy_)
        bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.bstack1l1l1111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l11l_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1lll1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣዤ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥዥ")), str):
                    url = kwargs.get(bstack1l1lll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦዦ"))
                elif hasattr(kwargs.get(bstack1l1lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧዧ")), bstack1l1lll1_opy_ (u"ࠪࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠫየ")):
                    url = kwargs.get(bstack1l1lll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢዩ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣዪ"))._url
            except Exception as e:
                url = bstack1l1lll1_opy_ (u"࠭ࠧያ")
                self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡳ࡮ࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࢁࠧዬ").format(e))
            self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡔࡨࡱࡴࡺࡥࠡࡕࡨࡶࡻ࡫ࡲࠡࡃࡧࡨࡷ࡫ࡳࡴࠢࡥࡩ࡮ࡴࡧࠡࡲࡤࡷࡸ࡫ࡤࠡࡣࡶࠤ࠿ࠦࡻࡾࠤይ").format(str(url)))
            self.bstack1l1l11111ll_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢዮ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1llllllll11_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l11ll111_opy_, False):
            return
        if not f.bstack11111ll11l_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_):
            return
        platform_index = f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_)
        if f.bstack1ll11ll111l_opy_(method_name, *args) and len(args) > 1:
            bstack11lll1ll1_opy_ = datetime.now()
            hub_url = bstack1lll11l1l11_opy_.hub_url(driver)
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧዯ") + str(hub_url) + bstack1l1lll1_opy_ (u"ࠦࠧደ"))
            bstack1l1l111l111_opy_ = args[1][bstack1l1lll1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዱ")] if isinstance(args[1], dict) and bstack1l1lll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧዲ") in args[1] else None
            bstack1l1l1111111_opy_ = bstack1l1lll1_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧዳ")
            if isinstance(bstack1l1l111l111_opy_, dict):
                bstack11lll1ll1_opy_ = datetime.now()
                r = self.bstack1l1l11111l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨዴ"), datetime.now() - bstack11lll1ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡶࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨ࠼ࠣࠦድ") + str(r) + bstack1l1lll1_opy_ (u"ࠥࠦዶ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l11l1lll_opy_(instance, driver, r.hub_url)
                        f.bstack1111111lll_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l11ll111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1lll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥዷ"), e)
    def bstack1l1l11l1111_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll11l1l11_opy_.session_id(driver)
            if session_id:
                bstack1l1l111l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢዸ").format(session_id)
                bstack1lll11l11l1_opy_.mark(bstack1l1l111l1ll_opy_)
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllllll11_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l11l11l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll11l1l11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥዹ") + str(hub_url) + bstack1l1lll1_opy_ (u"ࠢࠣዺ"))
            return
        framework_session_id = bstack1lll11l1l11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦዻ") + str(framework_session_id) + bstack1l1lll1_opy_ (u"ࠤࠥዼ"))
            return
        if bstack1lll11l1l11_opy_.bstack1l1l111ll11_opy_(*args) == bstack1lll11l1l11_opy_.bstack1l11lllllll_opy_:
            bstack1l1l1111l1l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡿࢂࡀࡥ࡯ࡦࠥዽ").format(framework_session_id)
            bstack1l1l111l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨዾ").format(framework_session_id)
            bstack1lll11l11l1_opy_.end(
                label=bstack1l1lll1_opy_ (u"ࠧࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠣዿ"),
                start=bstack1l1l111l1ll_opy_,
                end=bstack1l1l1111l1l_opy_,
                status=True,
                failure=None
            )
            bstack11lll1ll1_opy_ = datetime.now()
            r = self.bstack1l11llllll1_opy_(
                ref,
                f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧጀ"), datetime.now() - bstack11lll1ll1_opy_)
            f.bstack1111111lll_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l11l11l1_opy_, r.success)
    def bstack1l1l1111lll_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllllll11_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l111llll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll11l1l11_opy_.session_id(driver)
        hub_url = bstack1lll11l1l11_opy_.hub_url(driver)
        bstack11lll1ll1_opy_ = datetime.now()
        r = self.bstack1l1l111l1l1_opy_(
            ref,
            f.bstack1llllllll11_opy_(instance, bstack1lll11l1l11_opy_.bstack1ll1l1lllll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧጁ"), datetime.now() - bstack11lll1ll1_opy_)
        f.bstack1111111lll_opy_(instance, bstack1llll1l1lll_opy_.bstack1l1l111llll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l11ll1l1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1l1lll11l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨጂ") + str(req) + bstack1l1lll1_opy_ (u"ࠤࠥጃ"))
        try:
            r = self.bstack1llll11l1l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨጄ") + str(r.success) + bstack1l1lll1_opy_ (u"ࠦࠧጅ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጆ") + str(e) + bstack1l1lll1_opy_ (u"ࠨࠢጇ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll11l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1l11111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤገ") + str(req) + bstack1l1lll1_opy_ (u"ࠣࠤጉ"))
        try:
            r = self.bstack1llll11l1l1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧጊ") + str(r.success) + bstack1l1lll1_opy_ (u"ࠥࠦጋ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጌ") + str(e) + bstack1l1lll1_opy_ (u"ࠧࠨግ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111l11_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l11llllll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤጎ") + str(req) + bstack1l1lll1_opy_ (u"ࠢࠣጏ"))
        try:
            r = self.bstack1llll11l1l1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥጐ") + str(r) + bstack1l1lll1_opy_ (u"ࠤࠥ጑"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጒ") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧጓ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l111111l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1l111l1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴ࠿ࠦࠢጔ") + str(req) + bstack1l1lll1_opy_ (u"ࠨࠢጕ"))
        try:
            r = self.bstack1llll11l1l1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤ጖") + str(r) + bstack1l1lll1_opy_ (u"ࠣࠤ጗"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢጘ") + str(e) + bstack1l1lll1_opy_ (u"ࠥࠦጙ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111111111_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1l1l11111ll_opy_(self, instance: bstack1lllllll1ll_opy_, url: str, f: bstack1lll11l1l11_opy_, kwargs):
        bstack1l1l111ll1l_opy_ = version.parse(f.framework_version)
        bstack1l1l11l1l1l_opy_ = kwargs.get(bstack1l1lll1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧጚ"))
        bstack1l1l11l11ll_opy_ = kwargs.get(bstack1l1lll1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጛ"))
        bstack1l1l1ll11l1_opy_ = {}
        bstack1l1l1111ll1_opy_ = {}
        bstack1l1l111lll1_opy_ = None
        bstack1l1l11l111l_opy_ = {}
        if bstack1l1l11l11ll_opy_ is not None or bstack1l1l11l1l1l_opy_ is not None: # check top level caps
            if bstack1l1l11l11ll_opy_ is not None:
                bstack1l1l11l111l_opy_[bstack1l1lll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ጜ")] = bstack1l1l11l11ll_opy_
            if bstack1l1l11l1l1l_opy_ is not None and callable(getattr(bstack1l1l11l1l1l_opy_, bstack1l1lll1_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጝ"))):
                bstack1l1l11l111l_opy_[bstack1l1lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫጞ")] = bstack1l1l11l1l1l_opy_.to_capabilities()
        response = self.bstack1l1l1lll11l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l11l111l_opy_).encode(bstack1l1lll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣጟ")))
        if response is not None and response.capabilities:
            bstack1l1l1ll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1lll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤጠ")))
            if not bstack1l1l1ll11l1_opy_: # empty caps bstack1l1l1l1ll11_opy_ bstack1l1l1l1ll1l_opy_ bstack1l1l1lllll1_opy_ bstack1lll1llllll_opy_ or error in processing
                return
            bstack1l1l111lll1_opy_ = f.bstack1llll1111ll_opy_[bstack1l1lll1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣጡ")](bstack1l1l1ll11l1_opy_)
        if bstack1l1l11l1l1l_opy_ is not None and bstack1l1l111ll1l_opy_ >= version.parse(bstack1l1lll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫጢ")):
            bstack1l1l1111ll1_opy_ = None
        if (
                not bstack1l1l11l1l1l_opy_ and not bstack1l1l11l11ll_opy_
        ) or (
                bstack1l1l111ll1l_opy_ < version.parse(bstack1l1lll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬጣ"))
        ):
            bstack1l1l1111ll1_opy_ = {}
            bstack1l1l1111ll1_opy_.update(bstack1l1l1ll11l1_opy_)
        self.logger.info(bstack1111l1lll_opy_)
        if os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥጤ")).lower().__eq__(bstack1l1lll1_opy_ (u"ࠣࡶࡵࡹࡪࠨጥ")):
            kwargs.update(
                {
                    bstack1l1lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧጦ"): f.bstack1l1l11l1l11_opy_,
                }
            )
        if bstack1l1l111ll1l_opy_ >= version.parse(bstack1l1lll1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪጧ")):
            if bstack1l1l11l11ll_opy_ is not None:
                del kwargs[bstack1l1lll1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጨ")]
            kwargs.update(
                {
                    bstack1l1lll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨጩ"): bstack1l1l111lll1_opy_,
                    bstack1l1lll1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጪ"): True,
                    bstack1l1lll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢጫ"): None,
                }
            )
        elif bstack1l1l111ll1l_opy_ >= version.parse(bstack1l1lll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧጬ")):
            kwargs.update(
                {
                    bstack1l1lll1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጭ"): bstack1l1l1111ll1_opy_,
                    bstack1l1lll1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦጮ"): bstack1l1l111lll1_opy_,
                    bstack1l1lll1_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣጯ"): True,
                    bstack1l1lll1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧጰ"): None,
                }
            )
        elif bstack1l1l111ll1l_opy_ >= version.parse(bstack1l1lll1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ጱ")):
            kwargs.update(
                {
                    bstack1l1lll1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጲ"): bstack1l1l1111ll1_opy_,
                    bstack1l1lll1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጳ"): True,
                    bstack1l1lll1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጴ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1lll1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጵ"): bstack1l1l1111ll1_opy_,
                    bstack1l1lll1_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣጶ"): True,
                    bstack1l1lll1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧጷ"): None,
                }
            )