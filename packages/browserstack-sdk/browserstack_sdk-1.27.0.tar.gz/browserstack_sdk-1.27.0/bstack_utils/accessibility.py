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
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111ll1lllll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111lllll11l_opy_ as bstack111lll11l11_opy_, EVENTS
from bstack_utils.bstack11l1l11l_opy_ import bstack11l1l11l_opy_
from bstack_utils.helper import bstack11l1ll1lll_opy_, bstack111l1l11ll_opy_, bstack11ll1llll_opy_, bstack11l111ll11l_opy_, \
  bstack11l111ll111_opy_, bstack1111ll11_opy_, get_host_info, bstack11l1111ll1l_opy_, bstack1lll1l1ll1_opy_, bstack111ll111l1_opy_, bstack111ll1ll1ll_opy_, bstack111lll1l111_opy_, bstack1l1l1111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l111111l_opy_ import get_logger
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11l1l1lll_opy_ = bstack1lll11l11l1_opy_()
@bstack111ll111l1_opy_(class_method=False)
def _111lll11ll1_opy_(driver, bstack1111ll11l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1lll1_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ᢩࠧ"): caps.get(bstack1l1lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᢪ"), None),
        bstack1l1lll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᢫"): bstack1111ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᢬"), None),
        bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ᢭"): caps.get(bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᢮"), None),
        bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᢯"): caps.get(bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᢰ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1lll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᢱ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᢲ"), None) is None or os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᢳ")] == bstack1l1lll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᢴ"):
        return False
    return True
