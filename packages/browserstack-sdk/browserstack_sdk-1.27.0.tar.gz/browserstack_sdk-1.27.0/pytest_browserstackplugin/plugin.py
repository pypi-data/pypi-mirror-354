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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l1l1lll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llllll11_opy_, bstack1ll111l1_opy_, update, bstack111l1llll_opy_,
                                       bstack1llll1lll_opy_, bstack1l1lllll11_opy_, bstack11ll1ll11l_opy_, bstack1ll111lll_opy_,
                                       bstack1l111ll11l_opy_, bstack1ll11lll_opy_, bstack11ll11l1l_opy_,
                                       bstack1l111ll1l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l11l_opy_)
from browserstack_sdk.bstack11111l1l1_opy_ import bstack1l111111ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l111111l_opy_
from bstack_utils.capture import bstack11l1111l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l11ll111l_opy_, bstack11ll1ll1ll_opy_, bstack11lll111l_opy_, \
    bstack1lll1lll1_opy_
from bstack_utils.helper import bstack1l1l1111l_opy_, bstack111l111l1l1_opy_, bstack111l1l11ll_opy_, bstack1ll11llll_opy_, bstack1l1llll1111_opy_, bstack11l1ll1lll_opy_, \
    bstack1111l1l1ll1_opy_, \
    bstack1111ll11l1l_opy_, bstack1l111l111l_opy_, bstack1l1l1l1l1_opy_, bstack1111l1111ll_opy_, bstack1l1ll1lll1_opy_, Notset, \
    bstack1lll1ll1l1_opy_, bstack11l11llll1l_opy_, bstack11111lll111_opy_, Result, bstack1111lll1111_opy_, bstack111l11l1111_opy_, bstack111ll111l1_opy_, \
    bstack1ll11ll11_opy_, bstack11111l1l_opy_, bstack11l11l111_opy_, bstack1111l1l111l_opy_
from bstack_utils.bstack11111l1l11l_opy_ import bstack11111l1llll_opy_
from bstack_utils.messages import bstack1lll1l1l11_opy_, bstack11ll1l1ll_opy_, bstack1111l1lll_opy_, bstack1lll11l1_opy_, bstack1l1ll1l11_opy_, \
    bstack1l1111l11l_opy_, bstack11l111l1l1_opy_, bstack11111ll1_opy_, bstack111l1l11l_opy_, bstack111l11l1l_opy_, \
    bstack1ll1ll1111_opy_, bstack1llll111l_opy_
from bstack_utils.proxy import bstack1l111ll111_opy_, bstack1l1l1lll_opy_
from bstack_utils.bstack1ll111l1l_opy_ import bstack11l1ll1llll_opy_, bstack11l1lll11ll_opy_, bstack11l1lll11l1_opy_, bstack11l1lll1lll_opy_, \
    bstack11l1llll11l_opy_, bstack11l1lll1111_opy_, bstack11l1llll1l1_opy_, bstack1lllll11ll_opy_, bstack11l1llll111_opy_
from bstack_utils.bstack1ll1111111_opy_ import bstack1lll1l111l_opy_
from bstack_utils.bstack1lll11llll_opy_ import bstack1ll1l11ll_opy_, bstack1l11l1l111_opy_, bstack1l11111l11_opy_, \
    bstack1l111ll1l_opy_, bstack1lll1llll_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack111lllll1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1ll1l1l_opy_
