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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l11111_opy_ import bstack11111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1llll111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1lllll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l11l_opy_ import bstack1llll1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1_opy_ import bstack1ll11l1l1_opy_, bstack11lll1l111_opy_, bstack11l1l1l11_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1llll1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import bstack11111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllllll_opy_ import bstack1ll1ll1llll_opy_
from bstack_utils.helper import Notset, bstack1lll11lll1l_opy_, get_cli_dir, bstack1ll1lll11l1_opy_, bstack1l1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1111_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11_opy_ import bstack1ll1lll1_opy_
from bstack_utils.helper import Notset, bstack1lll11lll1l_opy_, get_cli_dir, bstack1ll1lll11l1_opy_, bstack1l1ll1lll1_opy_, bstack1lll1l1ll1_opy_, bstack1llllll111_opy_, bstack11l1lll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll1lll1_opy_, bstack1llll1lll11_opy_, bstack1lll11lllll_opy_, bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import bstack1lllllll1ll_opy_, bstack1llllll111l_opy_, bstack1llllll1l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l111111l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll11lll1l_opy_, bstack11l11ll1_opy_
logger = bstack1l111111l_opy_.get_logger(__name__, bstack1l111111l_opy_.bstack1lllll11111_opy_())
def bstack1lll11111l1_opy_(bs_config):
    bstack1lll1ll1ll1_opy_ = None
    bstack1lll1lll111_opy_ = None
    try:
        bstack1lll1lll111_opy_ = get_cli_dir()
        bstack1lll1ll1ll1_opy_ = bstack1ll1lll11l1_opy_(bstack1lll1lll111_opy_)
        bstack1lllll11ll1_opy_ = bstack1lll11lll1l_opy_(bstack1lll1ll1ll1_opy_, bstack1lll1lll111_opy_, bs_config)
        bstack1lll1ll1ll1_opy_ = bstack1lllll11ll1_opy_ if bstack1lllll11ll1_opy_ else bstack1lll1ll1ll1_opy_
        if not bstack1lll1ll1ll1_opy_:
            raise ValueError(bstack1l1lll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦ၌"))
    except Exception as ex:
        logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦ၍").format(ex))
        bstack1lll1ll1ll1_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧ၎"))
        if bstack1lll1ll1ll1_opy_:
            logger.debug(bstack1l1lll1_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨ၏") + str(bstack1lll1ll1ll1_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧၐ"))
        else:
            logger.debug(bstack1l1lll1_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣၑ"))
    return bstack1lll1ll1ll1_opy_, bstack1lll1lll111_opy_
bstack1lll1111ll1_opy_ = bstack1l1lll1_opy_ (u"ࠨ࠹࠺࠻࠼ࠦၒ")
bstack1lll1l1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨၓ")
bstack1lll11lll11_opy_ = bstack1l1lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧၔ")
bstack1lll111111l_opy_ = bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢၕ")
bstack1llll1ll11_opy_ = bstack1l1lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨၖ")
bstack1lll1111111_opy_ = re.compile(bstack1l1lll1_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥၗ"))
bstack1lll11l1l1l_opy_ = bstack1l1lll1_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥၘ")
bstack1lll1ll1l1l_opy_ = [
    bstack11lll1l111_opy_.bstack1l1l11lll1_opy_,
    bstack11lll1l111_opy_.CONNECT,
    bstack11lll1l111_opy_.bstack1l1ll1111_opy_,
]
class SDKCLI:
    _1lll1ll1lll_opy_ = None
    process: Union[None, Any]
    bstack1lllll1111l_opy_: bool
    bstack1lll111l1ll_opy_: bool
    bstack1llll11ll1l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll1lll111l_opy_: Union[None, grpc.Channel]
    bstack1llll111ll1_opy_: str
    test_framework: TestFramework
    bstack11111ll1l1_opy_: bstack11111l1l1l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll11ll11l_opy_: bstack1llll1lllll_opy_
    accessibility: bstack1lll11l111l_opy_
    bstack1llll1l11_opy_: bstack1ll1lll1_opy_
    ai: bstack1llll111l11_opy_
    bstack1llll1ll1l1_opy_: bstack1lllll1l1ll_opy_
    bstack1ll1ll1ll1l_opy_: List[bstack1lll1llll1l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lllll11lll_opy_: Any
    bstack1lll1l11lll_opy_: Dict[str, timedelta]
    bstack1lll1111lll_opy_: str
    bstack1111l11111_opy_: bstack11111lll11_opy_
    def __new__(cls):
        if not cls._1lll1ll1lll_opy_:
            cls._1lll1ll1lll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll1ll1lll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lllll1111l_opy_ = False
        self.bstack1ll1lll111l_opy_ = None
        self.bstack1llll11l1l1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll111111l_opy_, None)
        self.bstack1lll111lll1_opy_ = os.environ.get(bstack1lll11lll11_opy_, bstack1l1lll1_opy_ (u"ࠨࠢၙ")) == bstack1l1lll1_opy_ (u"ࠢࠣၚ")
        self.bstack1lll111l1ll_opy_ = False
        self.bstack1llll11ll1l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lllll11lll_opy_ = None
        self.test_framework = None
        self.bstack11111ll1l1_opy_ = None
        self.bstack1llll111ll1_opy_=bstack1l1lll1_opy_ (u"ࠣࠤၛ")
        self.session_framework = None
        self.logger = bstack1l111111l_opy_.get_logger(self.__class__.__name__, bstack1l111111l_opy_.bstack1lllll11111_opy_())
        self.bstack1lll1l11lll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l11111_opy_ = bstack11111lll11_opy_()
        self.bstack1llll111111_opy_ = None
        self.bstack1llll1l1l1l_opy_ = None
        self.bstack1lll11ll11l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1ll1ll1l_opy_ = []
    def bstack11ll1llll_opy_(self):
        return os.environ.get(bstack1llll1ll11_opy_).lower().__eq__(bstack1l1lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢၜ"))
    def is_enabled(self, config):
        if bstack1l1lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧၝ") in config and str(config[bstack1l1lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨၞ")]).lower() != bstack1l1lll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫၟ"):
            return False
        bstack1llll1lll1l_opy_ = [bstack1l1lll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨၠ"), bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦၡ")]
        bstack1lll1ll1l11_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦၢ")) in bstack1llll1lll1l_opy_ or os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪၣ")) in bstack1llll1lll1l_opy_
        os.environ[bstack1l1lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨၤ")] = str(bstack1lll1ll1l11_opy_) # bstack1lll111l11l_opy_ bstack1lll1l1ll11_opy_ VAR to bstack1lll1ll1111_opy_ is binary running
        return bstack1lll1ll1l11_opy_
    def bstack1lll1lll_opy_(self):
        for event in bstack1lll1ll1l1l_opy_:
            bstack1ll11l1l1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll11l1l1_opy_.logger.debug(bstack1l1lll1_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢၥ") + str(kwargs) + bstack1l1lll1_opy_ (u"ࠧࠨၦ"))
            )
        bstack1ll11l1l1_opy_.register(bstack11lll1l111_opy_.bstack1l1l11lll1_opy_, self.__1ll1llll1l1_opy_)
        bstack1ll11l1l1_opy_.register(bstack11lll1l111_opy_.CONNECT, self.__1lll111ll1l_opy_)
        bstack1ll11l1l1_opy_.register(bstack11lll1l111_opy_.bstack1l1ll1111_opy_, self.__1llll1ll1ll_opy_)
        bstack1ll11l1l1_opy_.register(bstack11lll1l111_opy_.bstack1lllll1111_opy_, self.__1llll1l1l11_opy_)
    def bstack1l1l1l1l1l_opy_(self):
        return not self.bstack1lll111lll1_opy_ and os.environ.get(bstack1lll11lll11_opy_, bstack1l1lll1_opy_ (u"ࠨࠢၧ")) != bstack1l1lll1_opy_ (u"ࠢࠣၨ")
    def is_running(self):
        if self.bstack1lll111lll1_opy_:
            return self.bstack1lllll1111l_opy_
        else:
            return bool(self.bstack1ll1lll111l_opy_)
    def bstack1ll1lll1l1l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1ll1ll1l_opy_) and cli.is_running()
    def __1ll1lll1111_opy_(self, bstack1lll1llll11_opy_=10):
        if self.bstack1llll11l1l1_opy_:
            return
        bstack11lll1ll1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll111111l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣ࡝ࠥၩ") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣၪ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l1lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧၫ"), 0), (bstack1l1lll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢၬ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll1llll11_opy_)
        self.bstack1ll1lll111l_opy_ = channel
        self.bstack1llll11l1l1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll1lll111l_opy_)
        self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦၭ"), datetime.now() - bstack11lll1ll1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll111111l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨၮ") + str(self.bstack1l1l1l1l1l_opy_()) + bstack1l1lll1_opy_ (u"ࠢࠣၯ"))
    def __1llll1ll1ll_opy_(self, event_name):
        if self.bstack1l1l1l1l1l_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣၰ"))
        self.__1lll1l1ll1l_opy_()
    def __1llll1l1l11_opy_(self, event_name, bstack1lll1ll11ll_opy_ = None, bstack111llll1l_opy_=1):
        if bstack111llll1l_opy_ == 1:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤၱ"))
        bstack1llll11l11l_opy_ = Path(bstack1ll1lll1ll1_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦၲ"))
        if self.bstack1lll1lll111_opy_ and bstack1llll11l11l_opy_.exists():
            with open(bstack1llll11l11l_opy_, bstack1l1lll1_opy_ (u"ࠫࡷ࠭ၳ"), encoding=bstack1l1lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫၴ")) as fp:
                data = json.load(fp)
                try:
                    bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"࠭ࡐࡐࡕࡗࠫၵ"), bstack1llllll111_opy_(bstack11ll1l1l1l_opy_), data, {
                        bstack1l1lll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬၶ"): (self.config[bstack1l1lll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪၷ")], self.config[bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬၸ")])
                    })
                except Exception as e:
                    logger.debug(bstack11l11ll1_opy_.format(str(e)))
            bstack1llll11l11l_opy_.unlink()
        sys.exit(bstack111llll1l_opy_)
    @measure(event_name=EVENTS.bstack1lll11ll111_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1ll1llll1l1_opy_(self, event_name: str, data):
        from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
        self.bstack1llll111ll1_opy_, self.bstack1lll1lll111_opy_ = bstack1lll11111l1_opy_(data.bs_config)
        os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨၹ")] = self.bstack1lll1lll111_opy_
        if not self.bstack1llll111ll1_opy_ or not self.bstack1lll1lll111_opy_:
            raise ValueError(bstack1l1lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥၺ"))
        if self.bstack1l1l1l1l1l_opy_():
            self.__1lll111ll1l_opy_(event_name, bstack11l1l1l11_opy_())
            return
        try:
            bstack1lll11l11l1_opy_.end(EVENTS.bstack1l11l111l1_opy_.value, EVENTS.bstack1l11l111l1_opy_.value + bstack1l1lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧၻ"), EVENTS.bstack1l11l111l1_opy_.value + bstack1l1lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦၼ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1l1lll1_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨၽ"))
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧၾ").format(e))
        start = datetime.now()
        is_started = self.__1llll1ll11l_opy_()
        self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨၿ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1lll1111_opy_()
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤႀ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1l11l11_opy_(data)
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤႁ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll1l11l1l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1lll111ll1l_opy_(self, event_name: str, data: bstack11l1l1l11_opy_):
        if not self.bstack1l1l1l1l1l_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤႂ"))
            return
        bin_session_id = os.environ.get(bstack1lll11lll11_opy_)
        start = datetime.now()
        self.__1ll1lll1111_opy_()
        self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧႃ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨႄ") + str(bin_session_id) + bstack1l1lll1_opy_ (u"ࠣࠤႅ"))
        start = datetime.now()
        self.__1llll11111l_opy_()
        self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢႆ"), datetime.now() - start)
    def __1lllll1l111_opy_(self):
        if not self.bstack1llll11l1l1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢႇ"))
            return
        bstack1llll1l11ll_opy_ = {
            bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႈ"): (bstack1lll1l111ll_opy_, bstack1ll1lll1l11_opy_, bstack1ll1ll1llll_opy_),
            bstack1l1lll1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢႉ"): (bstack1llll1l1lll_opy_, bstack1ll1lll1lll_opy_, bstack1lll11l1l11_opy_),
        }
        if not self.bstack1llll111111_opy_ and self.session_framework in bstack1llll1l11ll_opy_:
            bstack1ll1llll111_opy_, bstack1lll1lll11l_opy_, bstack1lllll1l1l1_opy_ = bstack1llll1l11ll_opy_[self.session_framework]
            bstack1ll1lll11ll_opy_ = bstack1lll1lll11l_opy_()
            self.bstack1llll1l1l1l_opy_ = bstack1ll1lll11ll_opy_
            self.bstack1llll111111_opy_ = bstack1lllll1l1l1_opy_
            self.bstack1ll1ll1ll1l_opy_.append(bstack1ll1lll11ll_opy_)
            self.bstack1ll1ll1ll1l_opy_.append(bstack1ll1llll111_opy_(self.bstack1llll1l1l1l_opy_))
        if not self.bstack1lll11ll11l_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1llllll_opy_
            self.bstack1lll11ll11l_opy_ = bstack1llll1lllll_opy_(self.bstack1llll111111_opy_, self.bstack1llll1l1l1l_opy_) # bstack1lll1lllll1_opy_
            self.bstack1ll1ll1ll1l_opy_.append(self.bstack1lll11ll11l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll11l111l_opy_(self.bstack1llll111111_opy_, self.bstack1llll1l1l1l_opy_)
            self.bstack1ll1ll1ll1l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l1lll1_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣႊ"), False) == True:
            self.ai = bstack1llll111l11_opy_()
            self.bstack1ll1ll1ll1l_opy_.append(self.ai)
        if not self.percy and self.bstack1lllll11lll_opy_ and self.bstack1lllll11lll_opy_.success:
            self.percy = bstack1lllll1l1ll_opy_(self.bstack1lllll11lll_opy_)
            self.bstack1ll1ll1ll1l_opy_.append(self.percy)
        for mod in self.bstack1ll1ll1ll1l_opy_:
            if not mod.bstack1lll1l1lll1_opy_():
                mod.configure(self.bstack1llll11l1l1_opy_, self.config, self.cli_bin_session_id, self.bstack1111l11111_opy_)
    def __1llll11l111_opy_(self):
        for mod in self.bstack1ll1ll1ll1l_opy_:
            if mod.bstack1lll1l1lll1_opy_():
                mod.configure(self.bstack1llll11l1l1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1lllll1l_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1lll1l11l11_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll111l1ll_opy_:
            return
        self.__1llll111lll_opy_(data)
        bstack11lll1ll1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l1lll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢႋ")
        req.sdk_language = bstack1l1lll1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣႌ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1111111_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤ࡞ႍࠦ") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႎ"))
            r = self.bstack1llll11l1l1_opy_.StartBinSession(req)
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨႏ"), datetime.now() - bstack11lll1ll1_opy_)
            os.environ[bstack1lll11lll11_opy_] = r.bin_session_id
            self.__1lll111ll11_opy_(r)
            self.__1lllll1l111_opy_()
            self.bstack1111l11111_opy_.start()
            self.bstack1lll111l1ll_opy_ = True
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡡࠢ႐") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦ႑"))
        except grpc.bstack1llll11llll_opy_ as bstack1lll1l1l11l_opy_:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ႒") + str(bstack1lll1l1l11l_opy_) + bstack1l1lll1_opy_ (u"ࠣࠤ႓"))
            traceback.print_exc()
            raise bstack1lll1l1l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ႔") + str(e) + bstack1l1lll1_opy_ (u"ࠥࠦ႕"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lllll111l1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1llll11111l_opy_(self):
        if not self.bstack1l1l1l1l1l_opy_() or not self.cli_bin_session_id or self.bstack1llll11ll1l_opy_:
            return
        bstack11lll1ll1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ႖"), bstack1l1lll1_opy_ (u"ࠬ࠶ࠧ႗")))
        try:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡛ࠣ႘") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤ႙"))
            r = self.bstack1llll11l1l1_opy_.ConnectBinSession(req)
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧႚ"), datetime.now() - bstack11lll1ll1_opy_)
            self.__1lll111ll11_opy_(r)
            self.__1lllll1l111_opy_()
            self.bstack1111l11111_opy_.start()
            self.bstack1llll11ll1l_opy_ = True
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤ࡞ࠦႛ") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤႜ"))
        except grpc.bstack1llll11llll_opy_ as bstack1lll1l1l11l_opy_:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨႝ") + str(bstack1lll1l1l11l_opy_) + bstack1l1lll1_opy_ (u"ࠧࠨ႞"))
            traceback.print_exc()
            raise bstack1lll1l1l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ႟") + str(e) + bstack1l1lll1_opy_ (u"ࠢࠣႠ"))
            traceback.print_exc()
            raise e
    def __1lll111ll11_opy_(self, r):
        self.bstack1lll11llll1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l1lll1_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢႡ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l1lll1_opy_ (u"ࠤࡨࡱࡵࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡹࡳࡪࠢႢ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l1lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࡧࡾࠦࡩࡴࠢࡶࡩࡳࡺࠠࡰࡰ࡯ࡽࠥࡧࡳࠡࡲࡤࡶࡹࠦ࡯ࡧࠢࡷ࡬ࡪࠦࠢࡄࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠰ࠧࠦࡡ࡯ࡦࠣࡸ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡡ࡭ࡵࡲࠤࡺࡹࡥࡥࠢࡥࡽ࡙ࠥࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࡸࡥࡧࡱࡵࡩ࠱ࠦࡎࡰࡰࡨࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡩࡴࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧႣ")
        self.bstack1lllll11lll_opy_ = getattr(r, bstack1l1lll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪႤ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩႥ")] = self.config_testhub.jwt
        os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫႦ")] = self.config_testhub.build_hashed_id
    def bstack1lll1ll11l1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lllll1111l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll1ll111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll1ll111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1ll11l1_opy_(event_name=EVENTS.bstack1llll1l11l1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1llll1ll11l_opy_(self, bstack1lll1llll11_opy_=10):
        if self.bstack1lllll1111l_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤႧ"))
            return True
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢႨ"))
        if os.getenv(bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤႩ")) == bstack1lll11l1l1l_opy_:
            self.cli_bin_session_id = bstack1lll11l1l1l_opy_
            self.cli_listen_addr = bstack1l1lll1_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨႪ") % (self.cli_bin_session_id)
            self.bstack1lllll1111l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1llll111ll1_opy_, bstack1l1lll1_opy_ (u"ࠦࡸࡪ࡫ࠣႫ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1111l11_opy_ compat for text=True in bstack1lll11ll1l1_opy_ python
            encoding=bstack1l1lll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦႬ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll11l1ll1_opy_ = threading.Thread(target=self.__1ll1llll11l_opy_, args=(bstack1lll1llll11_opy_,))
        bstack1lll11l1ll1_opy_.start()
        bstack1lll11l1ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥႭ") + str(self.process.stderr.read()) + bstack1l1lll1_opy_ (u"ࠢࠣႮ"))
        if not self.bstack1lllll1111l_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣ࡝ࠥႯ") + str(id(self)) + bstack1l1lll1_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧႰ"))
            self.__1lll1l1ll1l_opy_()
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦႱ") + str(self.bstack1lllll1111l_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧႲ"))
        return self.bstack1lllll1111l_opy_
    def __1ll1llll11l_opy_(self, bstack1ll1llllll1_opy_=10):
        bstack1lll1l1llll_opy_ = time.time()
        while self.process and time.time() - bstack1lll1l1llll_opy_ < bstack1ll1llllll1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l1lll1_opy_ (u"ࠧ࡯ࡤ࠾ࠤႳ") in line:
                    self.cli_bin_session_id = line.split(bstack1l1lll1_opy_ (u"ࠨࡩࡥ࠿ࠥႴ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨႵ") + str(self.cli_bin_session_id) + bstack1l1lll1_opy_ (u"ࠣࠤႶ"))
                    continue
                if bstack1l1lll1_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥႷ") in line:
                    self.cli_listen_addr = line.split(bstack1l1lll1_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦႸ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢႹ") + str(self.cli_listen_addr) + bstack1l1lll1_opy_ (u"ࠧࠨႺ"))
                    continue
                if bstack1l1lll1_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧႻ") in line:
                    port = line.split(bstack1l1lll1_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨႼ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢႽ") + str(port) + bstack1l1lll1_opy_ (u"ࠤࠥႾ"))
                    continue
                if line.strip() == bstack1lll1l1l1l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l1lll1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧႿ"), bstack1l1lll1_opy_ (u"ࠦ࠶ࠨჀ")) == bstack1l1lll1_opy_ (u"ࠧ࠷ࠢჁ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lllll1111l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢჂ") + str(e) + bstack1l1lll1_opy_ (u"ࠢࠣჃ"))
        return False
    @measure(event_name=EVENTS.bstack1ll1lllll11_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def __1lll1l1ll1l_opy_(self):
        if self.bstack1ll1lll111l_opy_:
            self.bstack1111l11111_opy_.stop()
            start = datetime.now()
            if self.bstack1lll11l1lll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll11ll1l_opy_:
                    self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧჄ"), datetime.now() - start)
                else:
                    self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨჅ"), datetime.now() - start)
            self.__1llll11l111_opy_()
            start = datetime.now()
            self.bstack1ll1lll111l_opy_.close()
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧ჆"), datetime.now() - start)
            self.bstack1ll1lll111l_opy_ = None
        if self.process:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡸࡺ࡯ࡱࠤჇ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣ჈"), datetime.now() - start)
            self.process = None
            if self.bstack1lll111lll1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1l1l1111_opy_()
                self.logger.info(
                    bstack1l1lll1_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤ჉").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭჊")] = self.config_testhub.build_hashed_id
        self.bstack1lllll1111l_opy_ = False
    def __1llll111lll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l1lll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ჋")] = selenium.__version__
            data.frameworks.append(bstack1l1lll1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ჌"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l1lll1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢჍ")] = __version__
            data.frameworks.append(bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ჎"))
        except:
            pass
    def bstack1lll1ll111l_opy_(self, hub_url: str, platform_index: int, bstack111l1llll_opy_: Any):
        if self.bstack11111ll1l1_opy_:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤ჏"))
            return
        try:
            bstack11lll1ll1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l1lll1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣა")
            self.bstack11111ll1l1_opy_ = bstack1lll11l1l11_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1llll1111ll_opy_={bstack1l1lll1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦბ"): bstack111l1llll_opy_}
            )
            def bstack1ll1ll1l1ll_opy_(self):
                return
            if self.config.get(bstack1l1lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥგ"), True):
                Service.start = bstack1ll1ll1l1ll_opy_
                Service.stop = bstack1ll1ll1l1ll_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack1ll1lll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll11ll1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥდ"), datetime.now() - bstack11lll1ll1_opy_)
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤე") + str(e) + bstack1l1lll1_opy_ (u"ࠦࠧვ"))
    def bstack1lll11l11ll_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11lll1l1l_opy_
            self.bstack11111ll1l1_opy_ = bstack1ll1ll1llll_opy_(
                platform_index,
                framework_name=bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤზ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢთ") + str(e) + bstack1l1lll1_opy_ (u"ࠢࠣი"))
            pass
    def bstack1ll1ll1l1l1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥკ"))
            return
        if bstack1l1ll1lll1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l1lll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤლ"): pytest.__version__ }, [bstack1l1lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢმ")], self.bstack1111l11111_opy_, self.bstack1llll11l1l1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1llll1l111l_opy_({ bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦნ"): pytest.__version__ }, [bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧო")], self.bstack1111l11111_opy_, self.bstack1llll11l1l1_opy_)
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥპ") + str(e) + bstack1l1lll1_opy_ (u"ࠢࠣჟ"))
        self.bstack1llll1111l1_opy_()
    def bstack1llll1111l1_opy_(self):
        if not self.bstack11ll1llll_opy_():
            return
        bstack11ll1lll1l_opy_ = None
        def bstack1llll1lll_opy_(config, startdir):
            return bstack1l1lll1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨრ").format(bstack1l1lll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣს"))
        def bstack1l1lllll11_opy_():
            return
        def bstack11111l11l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l1lll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪტ"):
                return bstack1l1lll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥუ")
            else:
                return bstack11ll1lll1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11ll1lll1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1llll1lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lllll11_opy_
            Config.getoption = bstack11111l11l_opy_
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢფ") + str(e) + bstack1l1lll1_opy_ (u"ࠨࠢქ"))
    def bstack1llll11l1ll_opy_(self):
        bstack1ll1ll11l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll1ll11l1_opy_, dict):
            if cli.config_observability:
                bstack1ll1ll11l1_opy_.update(
                    {bstack1l1lll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢღ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l1lll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦყ") in accessibility.get(bstack1l1lll1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥშ"), {}):
                    bstack1lllll11l1l_opy_ = accessibility.get(bstack1l1lll1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦჩ"))
                    bstack1lllll11l1l_opy_.update({ bstack1l1lll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧც"): bstack1lllll11l1l_opy_.pop(bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣძ")) })
                bstack1ll1ll11l1_opy_.update({bstack1l1lll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨწ"): accessibility })
        return bstack1ll1ll11l1_opy_
    @measure(event_name=EVENTS.bstack1llll11lll1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1lll11l1lll_opy_(self, bstack1lll1l1l1ll_opy_: str = None, bstack1lll1l11111_opy_: str = None, bstack111llll1l_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll11l1l1_opy_:
            return
        bstack11lll1ll1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack111llll1l_opy_:
            req.bstack111llll1l_opy_ = bstack111llll1l_opy_
        if bstack1lll1l1l1ll_opy_:
            req.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
        if bstack1lll1l11111_opy_:
            req.bstack1lll1l11111_opy_ = bstack1lll1l11111_opy_
        try:
            r = self.bstack1llll11l1l1_opy_.StopBinSession(req)
            SDKCLI.bstack1llll1l1ll1_opy_ = r.bstack1llll1l1ll1_opy_
            SDKCLI.bstack11ll11ll1_opy_ = r.bstack11ll11ll1_opy_
            self.bstack1l1llll111_opy_(bstack1l1lll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣჭ"), datetime.now() - bstack11lll1ll1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l1llll111_opy_(self, key: str, value: timedelta):
        tag = bstack1l1lll1_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣხ") if self.bstack1l1l1l1l1l_opy_() else bstack1l1lll1_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣჯ")
        self.bstack1lll1l11lll_opy_[bstack1l1lll1_opy_ (u"ࠥ࠾ࠧჰ").join([tag + bstack1l1lll1_opy_ (u"ࠦ࠲ࠨჱ") + str(id(self)), key])] += value
    def bstack1l1l1l1111_opy_(self):
        if not os.getenv(bstack1l1lll1_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤჲ"), bstack1l1lll1_opy_ (u"ࠨ࠰ࠣჳ")) == bstack1l1lll1_opy_ (u"ࠢ࠲ࠤჴ"):
            return
        bstack1lll111llll_opy_ = dict()
        bstack1lllllll11l_opy_ = []
        if self.test_framework:
            bstack1lllllll11l_opy_.extend(list(self.test_framework.bstack1lllllll11l_opy_.values()))
        if self.bstack11111ll1l1_opy_:
            bstack1lllllll11l_opy_.extend(list(self.bstack11111ll1l1_opy_.bstack1lllllll11l_opy_.values()))
        for instance in bstack1lllllll11l_opy_:
            if not instance.platform_index in bstack1lll111llll_opy_:
                bstack1lll111llll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll111llll_opy_[instance.platform_index]
            for k, v in instance.bstack1llll111l1l_opy_().items():
                report[k] += v
                report[k.split(bstack1l1lll1_opy_ (u"ࠣ࠼ࠥჵ"))[0]] += v
        bstack1llll1llll1_opy_ = sorted([(k, v) for k, v in self.bstack1lll1l11lll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll1l111l1_opy_ = 0
        for r in bstack1llll1llll1_opy_:
            bstack1lllll11l11_opy_ = r[1].total_seconds()
            bstack1lll1l111l1_opy_ += bstack1lllll11l11_opy_
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢჶ") + str(bstack1lllll11l11_opy_) + bstack1l1lll1_opy_ (u"ࠥࠦჷ"))
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠦ࠲࠳ࠢჸ"))
        bstack1lll11l1111_opy_ = []
        for platform_index, report in bstack1lll111llll_opy_.items():
            bstack1lll11l1111_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll11l1111_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11ll1ll1_opy_ = set()
        bstack1lll111l1l1_opy_ = 0
        for r in bstack1lll11l1111_opy_:
            bstack1lllll11l11_opy_ = r[2].total_seconds()
            bstack1lll111l1l1_opy_ += bstack1lllll11l11_opy_
            bstack11ll1ll1_opy_.add(r[0])
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨჹ") + str(bstack1lllll11l11_opy_) + bstack1l1lll1_opy_ (u"ࠨࠢჺ"))
        if self.bstack1l1l1l1l1l_opy_():
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠢ࠮࠯ࠥ჻"))
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣჼ") + str(bstack1lll111l1l1_opy_) + bstack1l1lll1_opy_ (u"ࠤࠥჽ"))
        else:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢჾ") + str(bstack1lll1l111l1_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧჿ"))
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠧ࠳࠭ࠣᄀ"))
    def bstack1lll11llll1_opy_(self, r):
        if r is not None and getattr(r, bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࠧᄁ"), None) and getattr(r.testhub, bstack1l1lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᄂ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l1lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᄃ")))
            for bstack1lll1lll1ll_opy_, err in errors.items():
                if err[bstack1l1lll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᄄ")] == bstack1l1lll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᄅ"):
                    self.logger.info(err[bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᄆ")])
                else:
                    self.logger.error(err[bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄇ")])
    def bstack1l111l1lll_opy_(self):
        return SDKCLI.bstack1llll1l1ll1_opy_, SDKCLI.bstack11ll11ll1_opy_
cli = SDKCLI()