def bstack1111ll1ll_opy_(config):
  return config.get(bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᢵ"), False) or any([p.get(bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᢶ"), False) == True for p in config.get(bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᢷ"), [])])
def bstack11l1ll111_opy_(config, bstack1l1l11111_opy_):
  try:
    bstack111lll111l1_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᢸ"), False)
    if int(bstack1l1l11111_opy_) < len(config.get(bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᢹ"), [])) and config[bstack1l1lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᢺ")][bstack1l1l11111_opy_]:
      bstack111ll1llll1_opy_ = config[bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᢻ")][bstack1l1l11111_opy_].get(bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᢼ"), None)
    else:
      bstack111ll1llll1_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᢽ"), None)
    if bstack111ll1llll1_opy_ != None:
      bstack111lll111l1_opy_ = bstack111ll1llll1_opy_
    bstack111ll1ll111_opy_ = os.getenv(bstack1l1lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᢾ")) is not None and len(os.getenv(bstack1l1lll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᢿ"))) > 0 and os.getenv(bstack1l1lll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᣀ")) != bstack1l1lll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᣁ")
    return bstack111lll111l1_opy_ and bstack111ll1ll111_opy_
  except Exception as error:
    logger.debug(bstack1l1lll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᣂ") + str(error))
  return False
def bstack11lll1111_opy_(test_tags):
  bstack1ll11ll1lll_opy_ = os.getenv(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᣃ"))
  if bstack1ll11ll1lll_opy_ is None:
    return True
  bstack1ll11ll1lll_opy_ = json.loads(bstack1ll11ll1lll_opy_)
  try:
    include_tags = bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᣄ")] if bstack1l1lll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᣅ") in bstack1ll11ll1lll_opy_ and isinstance(bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᣆ")], list) else []
    exclude_tags = bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᣇ")] if bstack1l1lll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᣈ") in bstack1ll11ll1lll_opy_ and isinstance(bstack1ll11ll1lll_opy_[bstack1l1lll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᣉ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᣊ") + str(error))
  return False
def bstack111lll111ll_opy_(config, bstack111lll1ll1l_opy_, bstack111llll1lll_opy_, bstack111lll11l1l_opy_):
  bstack11l11l1l1l1_opy_ = bstack11l111ll11l_opy_(config)
  bstack11l11ll11l1_opy_ = bstack11l111ll111_opy_(config)
  if bstack11l11l1l1l1_opy_ is None or bstack11l11ll11l1_opy_ is None:
    logger.error(bstack1l1lll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᣋ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᣌ"), bstack1l1lll1_opy_ (u"ࠧࡼࡿࠪᣍ")))
    data = {
        bstack1l1lll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᣎ"): config[bstack1l1lll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᣏ")],
        bstack1l1lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᣐ"): config.get(bstack1l1lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᣑ"), os.path.basename(os.getcwd())),
        bstack1l1lll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨᣒ"): bstack11l1ll1lll_opy_(),
        bstack1l1lll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᣓ"): config.get(bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᣔ"), bstack1l1lll1_opy_ (u"ࠨࠩᣕ")),
        bstack1l1lll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᣖ"): {
            bstack1l1lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪᣗ"): bstack111lll1ll1l_opy_,
            bstack1l1lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᣘ"): bstack111llll1lll_opy_,
            bstack1l1lll1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᣙ"): __version__,
            bstack1l1lll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᣚ"): bstack1l1lll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᣛ"),
            bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᣜ"): bstack1l1lll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᣝ"),
            bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᣞ"): bstack111lll11l1l_opy_
        },
        bstack1l1lll1_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᣟ"): settings,
        bstack1l1lll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ᣠ"): bstack11l1111ll1l_opy_(),
        bstack1l1lll1_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ᣡ"): bstack1111ll11_opy_(),
        bstack1l1lll1_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩᣢ"): get_host_info(),
        bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᣣ"): bstack11ll1llll_opy_(config)
    }
    headers = {
        bstack1l1lll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᣤ"): bstack1l1lll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᣥ"),
    }
    config = {
        bstack1l1lll1_opy_ (u"ࠫࡦࡻࡴࡩࠩᣦ"): (bstack11l11l1l1l1_opy_, bstack11l11ll11l1_opy_),
        bstack1l1lll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᣧ"): headers
    }
    response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"࠭ࡐࡐࡕࡗࠫᣨ"), bstack111lll11l11_opy_ + bstack1l1lll1_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᣩ"), data, config)
    bstack11l11ll11ll_opy_ = response.json()
    if bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᣪ")]:
      parsed = json.loads(os.getenv(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᣫ"), bstack1l1lll1_opy_ (u"ࠪࡿࢂ࠭ᣬ")))
      parsed[bstack1l1lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᣭ")] = bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠬࡪࡡࡵࡣࠪᣮ")][bstack1l1lll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᣯ")]
      os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᣰ")] = json.dumps(parsed)
      bstack11l1l11l_opy_.bstack1lllllll1l_opy_(bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᣱ")][bstack1l1lll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᣲ")])
      bstack11l1l11l_opy_.bstack11l11l1l111_opy_(bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠪࡨࡦࡺࡡࠨᣳ")][bstack1l1lll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᣴ")])
      bstack11l1l11l_opy_.store()
      return bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠬࡪࡡࡵࡣࠪᣵ")][bstack1l1lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ᣶")], bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡣࡷࡥࠬ᣷")][bstack1l1lll1_opy_ (u"ࠨ࡫ࡧࠫ᣸")]
    else:
      logger.error(bstack1l1lll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪ᣹") + bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᣺")])
      if bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᣻")] == bstack1l1lll1_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧ᣼"):
        for bstack111lll1lll1_opy_ in bstack11l11ll11ll_opy_[bstack1l1lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭᣽")]:
          logger.error(bstack111lll1lll1_opy_[bstack1l1lll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᣾")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤ᣿") +  str(error))
    return None, None
def bstack111llll111l_opy_():
  if os.getenv(bstack1l1lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᤀ")) is None:
    return {
        bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᤁ"): bstack1l1lll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᤂ"),
        bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᤃ"): bstack1l1lll1_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᤄ")
    }
  data = {bstack1l1lll1_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᤅ"): bstack11l1ll1lll_opy_()}
  headers = {
      bstack1l1lll1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᤆ"): bstack1l1lll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᤇ") + os.getenv(bstack1l1lll1_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᤈ")),
      bstack1l1lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᤉ"): bstack1l1lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᤊ")
  }
  response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"࠭ࡐࡖࡖࠪᤋ"), bstack111lll11l11_opy_ + bstack1l1lll1_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩᤌ"), data, { bstack1l1lll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᤍ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1lll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥᤎ") + bstack111l1l11ll_opy_().isoformat() + bstack1l1lll1_opy_ (u"ࠪ࡞ࠬᤏ"))
      return {bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᤐ"): bstack1l1lll1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᤑ"), bstack1l1lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᤒ"): bstack1l1lll1_opy_ (u"ࠧࠨᤓ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᤔ") + str(error))
    return {
        bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᤕ"): bstack1l1lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᤖ"),
        bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᤗ"): str(error)
    }