import bstack_utils.accessibility as bstack111l1ll1l_opy_
from bstack_utils.bstack111lll1l11_opy_ import bstack1lll11lll_opy_
from bstack_utils.bstack11l1l11l_opy_ import bstack11l1l11l_opy_
from bstack_utils.bstack1l1l1ll1ll_opy_ import bstack11ll1l1ll1_opy_
from browserstack_sdk.__init__ import bstack1l1lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1l1_opy_ import bstack1ll11l1l1_opy_, bstack11lll1l111_opy_, bstack11l1l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l11ll1_opy_, bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll11l1l1_opy_ import bstack1ll11l1l1_opy_, bstack11lll1l111_opy_, bstack11l1l1l11_opy_
bstack11lllll1_opy_ = None
bstack11l111l11l_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1l1111111l_opy_ = None
bstack11lll11l1_opy_ = None
bstack11lll11ll1_opy_ = None
bstack1l1lllll1l_opy_ = None
bstack11ll1ll1l1_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack111111l1_opy_ = None
bstack11ll1lll1l_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack1l111l1111_opy_ = None
bstack1l1111llll_opy_ = bstack1l1lll1_opy_ (u"࠭ࠧₐ")
CONFIG = {}
bstack1llll11l_opy_ = False
bstack11ll1llll1_opy_ = bstack1l1lll1_opy_ (u"ࠧࠨₑ")
bstack1llll1lll1_opy_ = bstack1l1lll1_opy_ (u"ࠨࠩₒ")
bstack11l11lll1l_opy_ = False
bstack1lll111l1l_opy_ = []
bstack1ll11lllll_opy_ = bstack1l11ll111l_opy_
bstack1llllll1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩₓ")
bstack1l111lll1_opy_ = {}
bstack1l1ll1ll1_opy_ = None
bstack11ll111111_opy_ = False
logger = bstack1l111111l_opy_.get_logger(__name__, bstack1ll11lllll_opy_)
store = {
    bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧₔ"): []
}
bstack1lllllllll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll111ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l11ll1_opy_(
    test_framework_name=bstack1ll1l11ll1_opy_[bstack1l1lll1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨₕ")] if bstack1l1ll1lll1_opy_() else bstack1ll1l11ll1_opy_[bstack1l1lll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬₖ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l111ll11_opy_(page, bstack11l1111l1_opy_):
    try:
        page.evaluate(bstack1l1lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢₗ"),
                      bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫₘ") + json.dumps(
                          bstack11l1111l1_opy_) + bstack1l1lll1_opy_ (u"ࠣࡿࢀࠦₙ"))
    except Exception as e:
        print(bstack1l1lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢₚ"), e)
def bstack11l11llll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1lll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦₛ"), bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩₜ") + json.dumps(
            message) + bstack1l1lll1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ₝") + json.dumps(level) + bstack1l1lll1_opy_ (u"࠭ࡽࡾࠩ₞"))
    except Exception as e:
        print(bstack1l1lll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ₟"), e)
def pytest_configure(config):
    global bstack11ll1llll1_opy_
    global CONFIG
    bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
    config.args = bstack11l1ll1l1l_opy_.bstack111llllllll_opy_(config.args)
    bstack111l111l1_opy_.bstack11l1l11lll_opy_(bstack11l11l111_opy_(config.getoption(bstack1l1lll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ₠"))))
    try:
        bstack1l111111l_opy_.bstack11111l111l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll11l1l1_opy_.invoke(bstack11lll1l111_opy_.CONNECT, bstack11l1l1l11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ₡"), bstack1l1lll1_opy_ (u"ࠪ࠴ࠬ₢")))
        config = json.loads(os.environ.get(bstack1l1lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ₣"), bstack1l1lll1_opy_ (u"ࠧࢁࡽࠣ₤")))
        cli.bstack1lll1ll111l_opy_(bstack1l1l1l1l1_opy_(bstack11ll1llll1_opy_, CONFIG), cli_context.platform_index, bstack111l1llll_opy_)
    if cli.bstack1ll1lll1l1l_opy_(bstack1llll1lllll_opy_):
        cli.bstack1ll1ll1l1l1_opy_()
        logger.debug(bstack1l1lll1_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ₥") + str(cli_context.platform_index) + bstack1l1lll1_opy_ (u"ࠢࠣ₦"))
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.BEFORE_ALL, bstack1lll11lllll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1lll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ₧"), None)
    if cli.is_running() and when == bstack1l1lll1_opy_ (u"ࠤࡦࡥࡱࡲࠢ₨"):
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.LOG_REPORT, bstack1lll11lllll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l1lll1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ₩"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1lll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ₪")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ₫"), bstack1l1lll1_opy_ (u"ࠨࡻࡾࠤ€")))
            if bstack11ll1l1ll1_opy_.bstack1lll1ll11l_opy_(config):
                bstack11lll1l1l1l_opy_ = bstack11ll1l1ll1_opy_.bstack11ll11l111_opy_(config)
                if item.execution_count > bstack11lll1l1l1l_opy_:
                    print(bstack1l1lll1_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡷ࠿ࠦࠧ₭"), report.nodeid, os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭₮")))
                    bstack11ll1l1ll1_opy_.bstack1111111l11l_opy_(report.nodeid)
            else:
                print(bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠩ₯"), report.nodeid, os.environ.get(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ₰")))
                bstack11ll1l1ll1_opy_.bstack1111111l11l_opy_(report.nodeid)
        else:
            print(bstack1l1lll1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡳࡥࡸࡹࡥࡥ࠼ࠣࠫ₱"), report.nodeid, os.environ.get(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ₲")))
    if cli.is_running():
        if when == bstack1l1lll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ₳"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.BEFORE_EACH, bstack1lll11lllll_opy_.POST, item, call, outcome)
        elif when == bstack1l1lll1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ₴"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.LOG_REPORT, bstack1lll11lllll_opy_.POST, item, call, outcome)
        elif when == bstack1l1lll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ₵"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.AFTER_EACH, bstack1lll11lllll_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llllll11ll1_opy_
    skipSessionName = item.config.getoption(bstack1l1lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ₶"))
    plugins = item.config.getoption(bstack1l1lll1_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ₷"))
    report = outcome.get_result()
    os.environ[bstack1l1lll1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ₸")] = report.nodeid
    bstack1lllllll11l1_opy_(item, call, report)
    if bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥ₹") not in plugins or bstack1l1ll1lll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1lll1_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢ₺"), None)
    page = getattr(item, bstack1l1lll1_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨ₻"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llllll1llll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llllll1ll1l_opy_(item, report, summary, skipSessionName)
def bstack1llllll1llll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ₼") and report.skipped:
        bstack11l1llll111_opy_(report)
    if report.when in [bstack1l1lll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ₽"), bstack1l1lll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ₾")]:
        return
    if not bstack1l1llll1111_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ₿")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ⃀") + json.dumps(
                    report.nodeid) + bstack1l1lll1_opy_ (u"࠭ࡽࡾࠩ⃁"))
        os.environ[bstack1l1lll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⃂")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1lll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣ⃃").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1lll1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⃄")))
    bstack1lll111111_opy_ = bstack1l1lll1_opy_ (u"ࠥࠦ⃅")
    bstack11l1llll111_opy_(report)
    if not passed:
        try:
            bstack1lll111111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1lll1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ⃆").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll111111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1lll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⃇")))
        bstack1lll111111_opy_ = bstack1l1lll1_opy_ (u"ࠨࠢ⃈")
        if not passed:
            try:
                bstack1lll111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1lll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ⃉").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll111111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ⃊")
                    + json.dumps(bstack1l1lll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥ⃋"))
                    + bstack1l1lll1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ⃌")
                )
            else:
                item._driver.execute_script(
                    bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ⃍")
                    + json.dumps(str(bstack1lll111111_opy_))
                    + bstack1l1lll1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ⃎")
                )
        except Exception as e:
            summary.append(bstack1l1lll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦ⃏").format(e))
def bstack1lllllll11ll_opy_(test_name, error_message):
    try:
        bstack11111111111_opy_ = []
        bstack1l1l11111_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⃐"), bstack1l1lll1_opy_ (u"ࠨ࠲ࠪ⃑"))
        bstack11llllll1_opy_ = {bstack1l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫⃒ࠧ"): test_name, bstack1l1lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ⃓ࠩ"): error_message, bstack1l1lll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ⃔"): bstack1l1l11111_opy_}
        bstack1lllllll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⃕"))
        if os.path.exists(bstack1lllllll1111_opy_):
            with open(bstack1lllllll1111_opy_) as f:
                bstack11111111111_opy_ = json.load(f)
        bstack11111111111_opy_.append(bstack11llllll1_opy_)
        with open(bstack1lllllll1111_opy_, bstack1l1lll1_opy_ (u"࠭ࡷࠨ⃖")) as f:
            json.dump(bstack11111111111_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬ⃗") + str(e))
def bstack1llllll1ll1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1lll1_opy_ (u"ࠣࡵࡨࡸࡺࡶ⃘ࠢ"), bstack1l1lll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱ⃙ࠦ")]:
        return
    if (str(skipSessionName).lower() != bstack1l1lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ⃚")):
        bstack1l111ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1lll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⃛")))
    bstack1lll111111_opy_ = bstack1l1lll1_opy_ (u"ࠧࠨ⃜")
    bstack11l1llll111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1lll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⃝").format(e)
                )
        try:
            if passed:
                bstack1lll1llll_opy_(getattr(item, bstack1l1lll1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⃞"), None), bstack1l1lll1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ⃟"))
            else:
                error_message = bstack1l1lll1_opy_ (u"ࠩࠪ⃠")
                if bstack1lll111111_opy_:
                    bstack11l11llll1_opy_(item._page, str(bstack1lll111111_opy_), bstack1l1lll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ⃡"))
                    bstack1lll1llll_opy_(getattr(item, bstack1l1lll1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ⃢"), None), bstack1l1lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ⃣"), str(bstack1lll111111_opy_))
                    error_message = str(bstack1lll111111_opy_)
                else:
                    bstack1lll1llll_opy_(getattr(item, bstack1l1lll1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⃤"), None), bstack1l1lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ⃥ࠢ"))
                bstack1lllllll11ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1lll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁ⃦ࠧ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1lll1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨ⃧"), default=bstack1l1lll1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ⃨"), help=bstack1l1lll1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ⃩"))
    parser.addoption(bstack1l1lll1_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶ⃪ࠦ"), default=bstack1l1lll1_opy_ (u"ࠨࡆࡢ࡮ࡶࡩ⃫ࠧ"), help=bstack1l1lll1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ⃬"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1lll1_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴ⃭ࠥ"), action=bstack1l1lll1_opy_ (u"ࠤࡶࡸࡴࡸࡥ⃮ࠣ"), default=bstack1l1lll1_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧ⃯ࠥ"),
                         help=bstack1l1lll1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥ⃰"))
def bstack111lll111l_opy_(log):
    if not (log[bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⃱")] and log[bstack1l1lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⃲")].strip()):
        return
    active = bstack111lll1lll_opy_()
    log = {
        bstack1l1lll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⃳"): log[bstack1l1lll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⃴")],
        bstack1l1lll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⃵"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"ࠪ࡞ࠬ⃶"),
        bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃷"): log[bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⃸")],
    }
    if active:
        if active[bstack1l1lll1_opy_ (u"࠭ࡴࡺࡲࡨࠫ⃹")] == bstack1l1lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⃺"):
            log[bstack1l1lll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃻")] = active[bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃼")]
        elif active[bstack1l1lll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⃽")] == bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⃾"):
            log[bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃿")] = active[bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭℀")]
    bstack1lll11lll_opy_.bstack1111ll111_opy_([log])