def bstack111lllll111_opy_(bstack111lll11lll_opy_):
    return re.match(bstack1l1lll1_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭ᤘ"), bstack111lll11lll_opy_.strip()) is not None
def bstack1ll111ll1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111lll11111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111lll11111_opy_ = desired_capabilities
        else:
          bstack111lll11111_opy_ = {}
        bstack111lll1l1l1_opy_ = (bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᤙ"), bstack1l1lll1_opy_ (u"ࠧࠨᤚ")).lower() or caps.get(bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᤛ"), bstack1l1lll1_opy_ (u"ࠩࠪᤜ")).lower())
        if bstack111lll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠪ࡭ࡴࡹࠧᤝ"):
            return True
        if bstack111lll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᤞ"):
            bstack111llll1l11_opy_ = str(float(caps.get(bstack1l1lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᤟")) or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᤠ"), {}).get(bstack1l1lll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᤡ"),bstack1l1lll1_opy_ (u"ࠨࠩᤢ"))))
            if bstack111lll1l1l1_opy_ == bstack1l1lll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᤣ") and int(bstack111llll1l11_opy_.split(bstack1l1lll1_opy_ (u"ࠪ࠲ࠬᤤ"))[0]) < float(bstack111ll1ll1l1_opy_):
                logger.warning(str(bstack111ll1lll11_opy_))
                return False
            return True
        bstack1ll1ll11111_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᤥ"), {}).get(bstack1l1lll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᤦ"), caps.get(bstack1l1lll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᤧ"), bstack1l1lll1_opy_ (u"ࠧࠨᤨ")))
        if bstack1ll1ll11111_opy_:
            logger.warning(bstack1l1lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᤩ"))
            return False
        browser = caps.get(bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᤪ"), bstack1l1lll1_opy_ (u"ࠪࠫᤫ")).lower() or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᤬"), bstack1l1lll1_opy_ (u"ࠬ࠭᤭")).lower()
        if browser != bstack1l1lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᤮"):
            logger.warning(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᤯"))
            return False
        browser_version = caps.get(bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᤰ")) or caps.get(bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᤱ")) or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᤲ")) or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᤳ"), {}).get(bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᤴ")) or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᤵ"), {}).get(bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᤶ"))
        bstack1ll1l111lll_opy_ = bstack111ll1lllll_opy_.bstack1ll11lll1l1_opy_
        bstack111ll1lll1l_opy_ = False
        if config is not None:
          bstack111ll1lll1l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᤷ") in config and str(config[bstack1l1lll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᤸ")]).lower() != bstack1l1lll1_opy_ (u"ࠪࡪࡦࡲࡳࡦ᤹ࠩ")
        if os.environ.get(bstack1l1lll1_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᤺"), bstack1l1lll1_opy_ (u"᤻ࠬ࠭")).lower() == bstack1l1lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ᤼") or bstack111ll1lll1l_opy_:
          bstack1ll1l111lll_opy_ = bstack111ll1lllll_opy_.bstack1ll1l1ll111_opy_
        if browser_version and browser_version != bstack1l1lll1_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ᤽") and int(browser_version.split(bstack1l1lll1_opy_ (u"ࠨ࠰ࠪ᤾"))[0]) <= bstack1ll1l111lll_opy_:
          logger.warning(bstack1ll1lll1ll1_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࡲ࡯࡮ࡠࡣ࠴࠵ࡾࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡹࡩࡷࡹࡩࡰࡰࢀ࠲ࠬ᤿"))
          return False
        if not options:
          bstack1ll1l1l111l_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᥀")) or bstack111lll11111_opy_.get(bstack1l1lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥁"), {})
          if bstack1l1lll1_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ᥂") in bstack1ll1l1l111l_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ᥃"), []):
              logger.warning(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ᥄"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥ᥅") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lllll11l1l_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥆"), {})
    bstack1lllll11l1l_opy_[bstack1l1lll1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭᥇")] = os.getenv(bstack1l1lll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᥈"))
    bstack111llll11ll_opy_ = json.loads(os.getenv(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᥉"), bstack1l1lll1_opy_ (u"࠭ࡻࡾࠩ᥊"))).get(bstack1l1lll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᥋"))
    if not config[bstack1l1lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᥌")].get(bstack1l1lll1_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ᥍")):
      if bstack1l1lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᥎") in caps:
        caps[bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᥏")][bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᥐ")] = bstack1lllll11l1l_opy_
        caps[bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᥑ")][bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᥒ")][bstack1l1lll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᥓ")] = bstack111llll11ll_opy_
      else:
        caps[bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᥔ")] = bstack1lllll11l1l_opy_
        caps[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᥕ")][bstack1l1lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᥖ")] = bstack111llll11ll_opy_
  except Exception as error:
    logger.debug(bstack1l1lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨᥗ") +  str(error))
def bstack1l111l1ll_opy_(driver, bstack111lll1ll11_opy_):
  try:
    setattr(driver, bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᥘ"), True)
    session = driver.session_id
    if session:
      bstack111lll1l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111lll1l11l_opy_ = False
      bstack111lll1l11l_opy_ = url.scheme in [bstack1l1lll1_opy_ (u"ࠢࡩࡶࡷࡴࠧᥙ"), bstack1l1lll1_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᥚ")]
      if bstack111lll1l11l_opy_:
        if bstack111lll1ll11_opy_:
          logger.info(bstack1l1lll1_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤᥛ"))
      return bstack111lll1ll11_opy_
  except Exception as e:
    logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᥜ") + str(e))
    return False
def bstack1l11ll1lll_opy_(driver, name, path):
  try:
    bstack1ll1l1ll1ll_opy_ = {
        bstack1l1lll1_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᥝ"): threading.current_thread().current_test_uuid,
        bstack1l1lll1_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᥞ"): os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᥟ"), bstack1l1lll1_opy_ (u"ࠧࠨᥠ")),
        bstack1l1lll1_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᥡ"): os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᥢ"), bstack1l1lll1_opy_ (u"ࠪࠫᥣ"))
    }
    bstack1ll1l11l111_opy_ = bstack11l1l1lll_opy_.bstack1ll11ll1ll1_opy_(EVENTS.bstack1ll11llll1_opy_.value)
    logger.debug(bstack1l1lll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᥤ"))
    try:
      if (bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᥥ"), None) and bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᥦ"), None)):
        scripts = {bstack1l1lll1_opy_ (u"ࠧࡴࡥࡤࡲࠬᥧ"): bstack11l1l11l_opy_.perform_scan}
        bstack111llll1ll1_opy_ = json.loads(scripts[bstack1l1lll1_opy_ (u"ࠣࡵࡦࡥࡳࠨᥨ")].replace(bstack1l1lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᥩ"), bstack1l1lll1_opy_ (u"ࠥࠦᥪ")))
        bstack111llll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᥫ")][bstack1l1lll1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᥬ")] = None
        scripts[bstack1l1lll1_opy_ (u"ࠨࡳࡤࡣࡱࠦᥭ")] = bstack1l1lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ᥮") + json.dumps(bstack111llll1ll1_opy_)
        bstack11l1l11l_opy_.bstack1lllllll1l_opy_(scripts)
        bstack11l1l11l_opy_.store()
        logger.debug(driver.execute_script(bstack11l1l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11l1l11l_opy_.perform_scan, {bstack1l1lll1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ᥯"): name}))
      bstack11l1l1lll_opy_.end(EVENTS.bstack1ll11llll1_opy_.value, bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᥰ"), bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᥱ"), True, None)
    except Exception as error:
      bstack11l1l1lll_opy_.end(EVENTS.bstack1ll11llll1_opy_.value, bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᥲ"), bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᥳ"), False, str(error))
    bstack1ll1l11l111_opy_ = bstack11l1l1lll_opy_.bstack11ll111l1ll_opy_(EVENTS.bstack1ll11ll1l11_opy_.value)
    bstack11l1l1lll_opy_.mark(bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᥴ"))
    try:
      if (bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᥵"), None) and bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᥶"), None)):
        scripts = {bstack1l1lll1_opy_ (u"ࠩࡶࡧࡦࡴࠧ᥷"): bstack11l1l11l_opy_.perform_scan}
        bstack111llll1ll1_opy_ = json.loads(scripts[bstack1l1lll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᥸")].replace(bstack1l1lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ᥹"), bstack1l1lll1_opy_ (u"ࠧࠨ᥺")))
        bstack111llll1ll1_opy_[bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᥻")][bstack1l1lll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ᥼")] = None
        scripts[bstack1l1lll1_opy_ (u"ࠣࡵࡦࡥࡳࠨ᥽")] = bstack1l1lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ᥾") + json.dumps(bstack111llll1ll1_opy_)
        bstack11l1l11l_opy_.bstack1lllllll1l_opy_(scripts)
        bstack11l1l11l_opy_.store()
        logger.debug(driver.execute_script(bstack11l1l11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11l1l11l_opy_.bstack111llll1l1l_opy_, bstack1ll1l1ll1ll_opy_))
      bstack11l1l1lll_opy_.end(bstack1ll1l11l111_opy_, bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᥿"), bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᦀ"),True, None)
    except Exception as error:
      bstack11l1l1lll_opy_.end(bstack1ll1l11l111_opy_, bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᦁ"), bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᦂ"),False, str(error))
    logger.info(bstack1l1lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᦃ"))
  except Exception as bstack1ll11lll111_opy_:
    logger.error(bstack1l1lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᦄ") + str(path) + bstack1l1lll1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᦅ") + str(bstack1ll11lll111_opy_))