def bstack111lll1lll_opy_():
    if len(store[bstack1l1lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ℁")]) > 0 and store[bstack1l1lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬℂ")][-1]:
        return {
            bstack1l1lll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ℃"): bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ℄"),
            bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ℅"): store[bstack1l1lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ℆")][-1]
        }
    if store.get(bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪℇ"), None):
        return {
            bstack1l1lll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ℈"): bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭℉"),
            bstack1l1lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩℊ"): store[bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧℋ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.INIT_TEST, bstack1lll11lllll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.INIT_TEST, bstack1lll11lllll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llllllll1l1_opy_ = True
        bstack1l1l1l11l1_opy_ = bstack111l1ll1l_opy_.bstack11lll1111_opy_(bstack1111ll11l1l_opy_(item.own_markers))
        if not cli.bstack1ll1lll1l1l_opy_(bstack1llll1lllll_opy_):
            item._a11y_test_case = bstack1l1l1l11l1_opy_
            if bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪℌ"), None):
                driver = getattr(item, bstack1l1lll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ℍ"), None)
                item._a11y_started = bstack111l1ll1l_opy_.bstack1l111l1ll_opy_(driver, bstack1l1l1l11l1_opy_)
        if not bstack1lll11lll_opy_.on() or bstack1llllll1l1l1_opy_ != bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ℎ"):
            return
        global current_test_uuid #, bstack111llll1ll_opy_
        bstack111ll1111l_opy_ = {
            bstack1l1lll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬℏ"): uuid4().__str__(),
            bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬℐ"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"ࠩ࡝ࠫℑ")
        }
        current_test_uuid = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨℒ")]
        store[bstack1l1lll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨℓ")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ℔")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll111ll_opy_[item.nodeid] = {**_111ll111ll_opy_[item.nodeid], **bstack111ll1111l_opy_}
        bstack1111111111l_opy_(item, _111ll111ll_opy_[item.nodeid], bstack1l1lll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧℕ"))
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ№"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ℗")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.BEFORE_EACH, bstack1lll11lllll_opy_.PRE, item, bstack1l1lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ℘"))
    if bstack11ll1l1ll1_opy_.bstack1111111ll11_opy_():
            bstack1llllllll111_opy_ = bstack1l1lll1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡥࡸࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢℙ")
            logger.error(bstack1llllllll111_opy_)
            bstack111ll1111l_opy_ = {
                bstack1l1lll1_opy_ (u"ࠫࡺࡻࡩࡥࠩℚ"): uuid4().__str__(),
                bstack1l1lll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩℛ"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"࡚࠭ࠨℜ"),
                bstack1l1lll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬℝ"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"ࠨ࡜ࠪ℞"),
                bstack1l1lll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ℟"): bstack1l1lll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ℠"),
                bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ℡"): bstack1llllllll111_opy_,
                bstack1l1lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ™"): [],
                bstack1l1lll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ℣"): []
            }
            bstack1111111111l_opy_(item, bstack111ll1111l_opy_, bstack1l1lll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨℤ"))
            pytest.skip(bstack1llllllll111_opy_)
            return # skip all existing bstack1llllll11ll1_opy_
    global bstack1lllllllll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111l1111ll_opy_():
        atexit.register(bstack1ll111ll_opy_)
        if not bstack1lllllllll11_opy_:
            try:
                bstack1llllllll11l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111l1l111l_opy_():
                    bstack1llllllll11l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llllllll11l_opy_:
                    signal.signal(s, bstack1lllllllll1l_opy_)
                bstack1lllllllll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ℥") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l1ll1llll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩΩ")
    try:
        if not bstack1lll11lll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111ll1111l_opy_ = {
            bstack1l1lll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ℧"): uuid,
            bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨℨ"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"ࠬࡠࠧ℩"),
            bstack1l1lll1_opy_ (u"࠭ࡴࡺࡲࡨࠫK"): bstack1l1lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬÅ"),
            bstack1l1lll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫℬ"): bstack1l1lll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧℭ"),
            bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭℮"): bstack1l1lll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪℯ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩℰ")] = item
        store[bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪℱ")] = [uuid]
        if not _111ll111ll_opy_.get(item.nodeid, None):
            _111ll111ll_opy_[item.nodeid] = {bstack1l1lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Ⅎ"): [], bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪℳ"): []}
        _111ll111ll_opy_[item.nodeid][bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨℴ")].append(bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨℵ")])
        _111ll111ll_opy_[item.nodeid + bstack1l1lll1_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫℶ")] = bstack111ll1111l_opy_
        bstack1llllll1l1ll_opy_(item, bstack111ll1111l_opy_, bstack1l1lll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ℷ"))
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩℸ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.AFTER_EACH, bstack1lll11lllll_opy_.PRE, item, bstack1l1lll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩℹ"))
        return # skip all existing bstack1llllll11ll1_opy_
    try:
        global bstack1l111lll1_opy_
        bstack1l1l11111_opy_ = 0
        if bstack11l11lll1l_opy_ is True:
            bstack1l1l11111_opy_ = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ℺")))
        if bstack111lll11l_opy_.bstack1ll111ll1_opy_() == bstack1l1lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ℻"):
            if bstack111lll11l_opy_.bstack1l1ll111_opy_() == bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧℼ"):
                bstack1llllll11lll_opy_ = bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧℽ"), None)
                bstack111l11l1_opy_ = bstack1llllll11lll_opy_ + bstack1l1lll1_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣℾ")
                driver = getattr(item, bstack1l1lll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧℿ"), None)
                bstack11llll1111_opy_ = getattr(item, bstack1l1lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⅀"), None)
                bstack11l1ll1l11_opy_ = getattr(item, bstack1l1lll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⅁"), None)
                PercySDK.screenshot(driver, bstack111l11l1_opy_, bstack11llll1111_opy_=bstack11llll1111_opy_, bstack11l1ll1l11_opy_=bstack11l1ll1l11_opy_, bstack1lll11111l_opy_=bstack1l1l11111_opy_)
        if not cli.bstack1ll1lll1l1l_opy_(bstack1llll1lllll_opy_):
            if getattr(item, bstack1l1lll1_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ⅂"), False):
                bstack1l111111ll_opy_.bstack1l1l1ll1l_opy_(getattr(item, bstack1l1lll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⅃"), None), bstack1l111lll1_opy_, logger, item)
        if not bstack1lll11lll_opy_.on():
            return
        bstack111ll1111l_opy_ = {
            bstack1l1lll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⅄"): uuid4().__str__(),
            bstack1l1lll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩⅅ"): bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"࡚࠭ࠨⅆ"),
            bstack1l1lll1_opy_ (u"ࠧࡵࡻࡳࡩࠬⅇ"): bstack1l1lll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ⅈ"),
            bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬⅉ"): bstack1l1lll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⅊"),
            bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⅋"): bstack1l1lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⅌")
        }
        _111ll111ll_opy_[item.nodeid + bstack1l1lll1_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⅍")] = bstack111ll1111l_opy_
        bstack1llllll1l1ll_opy_(item, bstack111ll1111l_opy_, bstack1l1lll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅎ"))
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ⅏"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11l1lll1lll_opy_(fixturedef.argname):
        store[bstack1l1lll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ⅐")] = request.node
    elif bstack11l1llll11l_opy_(fixturedef.argname):
        store[bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⅑")] = request.node
    if not bstack1lll11lll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.SETUP_FIXTURE, bstack1lll11lllll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.SETUP_FIXTURE, bstack1lll11lllll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llllll11ll1_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.SETUP_FIXTURE, bstack1lll11lllll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.SETUP_FIXTURE, bstack1lll11lllll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llllll11ll1_opy_
    try:
        fixture = {
            bstack1l1lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⅒"): fixturedef.argname,
            bstack1l1lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⅓"): bstack1111l1l1ll1_opy_(outcome),
            bstack1l1lll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⅔"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⅕")]
        if not _111ll111ll_opy_.get(current_test_item.nodeid, None):
            _111ll111ll_opy_[current_test_item.nodeid] = {bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⅖"): []}
        _111ll111ll_opy_[current_test_item.nodeid][bstack1l1lll1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⅗")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1lll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭⅘"), str(err))
if bstack1l1ll1lll1_opy_() and bstack1lll11lll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.STEP, bstack1lll11lllll_opy_.PRE, request, step)
            return
        try:
            _111ll111ll_opy_[request.node.nodeid][bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⅙")].bstack11l11l1l1_opy_(id(step))
        except Exception as err:
            print(bstack1l1lll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ⅚"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.STEP, bstack1lll11lllll_opy_.POST, request, step, exception)
            return
        try:
            _111ll111ll_opy_[request.node.nodeid][bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⅛")].bstack111ll1llll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1lll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ⅜"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.STEP, bstack1lll11lllll_opy_.POST, request, step)
            return
        try:
            bstack111llllll1_opy_: bstack111lllll1l_opy_ = _111ll111ll_opy_[request.node.nodeid][bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⅝")]
            bstack111llllll1_opy_.bstack111ll1llll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1lll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭⅞"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llllll1l1l1_opy_
        try:
            if not bstack1lll11lll_opy_.on() or bstack1llllll1l1l1_opy_ != bstack1l1lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⅟"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.TEST, bstack1lll11lllll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪⅠ"), None)
            if not _111ll111ll_opy_.get(request.node.nodeid, None):
                _111ll111ll_opy_[request.node.nodeid] = {}
            bstack111llllll1_opy_ = bstack111lllll1l_opy_.bstack11l1l11l1ll_opy_(
                scenario, feature, request.node,
                name=bstack11l1lll1111_opy_(request.node, scenario),
                started_at=bstack11l1ll1lll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1lll1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧⅡ"),
                tags=bstack11l1llll1l1_opy_(feature, scenario),
                bstack11l111111l_opy_=bstack1lll11lll_opy_.bstack111lll11l1_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll111ll_opy_[request.node.nodeid][bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩⅢ")] = bstack111llllll1_opy_
            bstack1llllll1lll1_opy_(bstack111llllll1_opy_.uuid)
            bstack1lll11lll_opy_.bstack11l1111111_opy_(bstack1l1lll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅣ"), bstack111llllll1_opy_)
        except Exception as err:
            print(bstack1l1lll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪⅤ"), str(err))
def bstack1lllllll1lll_opy_(bstack111lll1l1l_opy_):
    if bstack111lll1l1l_opy_ in store[bstack1l1lll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭Ⅵ")]:
        store[bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧⅦ")].remove(bstack111lll1l1l_opy_)
def bstack1llllll1lll1_opy_(test_uuid):
    store[bstack1l1lll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨⅧ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1lll11lll_opy_.bstack11l11ll1111_opy_
def bstack1lllllll11l1_opy_(item, call, report):
    logger.debug(bstack1l1lll1_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧⅨ"))
    global bstack1llllll1l1l1_opy_
    bstack11l1llll11_opy_ = bstack11l1ll1lll_opy_()
    if hasattr(report, bstack1l1lll1_opy_ (u"࠭ࡳࡵࡱࡳࠫⅩ")):
        bstack11l1llll11_opy_ = bstack1111lll1111_opy_(report.stop)
    elif hasattr(report, bstack1l1lll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭Ⅺ")):
        bstack11l1llll11_opy_ = bstack1111lll1111_opy_(report.start)
    try:
        if getattr(report, bstack1l1lll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭Ⅻ"), bstack1l1lll1_opy_ (u"ࠩࠪⅬ")) == bstack1l1lll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨⅭ"):
            logger.debug(bstack1l1lll1_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭Ⅾ").format(getattr(report, bstack1l1lll1_opy_ (u"ࠬࡽࡨࡦࡰࠪⅯ"), bstack1l1lll1_opy_ (u"࠭ࠧⅰ")).__str__(), bstack1llllll1l1l1_opy_))
            if bstack1llllll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧⅱ"):
                _111ll111ll_opy_[item.nodeid][bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ⅲ")] = bstack11l1llll11_opy_
                bstack1111111111l_opy_(item, _111ll111ll_opy_[item.nodeid], bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫⅳ"), report, call)
                store[bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧⅴ")] = None
            elif bstack1llllll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣⅵ"):
                bstack111llllll1_opy_ = _111ll111ll_opy_[item.nodeid][bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨⅶ")]
                bstack111llllll1_opy_.set(hooks=_111ll111ll_opy_[item.nodeid].get(bstack1l1lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬⅷ"), []))
                exception, bstack111llll11l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111llll11l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1lll1_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭ⅸ"), bstack1l1lll1_opy_ (u"ࠨࠩⅹ"))]
                bstack111llllll1_opy_.stop(time=bstack11l1llll11_opy_, result=Result(result=getattr(report, bstack1l1lll1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪⅺ"), bstack1l1lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪⅻ")), exception=exception, bstack111llll11l_opy_=bstack111llll11l_opy_))
                bstack1lll11lll_opy_.bstack11l1111111_opy_(bstack1l1lll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ⅼ"), _111ll111ll_opy_[item.nodeid][bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨⅽ")])
        elif getattr(report, bstack1l1lll1_opy_ (u"࠭ࡷࡩࡧࡱࠫⅾ"), bstack1l1lll1_opy_ (u"ࠧࠨⅿ")) in [bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧↀ"), bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫↁ")]:
            logger.debug(bstack1l1lll1_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬↂ").format(getattr(report, bstack1l1lll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩↃ"), bstack1l1lll1_opy_ (u"ࠬ࠭ↄ")).__str__(), bstack1llllll1l1l1_opy_))
            bstack111lllll11_opy_ = item.nodeid + bstack1l1lll1_opy_ (u"࠭࠭ࠨↅ") + getattr(report, bstack1l1lll1_opy_ (u"ࠧࡸࡪࡨࡲࠬↆ"), bstack1l1lll1_opy_ (u"ࠨࠩↇ"))
            if getattr(report, bstack1l1lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪↈ"), False):
                hook_type = bstack1l1lll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ↉") if getattr(report, bstack1l1lll1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ↊"), bstack1l1lll1_opy_ (u"ࠬ࠭↋")) == bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ↌") else bstack1l1lll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ↍")
                _111ll111ll_opy_[bstack111lllll11_opy_] = {
                    bstack1l1lll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↎"): uuid4().__str__(),
                    bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↏"): bstack11l1llll11_opy_,
                    bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭←"): hook_type
                }
            _111ll111ll_opy_[bstack111lllll11_opy_][bstack1l1lll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ↑")] = bstack11l1llll11_opy_
            bstack1lllllll1lll_opy_(_111ll111ll_opy_[bstack111lllll11_opy_][bstack1l1lll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ→")])
            bstack1llllll1l1ll_opy_(item, _111ll111ll_opy_[bstack111lllll11_opy_], bstack1l1lll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ↓"), report, call)
            if getattr(report, bstack1l1lll1_opy_ (u"ࠧࡸࡪࡨࡲࠬ↔"), bstack1l1lll1_opy_ (u"ࠨࠩ↕")) == bstack1l1lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ↖"):
                if getattr(report, bstack1l1lll1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ↗"), bstack1l1lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ↘")) == bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ↙"):
                    bstack111ll1111l_opy_ = {
                        bstack1l1lll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↚"): uuid4().__str__(),
                        bstack1l1lll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↛"): bstack11l1ll1lll_opy_(),
                        bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭↜"): bstack11l1ll1lll_opy_()
                    }
                    _111ll111ll_opy_[item.nodeid] = {**_111ll111ll_opy_[item.nodeid], **bstack111ll1111l_opy_}
                    bstack1111111111l_opy_(item, _111ll111ll_opy_[item.nodeid], bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ↝"))
                    bstack1111111111l_opy_(item, _111ll111ll_opy_[item.nodeid], bstack1l1lll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ↞"), report, call)
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ↟"), str(err))
def bstack1llllll11l11_opy_(test, bstack111ll1111l_opy_, result=None, call=None, bstack11ll1ll11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llllll1_opy_ = {
        bstack1l1lll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ↠"): bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↡")],
        bstack1l1lll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ↢"): bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭↣"),
        bstack1l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ↤"): test.name,
        bstack1l1lll1_opy_ (u"ࠪࡦࡴࡪࡹࠨ↥"): {
            bstack1l1lll1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ↦"): bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ↧"),
            bstack1l1lll1_opy_ (u"࠭ࡣࡰࡦࡨࠫ↨"): inspect.getsource(test.obj)
        },
        bstack1l1lll1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ↩"): test.name,
        bstack1l1lll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ↪"): test.name,
        bstack1l1lll1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ↫"): bstack11l1ll1l1l_opy_.bstack111l11l1ll_opy_(test),
        bstack1l1lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭↬"): file_path,
        bstack1l1lll1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭↭"): file_path,
        bstack1l1lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ↮"): bstack1l1lll1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ↯"),
        bstack1l1lll1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ↰"): file_path,
        bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↱"): bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↲")],
        bstack1l1lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭↳"): bstack1l1lll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ↴"),
        bstack1l1lll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ↵"): {
            bstack1l1lll1_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ↶"): test.nodeid
        },
        bstack1l1lll1_opy_ (u"ࠧࡵࡣࡪࡷࠬ↷"): bstack1111ll11l1l_opy_(test.own_markers)
    }
    if bstack11ll1ll11_opy_ in [bstack1l1lll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ↸"), bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ↹")]:
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠪࡱࡪࡺࡡࠨ↺")] = {
            bstack1l1lll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭↻"): bstack111ll1111l_opy_.get(bstack1l1lll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ↼"), [])
        }
    if bstack11ll1ll11_opy_ == bstack1l1lll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ↽"):
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ↾")] = bstack1l1lll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ↿")
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⇀")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⇁")]
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⇂")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⇃")]
    if result:
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⇄")] = result.outcome
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⇅")] = result.duration * 1000
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⇆")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⇇")]
        if result.failed:
            bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⇈")] = bstack1lll11lll_opy_.bstack1111l111l1_opy_(call.excinfo.typename)
            bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⇉")] = bstack1lll11lll_opy_.bstack11l111lllll_opy_(call.excinfo, result)
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⇊")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⇋")]
    if outcome:
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⇌")] = bstack1111l1l1ll1_opy_(outcome)
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⇍")] = 0
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⇎")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⇏")]
        if bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⇐")] == bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⇑"):
            bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⇒")] = bstack1l1lll1_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⇓")  # bstack1lllllllllll_opy_
            bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⇔")] = [{bstack1l1lll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⇕"): [bstack1l1lll1_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⇖")]}]
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⇗")] = bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⇘")]
    return bstack111llllll1_opy_