def bstack111ll1ll11l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1lll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᦆ")) and str(caps.get(bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᦇ"))).lower() == bstack1l1lll1_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᦈ"):
        bstack111llll1l11_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᦉ")) or caps.get(bstack1l1lll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᦊ"))
        if bstack111llll1l11_opy_ and int(str(bstack111llll1l11_opy_)) < bstack111ll1ll1l1_opy_:
            return False
    return True
def bstack1ll111111l_opy_(config):
  if bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᦋ") in config:
        return config[bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᦌ")]
  for platform in config.get(bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᦍ"), []):
      if bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᦎ") in platform:
          return platform[bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᦏ")]
  return None
def bstack111ll11ll_opy_(bstack1l11l11111_opy_):
  try:
    browser_name = bstack1l11l11111_opy_[bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᦐ")]
    browser_version = bstack1l11l11111_opy_[bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᦑ")]
    chrome_options = bstack1l11l11111_opy_[bstack1l1lll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩᦒ")]
    try:
        bstack111lll1111l_opy_ = int(browser_version.split(bstack1l1lll1_opy_ (u"ࠩ࠱ࠫᦓ"))[0])
    except ValueError as e:
        logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢᦔ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1lll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᦕ")):
        logger.warning(bstack1l1lll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᦖ"))
        return False
    if bstack111lll1111l_opy_ < bstack111ll1lllll_opy_.bstack1ll1l1ll111_opy_:
        logger.warning(bstack1ll1lll1ll1_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧᦗ"))
        return False
    if chrome_options and any(bstack1l1lll1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᦘ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l1lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᦙ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢᦚ") + str(e))
    return False
def bstack111111lll_opy_(bstack1ll1111l_opy_, config):
    try:
      bstack1ll1l1ll11l_opy_ = bstack1l1lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᦛ") in config and config[bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᦜ")] == True
      bstack111ll1lll1l_opy_ = bstack1l1lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᦝ") in config and str(config[bstack1l1lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᦞ")]).lower() != bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᦟ")
      if not (bstack1ll1l1ll11l_opy_ and (not bstack11ll1llll_opy_(config) or bstack111ll1lll1l_opy_)):
        return bstack1ll1111l_opy_
      bstack111llll11l1_opy_ = bstack11l1l11l_opy_.bstack11l11l11111_opy_
      if bstack111llll11l1_opy_ is None:
        logger.debug(bstack1l1lll1_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦᦠ"))
        return bstack1ll1111l_opy_
      bstack111llll1111_opy_ = int(str(bstack111lll1l111_opy_()).split(bstack1l1lll1_opy_ (u"ࠩ࠱ࠫᦡ"))[0])
      logger.debug(bstack1l1lll1_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥᦢ") + str(bstack111llll1111_opy_) + bstack1l1lll1_opy_ (u"ࠦࠧᦣ"))
      if bstack111llll1111_opy_ == 3 and isinstance(bstack1ll1111l_opy_, dict) and bstack1l1lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᦤ") in bstack1ll1111l_opy_ and bstack111llll11l1_opy_ is not None:
        if bstack1l1lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦥ") not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᦦ")]:
          bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᦧ")][bstack1l1lll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᦨ")] = {}
        if bstack1l1lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᦩ") in bstack111llll11l1_opy_:
          if bstack1l1lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᦪ") not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᦫ")][bstack1l1lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᦬")]:
            bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᦭")][bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᦮")][bstack1l1lll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᦯")] = []
          for arg in bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᦰ")]:
            if arg not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᦱ")][bstack1l1lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᦲ")][bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫᦳ")]:
              bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᦴ")][bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦵ")][bstack1l1lll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᦶ")].append(arg)
        if bstack1l1lll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᦷ") in bstack111llll11l1_opy_:
          if bstack1l1lll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᦸ") not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᦹ")][bstack1l1lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᦺ")]:
            bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᦻ")][bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦼ")][bstack1l1lll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᦽ")] = []
          for ext in bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᦾ")]:
            if ext not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᦿ")][bstack1l1lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᧀ")][bstack1l1lll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᧁ")]:
              bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᧂ")][bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᧃ")][bstack1l1lll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᧄ")].append(ext)
        if bstack1l1lll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᧅ") in bstack111llll11l1_opy_:
          if bstack1l1lll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᧆ") not in bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᧇ")][bstack1l1lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᧈ")]:
            bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᧉ")][bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᧊")][bstack1l1lll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᧋")] = {}
          bstack111ll1ll1ll_opy_(bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᧌")][bstack1l1lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᧍")][bstack1l1lll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᧎")],
                    bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᧏")])
        os.environ[bstack1l1lll1_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᧐")] = bstack1l1lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᧑")
        return bstack1ll1111l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1111l_opy_, ChromeOptions):
          chrome_options = bstack1ll1111l_opy_
        elif isinstance(bstack1ll1111l_opy_, dict):
          for value in bstack1ll1111l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1111l_opy_, dict):
            bstack1ll1111l_opy_[bstack1l1lll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᧒")] = chrome_options
          else:
            bstack1ll1111l_opy_ = chrome_options
        if bstack111llll11l1_opy_ is not None:
          if bstack1l1lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᧓") in bstack111llll11l1_opy_:
                bstack111lll1llll_opy_ = chrome_options.arguments or []
                new_args = bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩ᧔")]
                for arg in new_args:
                    if arg not in bstack111lll1llll_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1lll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᧕") in bstack111llll11l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1lll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᧖"), [])
                bstack111ll1l1lll_opy_ = bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ᧗")]
                for extension in bstack111ll1l1lll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1lll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᧘") in bstack111llll11l1_opy_:
                bstack111lll1l1ll_opy_ = chrome_options.experimental_options.get(bstack1l1lll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᧙"), {})
                bstack111ll1l1ll1_opy_ = bstack111llll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᧚")]
                bstack111ll1ll1ll_opy_(bstack111lll1l1ll_opy_, bstack111ll1l1ll1_opy_)
                chrome_options.add_experimental_option(bstack1l1lll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᧛"), bstack111lll1l1ll_opy_)
        os.environ[bstack1l1lll1_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᧜")] = bstack1l1lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ᧝")
        return bstack1ll1111l_opy_
    except Exception as e:
      logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧ᧞") + str(e))
      return bstack1ll1111l_opy_