def bstack1lllllll1l1l_opy_(test, bstack1111lllll1_opy_, bstack11ll1ll11_opy_, result, call, outcome, bstack111111111l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⇙")]
    hook_name = bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⇚")]
    hook_data = {
        bstack1l1lll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⇛"): bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇜")],
        bstack1l1lll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⇝"): bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⇞"),
        bstack1l1lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⇟"): bstack1l1lll1_opy_ (u"࠭ࡻࡾࠩ⇠").format(bstack11l1lll11ll_opy_(hook_name)),
        bstack1l1lll1_opy_ (u"ࠧࡣࡱࡧࡽࠬ⇡"): {
            bstack1l1lll1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⇢"): bstack1l1lll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⇣"),
            bstack1l1lll1_opy_ (u"ࠪࡧࡴࡪࡥࠨ⇤"): None
        },
        bstack1l1lll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⇥"): test.name,
        bstack1l1lll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⇦"): bstack11l1ll1l1l_opy_.bstack111l11l1ll_opy_(test, hook_name),
        bstack1l1lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⇧"): file_path,
        bstack1l1lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⇨"): file_path,
        bstack1l1lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇩"): bstack1l1lll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⇪"),
        bstack1l1lll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⇫"): file_path,
        bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⇬"): bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⇭")],
        bstack1l1lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⇮"): bstack1l1lll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⇯") if bstack1llllll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⇰") else bstack1l1lll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⇱"),
        bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⇲"): hook_type
    }
    bstack11l11lll111_opy_ = bstack111ll11l1l_opy_(_111ll111ll_opy_.get(test.nodeid, None))
    if bstack11l11lll111_opy_:
        hook_data[bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⇳")] = bstack11l11lll111_opy_
    if result:
        hook_data[bstack1l1lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⇴")] = result.outcome
        hook_data[bstack1l1lll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⇵")] = result.duration * 1000
        hook_data[bstack1l1lll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⇶")] = bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⇷")]
        if result.failed:
            hook_data[bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⇸")] = bstack1lll11lll_opy_.bstack1111l111l1_opy_(call.excinfo.typename)
            hook_data[bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⇹")] = bstack1lll11lll_opy_.bstack11l111lllll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⇺")] = bstack1111l1l1ll1_opy_(outcome)
        hook_data[bstack1l1lll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⇻")] = 100
        hook_data[bstack1l1lll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⇼")] = bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⇽")]
        if hook_data[bstack1l1lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇾")] == bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⇿"):
            hook_data[bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ∀")] = bstack1l1lll1_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ∁")  # bstack1lllllllllll_opy_
            hook_data[bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭∂")] = [{bstack1l1lll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ∃"): [bstack1l1lll1_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ∄")]}]
    if bstack111111111l1_opy_:
        hook_data[bstack1l1lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ∅")] = bstack111111111l1_opy_.result
        hook_data[bstack1l1lll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ∆")] = bstack11l11llll1l_opy_(bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ∇")], bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ∈")])
        hook_data[bstack1l1lll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ∉")] = bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ∊")]
        if hook_data[bstack1l1lll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ∋")] == bstack1l1lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ∌"):
            hook_data[bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ∍")] = bstack1lll11lll_opy_.bstack1111l111l1_opy_(bstack111111111l1_opy_.exception_type)
            hook_data[bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ∎")] = [{bstack1l1lll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ∏"): bstack11111lll111_opy_(bstack111111111l1_opy_.exception)}]
    return hook_data
def bstack1111111111l_opy_(test, bstack111ll1111l_opy_, bstack11ll1ll11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1lll1_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ∐").format(bstack11ll1ll11_opy_))
    bstack111llllll1_opy_ = bstack1llllll11l11_opy_(test, bstack111ll1111l_opy_, result, call, bstack11ll1ll11_opy_, outcome)
    driver = getattr(test, bstack1l1lll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ∑"), None)
    if bstack11ll1ll11_opy_ == bstack1l1lll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ−") and driver:
        bstack111llllll1_opy_[bstack1l1lll1_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ∓")] = bstack1lll11lll_opy_.bstack111lll11l1_opy_(driver)
    if bstack11ll1ll11_opy_ == bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ∔"):
        bstack11ll1ll11_opy_ = bstack1l1lll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ∕")
    bstack111l1l11l1_opy_ = {
        bstack1l1lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ∖"): bstack11ll1ll11_opy_,
        bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ∗"): bstack111llllll1_opy_
    }
    bstack1lll11lll_opy_.bstack11l1lll1l1_opy_(bstack111l1l11l1_opy_)
    if bstack11ll1ll11_opy_ == bstack1l1lll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ∘"):
        threading.current_thread().bstackTestMeta = {bstack1l1lll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ∙"): bstack1l1lll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ√")}
    elif bstack11ll1ll11_opy_ == bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ∛"):
        threading.current_thread().bstackTestMeta = {bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ∜"): getattr(result, bstack1l1lll1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ∝"), bstack1l1lll1_opy_ (u"ࠬ࠭∞"))}
def bstack1llllll1l1ll_opy_(test, bstack111ll1111l_opy_, bstack11ll1ll11_opy_, result=None, call=None, outcome=None, bstack111111111l1_opy_=None):
    logger.debug(bstack1l1lll1_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭∟").format(bstack11ll1ll11_opy_))
    hook_data = bstack1lllllll1l1l_opy_(test, bstack111ll1111l_opy_, bstack11ll1ll11_opy_, result, call, outcome, bstack111111111l1_opy_)
    bstack111l1l11l1_opy_ = {
        bstack1l1lll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ∠"): bstack11ll1ll11_opy_,
        bstack1l1lll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ∡"): hook_data
    }
    bstack1lll11lll_opy_.bstack11l1lll1l1_opy_(bstack111l1l11l1_opy_)
def bstack111ll11l1l_opy_(bstack111ll1111l_opy_):
    if not bstack111ll1111l_opy_:
        return None
    if bstack111ll1111l_opy_.get(bstack1l1lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ∢"), None):
        return getattr(bstack111ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭∣")], bstack1l1lll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ∤"), None)
    return bstack111ll1111l_opy_.get(bstack1l1lll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ∥"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.LOG, bstack1lll11lllll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_.LOG, bstack1lll11lllll_opy_.POST, request, caplog)
        return # skip all existing bstack1llllll11ll1_opy_
    try:
        if not bstack1lll11lll_opy_.on():
            return
        places = [bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ∦"), bstack1l1lll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ∧"), bstack1l1lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ∨")]
        logs = []
        for bstack1llllll1ll11_opy_ in places:
            records = caplog.get_records(bstack1llllll1ll11_opy_)
            bstack1llllll1l11l_opy_ = bstack1l1lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ∩") if bstack1llllll1ll11_opy_ == bstack1l1lll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ∪") else bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ∫")
            bstack1lllllll1ll1_opy_ = request.node.nodeid + (bstack1l1lll1_opy_ (u"ࠬ࠭∬") if bstack1llllll1ll11_opy_ == bstack1l1lll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ∭") else bstack1l1lll1_opy_ (u"ࠧ࠮ࠩ∮") + bstack1llllll1ll11_opy_)
            test_uuid = bstack111ll11l1l_opy_(_111ll111ll_opy_.get(bstack1lllllll1ll1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l11l1111_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1lll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ∯"): bstack111l111l1l1_opy_(record.created).isoformat() + bstack1l1lll1_opy_ (u"ࠩ࡝ࠫ∰"),
                    bstack1l1lll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ∱"): record.levelname,
                    bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ∲"): record.message,
                    bstack1llllll1l11l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1lll11lll_opy_.bstack1111ll111_opy_(logs)
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ∳"), str(err))
def bstack1llllll1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll111111_opy_
    bstack11l1ll11_opy_ = bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ∴"), None) and bstack1l1l1111l_opy_(
            threading.current_thread(), bstack1l1lll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭∵"), None)
    bstack1ll11l1111_opy_ = getattr(driver, bstack1l1lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ∶"), None) != None and getattr(driver, bstack1l1lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ∷"), None) == True
    if sequence == bstack1l1lll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ∸") and driver != None:
      if not bstack11ll111111_opy_ and bstack1l1llll1111_opy_() and bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ∹") in CONFIG and CONFIG[bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ∺")] == True and bstack11l1l11l_opy_.bstack1l1111ll11_opy_(driver_command) and (bstack1ll11l1111_opy_ or bstack11l1ll11_opy_) and not bstack1l111l11l_opy_(args):
        try:
          bstack11ll111111_opy_ = True
          logger.debug(bstack1l1lll1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ∻").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ∼").format(str(err)))
        bstack11ll111111_opy_ = False
    if sequence == bstack1l1lll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ∽"):
        if driver_command == bstack1l1lll1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭∾"):
            bstack1lll11lll_opy_.bstack1lll111l11_opy_({
                bstack1l1lll1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ∿"): response[bstack1l1lll1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ≀")],
                bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ≁"): store[bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ≂")]
            })
def bstack1ll111ll_opy_():
    global bstack1lll111l1l_opy_
    bstack1l111111l_opy_.bstack1ll11l111l_opy_()
    logging.shutdown()
    bstack1lll11lll_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllllllll1l_opy_(*args):
    global bstack1lll111l1l_opy_
    bstack1lll11lll_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l11ll_opy_, stage=STAGE.bstack1lllll111l_opy_, bstack1ll1llllll_opy_=bstack1l1ll1ll1_opy_)
def bstack11l1llll1l_opy_(self, *args, **kwargs):
    bstack1lll111l1_opy_ = bstack11lllll1_opy_(self, *args, **kwargs)
    bstack1ll11ll1ll_opy_ = getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ≃"), None)
    if bstack1ll11ll1ll_opy_ and bstack1ll11ll1ll_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ≄"), bstack1l1lll1_opy_ (u"ࠩࠪ≅")) == bstack1l1lll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ≆"):
        bstack1lll11lll_opy_.bstack1llllllll_opy_(self)
    return bstack1lll111l1_opy_
@measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.bstack1lll1lll1l_opy_, bstack1ll1llllll_opy_=bstack1l1ll1ll1_opy_)
def bstack1ll11l11_opy_(framework_name):
    from bstack_utils.config import Config
    bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
    if bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ≇")):
        return
    bstack111l111l1_opy_.bstack11l111ll1_opy_(bstack1l1lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ≈"), True)
    global bstack1l1111llll_opy_
    global bstack11lll1ll_opy_
    bstack1l1111llll_opy_ = framework_name
    logger.info(bstack1llll111l_opy_.format(bstack1l1111llll_opy_.split(bstack1l1lll1_opy_ (u"࠭࠭ࠨ≉"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1llll1111_opy_():
            Service.start = bstack11ll1ll11l_opy_
            Service.stop = bstack1ll111lll_opy_
            webdriver.Remote.get = bstack11l111ll_opy_
            webdriver.Remote.__init__ = bstack1ll1l1l1ll_opy_
            if not isinstance(os.getenv(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ≊")), str):
                return
            WebDriver.quit = bstack1l11111l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1lll11lll_opy_.on():
            webdriver.Remote.__init__ = bstack11l1llll1l_opy_
        bstack11lll1ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭≋")):
        bstack11lll1ll_opy_ = eval(os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ≌")))
    if not bstack11lll1ll_opy_:
        bstack1ll11lll_opy_(bstack1l1lll1_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ≍"), bstack1ll1ll1111_opy_)
    if bstack11llll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1lll1_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ≎")) and callable(getattr(RemoteConnection, bstack1l1lll1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭≏"))):
                RemoteConnection._get_proxy_url = bstack1l11l11ll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l11l11ll_opy_
        except Exception as e:
            logger.error(bstack1l1111l11l_opy_.format(str(e)))
    if bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭≐") in str(framework_name).lower():
        if not bstack1l1llll1111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1llll1lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lllll11_opy_
            Config.getoption = bstack11111l11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll1l111l1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1l1l_opy_, stage=STAGE.bstack1lllll111l_opy_, bstack1ll1llllll_opy_=bstack1l1ll1ll1_opy_)
def bstack1l11111l1_opy_(self):
    global bstack1l1111llll_opy_
    global bstack11ll11ll11_opy_
    global bstack11l111l11l_opy_
    try:
        if bstack1l1lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ≑") in bstack1l1111llll_opy_ and self.session_id != None and bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ≒"), bstack1l1lll1_opy_ (u"ࠩࠪ≓")) != bstack1l1lll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ≔"):
            bstack1llllllll1_opy_ = bstack1l1lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ≕") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ≖")
            bstack11111l1l_opy_(logger, True)
            if os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ≗"), None):
                self.execute_script(
                    bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ≘") + json.dumps(
                        os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ≙"))) + bstack1l1lll1_opy_ (u"ࠩࢀࢁࠬ≚"))
            if self != None:
                bstack1l111ll1l_opy_(self, bstack1llllllll1_opy_, bstack1l1lll1_opy_ (u"ࠪ࠰ࠥ࠭≛").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll1lll1l1l_opy_(bstack1llll1lllll_opy_):
            item = store.get(bstack1l1lll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ≜"), None)
            if item is not None and bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ≝"), None):
                bstack1l111111ll_opy_.bstack1l1l1ll1l_opy_(self, bstack1l111lll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1lll1_opy_ (u"࠭ࠧ≞")
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ≟") + str(e))
    bstack11l111l11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack111111111_opy_, stage=STAGE.bstack1lllll111l_opy_, bstack1ll1llllll_opy_=bstack1l1ll1ll1_opy_)
def bstack1ll1l1l1ll_opy_(self, command_executor,
             desired_capabilities=None, bstack11l1111lll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll11ll11_opy_
    global bstack1l1ll1ll1_opy_
    global bstack11l11lll1l_opy_
    global bstack1l1111llll_opy_
    global bstack11lllll1_opy_
    global bstack1lll111l1l_opy_
    global bstack11ll1llll1_opy_
    global bstack1llll1lll1_opy_
    global bstack1l111lll1_opy_
    CONFIG[bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ≠")] = str(bstack1l1111llll_opy_) + str(__version__)
    command_executor = bstack1l1l1l1l1_opy_(bstack11ll1llll1_opy_, CONFIG)
    logger.debug(bstack1lll11l1_opy_.format(command_executor))
    proxy = bstack1l111ll1l1_opy_(CONFIG, proxy)
    bstack1l1l11111_opy_ = 0
    try:
        if bstack11l11lll1l_opy_ is True:
            bstack1l1l11111_opy_ = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ≡")))
    except:
        bstack1l1l11111_opy_ = 0
    bstack11l111l1_opy_ = bstack1llllll11_opy_(CONFIG, bstack1l1l11111_opy_)
    logger.debug(bstack11111ll1_opy_.format(str(bstack11l111l1_opy_)))
    bstack1l111lll1_opy_ = CONFIG.get(bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭≢"))[bstack1l1l11111_opy_]
    if bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ≣") in CONFIG and CONFIG[bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ≤")]:
        bstack1l11111l11_opy_(bstack11l111l1_opy_, bstack1llll1lll1_opy_)
    if bstack111l1ll1l_opy_.bstack11l1ll111_opy_(CONFIG, bstack1l1l11111_opy_) and bstack111l1ll1l_opy_.bstack1ll111ll1l_opy_(bstack11l111l1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll1lll1l1l_opy_(bstack1llll1lllll_opy_):
            bstack111l1ll1l_opy_.set_capabilities(bstack11l111l1_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll111l_opy_ = bstack1ll111l1_opy_(desired_capabilities)
        bstack11ll111l_opy_[bstack1l1lll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭≥")] = bstack1lll1ll1l1_opy_(CONFIG)
        bstack11l1ll1111_opy_ = bstack1llllll11_opy_(bstack11ll111l_opy_)
        if bstack11l1ll1111_opy_:
            bstack11l111l1_opy_ = update(bstack11l1ll1111_opy_, bstack11l111l1_opy_)
        desired_capabilities = None
    if options:
        bstack1l111ll11l_opy_(options, bstack11l111l1_opy_)
    if not options:
        options = bstack111l1llll_opy_(bstack11l111l1_opy_)
    if proxy and bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ≦")):
        options.proxy(proxy)
    if options and bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ≧")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l111l111l_opy_() < version.parse(bstack1l1lll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ≨")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l111l1_opy_)
    logger.info(bstack1111l1lll_opy_)
    bstack11l1l1lll_opy_.end(EVENTS.bstack1l11l111l1_opy_.value, EVENTS.bstack1l11l111l1_opy_.value + bstack1l1lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ≩"),
                               EVENTS.bstack1l11l111l1_opy_.value + bstack1l1lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ≪"), True, None)
    if bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ≫")):
        bstack11lllll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ≬")):
        bstack11lllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11l1111lll_opy_=bstack11l1111lll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ≭")):
        bstack11lllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1111lll_opy_=bstack11l1111lll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11lllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11l1111lll_opy_=bstack11l1111lll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11ll1111l1_opy_ = bstack1l1lll1_opy_ (u"ࠨࠩ≮")
        if bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ≯")):
            bstack11ll1111l1_opy_ = self.caps.get(bstack1l1lll1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ≰"))
        else:
            bstack11ll1111l1_opy_ = self.capabilities.get(bstack1l1lll1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ≱"))
        if bstack11ll1111l1_opy_:
            bstack1ll11ll11_opy_(bstack11ll1111l1_opy_)
            if bstack1l111l111l_opy_() <= version.parse(bstack1l1lll1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ≲")):
                self.command_executor._url = bstack1l1lll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ≳") + bstack11ll1llll1_opy_ + bstack1l1lll1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ≴")
            else:
                self.command_executor._url = bstack1l1lll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ≵") + bstack11ll1111l1_opy_ + bstack1l1lll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ≶")
            logger.debug(bstack11ll1l1ll_opy_.format(bstack11ll1111l1_opy_))
        else:
            logger.debug(bstack1lll1l1l11_opy_.format(bstack1l1lll1_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦ≷")))
    except Exception as e:
        logger.debug(bstack1lll1l1l11_opy_.format(e))
    bstack11ll11ll11_opy_ = self.session_id
    if bstack1l1lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ≸") in bstack1l1111llll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ≹"), None)
        if item:
            bstack1llllllll1ll_opy_ = getattr(item, bstack1l1lll1_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ≺"), False)
            if not getattr(item, bstack1l1lll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ≻"), None) and bstack1llllllll1ll_opy_:
                setattr(store[bstack1l1lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ≼")], bstack1l1lll1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ≽"), self)
        bstack1ll11ll1ll_opy_ = getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ≾"), None)
        if bstack1ll11ll1ll_opy_ and bstack1ll11ll1ll_opy_.get(bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ≿"), bstack1l1lll1_opy_ (u"ࠬ࠭⊀")) == bstack1l1lll1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⊁"):
            bstack1lll11lll_opy_.bstack1llllllll_opy_(self)
    bstack1lll111l1l_opy_.append(self)
    if bstack1l1lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⊂") in CONFIG and bstack1l1lll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⊃") in CONFIG[bstack1l1lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⊄")][bstack1l1l11111_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⊅")][bstack1l1l11111_opy_][bstack1l1lll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⊆")]
    logger.debug(bstack111l11l1l_opy_.format(bstack11ll11ll11_opy_))
@measure(event_name=EVENTS.bstack1l11ll1l1_opy_, stage=STAGE.bstack1lllll111l_opy_, bstack1ll1llllll_opy_=bstack1l1ll1ll1_opy_)
def bstack11l111ll_opy_(self, url):
    global bstack1l1llll1ll_opy_
    global CONFIG
    try:
        bstack1l11l1l111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111l1l11l_opy_.format(str(err)))
    try:
        bstack1l1llll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11lll11111_opy_ = str(e)
            if any(err_msg in bstack11lll11111_opy_ for err_msg in bstack11lll111l_opy_):
                bstack1l11l1l111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111l1l11l_opy_.format(str(err)))
        raise e
def bstack1l111llll_opy_(item, when):
    global bstack1l1111l1ll_opy_
    try:
        bstack1l1111l1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l111l1_opy_(item, call, rep):
    global bstack1l111l1111_opy_
    global bstack1lll111l1l_opy_
    name = bstack1l1lll1_opy_ (u"ࠬ࠭⊇")
    try:
        if rep.when == bstack1l1lll1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⊈"):
            bstack11ll11ll11_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1lll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⊉"))
            try:
                if (str(skipSessionName).lower() != bstack1l1lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭⊊")):
                    name = str(rep.nodeid)
                    bstack1l1llllll_opy_ = bstack1ll1l11ll_opy_(bstack1l1lll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⊋"), name, bstack1l1lll1_opy_ (u"ࠪࠫ⊌"), bstack1l1lll1_opy_ (u"ࠫࠬ⊍"), bstack1l1lll1_opy_ (u"ࠬ࠭⊎"), bstack1l1lll1_opy_ (u"࠭ࠧ⊏"))
                    os.environ[bstack1l1lll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⊐")] = name
                    for driver in bstack1lll111l1l_opy_:
                        if bstack11ll11ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1llllll_opy_)
            except Exception as e:
                logger.debug(bstack1l1lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⊑").format(str(e)))
            try:
                bstack1lllll11ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⊒"):
                    status = bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⊓") if rep.outcome.lower() == bstack1l1lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⊔") else bstack1l1lll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⊕")
                    reason = bstack1l1lll1_opy_ (u"࠭ࠧ⊖")
                    if status == bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⊗"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1lll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭⊘") if status == bstack1l1lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⊙") else bstack1l1lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⊚")
                    data = name + bstack1l1lll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭⊛") if status == bstack1l1lll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⊜") else name + bstack1l1lll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ⊝") + reason
                    bstack111ll1l1l_opy_ = bstack1ll1l11ll_opy_(bstack1l1lll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ⊞"), bstack1l1lll1_opy_ (u"ࠨࠩ⊟"), bstack1l1lll1_opy_ (u"ࠩࠪ⊠"), bstack1l1lll1_opy_ (u"ࠪࠫ⊡"), level, data)
                    for driver in bstack1lll111l1l_opy_:
                        if bstack11ll11ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll1l1l_opy_)
            except Exception as e:
                logger.debug(bstack1l1lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⊢").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ⊣").format(str(e)))
    bstack1l111l1111_opy_(item, call, rep)
notset = Notset()
def bstack11111l11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11ll1lll1l_opy_
    if str(name).lower() == bstack1l1lll1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭⊤"):
        return bstack1l1lll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ⊥")
    else:
        return bstack11ll1lll1l_opy_(self, name, default, skip)
def bstack1l11l11ll_opy_(self):
    global CONFIG
    global bstack1l1lllll1l_opy_
    try:
        proxy = bstack1l111ll111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1lll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭⊦")):
                proxies = bstack1l1l1lll_opy_(proxy, bstack1l1l1l1l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11l11l1_opy_ = proxies.popitem()
                    if bstack1l1lll1_opy_ (u"ࠤ࠽࠳࠴ࠨ⊧") in bstack1ll11l11l1_opy_:
                        return bstack1ll11l11l1_opy_
                    else:
                        return bstack1l1lll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⊨") + bstack1ll11l11l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣ⊩").format(str(e)))
    return bstack1l1lllll1l_opy_(self)
def bstack11llll1l_opy_():
    return (bstack1l1lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⊪") in CONFIG or bstack1l1lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⊫") in CONFIG) and bstack1ll11llll_opy_() and bstack1l111l111l_opy_() >= version.parse(
        bstack11ll1ll1ll_opy_)
def bstack1l11ll111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1ll1ll1_opy_
    global bstack11l11lll1l_opy_
    global bstack1l1111llll_opy_
    CONFIG[bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⊬")] = str(bstack1l1111llll_opy_) + str(__version__)
    bstack1l1l11111_opy_ = 0
    try:
        if bstack11l11lll1l_opy_ is True:
            bstack1l1l11111_opy_ = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⊭")))
    except:
        bstack1l1l11111_opy_ = 0
    CONFIG[bstack1l1lll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ⊮")] = True
    bstack11l111l1_opy_ = bstack1llllll11_opy_(CONFIG, bstack1l1l11111_opy_)
    logger.debug(bstack11111ll1_opy_.format(str(bstack11l111l1_opy_)))
    if CONFIG.get(bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⊯")):
        bstack1l11111l11_opy_(bstack11l111l1_opy_, bstack1llll1lll1_opy_)
    if bstack1l1lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⊰") in CONFIG and bstack1l1lll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⊱") in CONFIG[bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⊲")][bstack1l1l11111_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1l1lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⊳")][bstack1l1l11111_opy_][bstack1l1lll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⊴")]
    import urllib
    import json
    if bstack1l1lll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⊵") in CONFIG and str(CONFIG[bstack1l1lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⊶")]).lower() != bstack1l1lll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ⊷"):
        bstack11llllll11_opy_ = bstack1l1lll1l1l_opy_()
        bstack1l1l11l1ll_opy_ = bstack11llllll11_opy_ + urllib.parse.quote(json.dumps(bstack11l111l1_opy_))
    else:
        bstack1l1l11l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ⊸") + urllib.parse.quote(json.dumps(bstack11l111l1_opy_))
    browser = self.connect(bstack1l1l11l1ll_opy_)
    return browser
def bstack1ll1111l1_opy_():
    global bstack11lll1ll_opy_
    global bstack1l1111llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11lll1l1l_opy_
        if not bstack1l1llll1111_opy_():
            global bstack11l11lllll_opy_
            if not bstack11l11lllll_opy_:
                from bstack_utils.helper import bstack1lll1111l_opy_, bstack1111lll1l_opy_
                bstack11l11lllll_opy_ = bstack1lll1111l_opy_()
                bstack1111lll1l_opy_(bstack1l1111llll_opy_)
            BrowserType.connect = bstack11lll1l1l_opy_
            return
        BrowserType.launch = bstack1l11ll111_opy_
        bstack11lll1ll_opy_ = True
    except Exception as e:
        pass
def bstack1llllll1l111_opy_():
    global CONFIG
    global bstack1llll11l_opy_
    global bstack11ll1llll1_opy_
    global bstack1llll1lll1_opy_
    global bstack11l11lll1l_opy_
    global bstack1ll11lllll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ⊹")))
    bstack1llll11l_opy_ = eval(os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ⊺")))
    bstack11ll1llll1_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ⊻"))
    bstack11ll11l1l_opy_(CONFIG, bstack1llll11l_opy_)
    bstack1ll11lllll_opy_ = bstack1l111111l_opy_.bstack11llllll_opy_(CONFIG, bstack1ll11lllll_opy_)
    if cli.bstack1l1l1l1l1l_opy_():
        bstack1ll11l1l1_opy_.invoke(bstack11lll1l111_opy_.CONNECT, bstack11l1l1l11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⊼"), bstack1l1lll1_opy_ (u"ࠪ࠴ࠬ⊽")))
        cli.bstack1lll11l11ll_opy_(cli_context.platform_index)
        cli.bstack1lll1ll111l_opy_(bstack1l1l1l1l1_opy_(bstack11ll1llll1_opy_, CONFIG), cli_context.platform_index, bstack111l1llll_opy_)
        cli.bstack1ll1ll1l1l1_opy_()
        logger.debug(bstack1l1lll1_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ⊾") + str(cli_context.platform_index) + bstack1l1lll1_opy_ (u"ࠧࠨ⊿"))
        return # skip all existing bstack1llllll11ll1_opy_
    global bstack11lllll1_opy_
    global bstack11l111l11l_opy_
    global bstack1l1ll111l1_opy_
    global bstack1l1111111l_opy_
    global bstack11lll11l1_opy_
    global bstack11lll11ll1_opy_
    global bstack11ll1ll1l1_opy_
    global bstack1l1llll1ll_opy_
    global bstack1l1lllll1l_opy_
    global bstack11ll1lll1l_opy_
    global bstack1l1111l1ll_opy_
    global bstack1l111l1111_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11lllll1_opy_ = webdriver.Remote.__init__
        bstack11l111l11l_opy_ = WebDriver.quit
        bstack11ll1ll1l1_opy_ = WebDriver.close
        bstack1l1llll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1lll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⋀") in CONFIG or bstack1l1lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⋁") in CONFIG) and bstack1ll11llll_opy_():
        if bstack1l111l111l_opy_() < version.parse(bstack11ll1ll1ll_opy_):
            logger.error(bstack11l111l1l1_opy_.format(bstack1l111l111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1lll1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⋂")) and callable(getattr(RemoteConnection, bstack1l1lll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⋃"))):
                    bstack1l1lllll1l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1lllll1l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1111l11l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11ll1lll1l_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1111l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1ll1l11_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l111l1111_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ⋄"))
    bstack1llll1lll1_opy_ = CONFIG.get(bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ⋅"), {}).get(bstack1l1lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⋆"))
    bstack11l11lll1l_opy_ = True
    bstack1ll11l11_opy_(bstack1lll1lll1_opy_)
if (bstack1111l1111ll_opy_()):
    bstack1llllll1l111_opy_()
@bstack111ll111l1_opy_(class_method=False)
def bstack1lllllll1l11_opy_(hook_name, event, bstack1l11l111l1l_opy_=None):
    if hook_name not in [bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⋇"), bstack1l1lll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⋈"), bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⋉"), bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⋊"), bstack1l1lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⋋"), bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⋌"), bstack1l1lll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ⋍"), bstack1l1lll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⋎")]:
        return
    node = store[bstack1l1lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⋏")]
    if hook_name in [bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⋐"), bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⋑")]:
        node = store[bstack1l1lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⋒")]
    elif hook_name in [bstack1l1lll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⋓"), bstack1l1lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⋔")]:
        node = store[bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ⋕")]
    hook_type = bstack11l1lll11l1_opy_(hook_name)
    if event == bstack1l1lll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ⋖"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_[hook_type], bstack1lll11lllll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1111lllll1_opy_ = {
            bstack1l1lll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⋗"): uuid,
            bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⋘"): bstack11l1ll1lll_opy_(),
            bstack1l1lll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⋙"): bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⋚"),
            bstack1l1lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⋛"): hook_type,
            bstack1l1lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⋜"): hook_name
        }
        store[bstack1l1lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⋝")].append(uuid)
        bstack1llllllllll1_opy_ = node.nodeid
        if hook_type == bstack1l1lll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⋞"):
            if not _111ll111ll_opy_.get(bstack1llllllllll1_opy_, None):
                _111ll111ll_opy_[bstack1llllllllll1_opy_] = {bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⋟"): []}
            _111ll111ll_opy_[bstack1llllllllll1_opy_][bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⋠")].append(bstack1111lllll1_opy_[bstack1l1lll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⋡")])
        _111ll111ll_opy_[bstack1llllllllll1_opy_ + bstack1l1lll1_opy_ (u"ࠬ࠳ࠧ⋢") + hook_name] = bstack1111lllll1_opy_
        bstack1llllll1l1ll_opy_(node, bstack1111lllll1_opy_, bstack1l1lll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⋣"))
    elif event == bstack1l1lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⋤"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll1lll1_opy_[hook_type], bstack1lll11lllll_opy_.POST, node, None, bstack1l11l111l1l_opy_)
            return
        bstack111lllll11_opy_ = node.nodeid + bstack1l1lll1_opy_ (u"ࠨ࠯ࠪ⋥") + hook_name
        _111ll111ll_opy_[bstack111lllll11_opy_][bstack1l1lll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⋦")] = bstack11l1ll1lll_opy_()
        bstack1lllllll1lll_opy_(_111ll111ll_opy_[bstack111lllll11_opy_][bstack1l1lll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⋧")])
        bstack1llllll1l1ll_opy_(node, _111ll111ll_opy_[bstack111lllll11_opy_], bstack1l1lll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⋨"), bstack111111111l1_opy_=bstack1l11l111l1l_opy_)
def bstack1llllll11l1l_opy_():
    global bstack1llllll1l1l1_opy_
    if bstack1l1ll1lll1_opy_():
        bstack1llllll1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⋩")
    else:
        bstack1llllll1l1l1_opy_ = bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⋪")
@bstack1lll11lll_opy_.bstack11l11ll1111_opy_
def bstack1lllllll111l_opy_():
    bstack1llllll11l1l_opy_()
    if cli.is_running():
        try:
            bstack11111l1llll_opy_(bstack1lllllll1l11_opy_)
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⋫").format(e))
        return
    if bstack1ll11llll_opy_():
        bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
        bstack1l1lll1_opy_ (u"ࠨࠩࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡁࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡧࡦࡶࡶࠤࡺࡹࡥࡥࠢࡩࡳࡷࠦࡡ࠲࠳ࡼࠤࡨࡵ࡭࡮ࡣࡱࡨࡸ࠳ࡷࡳࡣࡳࡴ࡮ࡴࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡹࠦࡩࡴࠢࡳࡥࡹࡩࡨࡦࡦࠣ࡭ࡳࠦࡡࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࠥ࡯ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡷࡶࠤࡼ࡫ࠠ࡯ࡧࡨࡨࠥࡺ࡯ࠡࡷࡶࡩ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࡐࡢࡶࡦ࡬࠭ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠪࠢࡩࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠩࠪࠫ⋬")
        if bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⋭")):
            if CONFIG.get(bstack1l1lll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⋮")) is not None and int(CONFIG[bstack1l1lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⋯")]) > 1:
                bstack1lll1l111l_opy_(bstack1llllll1l1_opy_)
            return
        bstack1lll1l111l_opy_(bstack1llllll1l1_opy_)
    try:
        bstack11111l1llll_opy_(bstack1lllllll1l11_opy_)
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ⋰").format(e))
bstack1lllllll111l_opy_()