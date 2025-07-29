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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1111ll1l_opy_, bstack1111ll11_opy_, get_host_info, bstack11l1111ll11_opy_, \
 bstack11ll1llll_opy_, bstack1l1l1111l_opy_, bstack111ll111l1_opy_, bstack11l11l1111l_opy_, bstack11l1ll1lll_opy_
import bstack_utils.accessibility as bstack111l1ll1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1ll1l1l_opy_
from bstack_utils.percy import bstack111lll11l_opy_
from bstack_utils.config import Config
bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack111lll11l_opy_()
@bstack111ll111l1_opy_(class_method=False)
def bstack11l11l11lll_opy_(bs_config, bstack11l1l1l1l_opy_):
  try:
    data = {
        bstack1l1lll1_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᠾ"): bstack1l1lll1_opy_ (u"ࠬࡰࡳࡰࡰࠪᠿ"),
        bstack1l1lll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᡀ"): bs_config.get(bstack1l1lll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᡁ"), bstack1l1lll1_opy_ (u"ࠨࠩᡂ")),
        bstack1l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᡃ"): bs_config.get(bstack1l1lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᡄ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᡅ"): bs_config.get(bstack1l1lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᡆ")),
        bstack1l1lll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᡇ"): bs_config.get(bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᡈ"), bstack1l1lll1_opy_ (u"ࠨࠩᡉ")),
        bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᡊ"): bstack11l1ll1lll_opy_(),
        bstack1l1lll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᡋ"): bstack11l1111ll11_opy_(bs_config),
        bstack1l1lll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᡌ"): get_host_info(),
        bstack1l1lll1_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᡍ"): bstack1111ll11_opy_(),
        bstack1l1lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᡎ"): os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᡏ")),
        bstack1l1lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᡐ"): os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᡑ"), False),
        bstack1l1lll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᡒ"): bstack11l1111ll1l_opy_(),
        bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᡓ"): bstack11l1111111l_opy_(bs_config),
        bstack1l1lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩᡔ"): bstack11l111111ll_opy_(bstack11l1l1l1l_opy_),
        bstack1l1lll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᡕ"): bstack11l1111l1ll_opy_(bs_config, bstack11l1l1l1l_opy_.get(bstack1l1lll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᡖ"), bstack1l1lll1_opy_ (u"ࠨࠩᡗ"))),
        bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᡘ"): bstack11ll1llll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦᡙ").format(str(error)))
    return None
def bstack11l111111ll_opy_(framework):
  return {
    bstack1l1lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᡚ"): framework.get(bstack1l1lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᡛ"), bstack1l1lll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᡜ")),
    bstack1l1lll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᡝ"): framework.get(bstack1l1lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᡞ")),
    bstack1l1lll1_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᡟ"): framework.get(bstack1l1lll1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᡠ")),
    bstack1l1lll1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᡡ"): bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᡢ"),
    bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᡣ"): framework.get(bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᡤ"))
  }
def bstack1llll11l11_opy_(bs_config, framework):
  bstack1l11lll11_opy_ = False
  bstack11lll1l11_opy_ = False
  bstack11l1111lll1_opy_ = False
  if bstack1l1lll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᡥ") in bs_config:
    bstack11l1111lll1_opy_ = True
  elif bstack1l1lll1_opy_ (u"ࠩࡤࡴࡵ࠭ᡦ") in bs_config:
    bstack1l11lll11_opy_ = True
  else:
    bstack11lll1l11_opy_ = True
  bstack1l1ll1ll1l_opy_ = {
    bstack1l1lll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᡧ"): bstack11l1ll1l1l_opy_.bstack11l1111l111_opy_(bs_config, framework),
    bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᡨ"): bstack111l1ll1l_opy_.bstack1111ll1ll_opy_(bs_config),
    bstack1l1lll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᡩ"): bs_config.get(bstack1l1lll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᡪ"), False),
    bstack1l1lll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᡫ"): bstack11lll1l11_opy_,
    bstack1l1lll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᡬ"): bstack1l11lll11_opy_,
    bstack1l1lll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᡭ"): bstack11l1111lll1_opy_
  }
  return bstack1l1ll1ll1l_opy_
@bstack111ll111l1_opy_(class_method=False)
def bstack11l1111111l_opy_(bs_config):
  try:
    bstack11l11111ll1_opy_ = json.loads(os.getenv(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᡮ"), bstack1l1lll1_opy_ (u"ࠫࢀࢃࠧᡯ")))
    bstack11l11111ll1_opy_ = bstack11l11111lll_opy_(bs_config, bstack11l11111ll1_opy_)
    return {
        bstack1l1lll1_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᡰ"): bstack11l11111ll1_opy_
    }
  except Exception as error:
    logger.error(bstack1l1lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧᡱ").format(str(error)))
    return {}
def bstack11l11111lll_opy_(bs_config, bstack11l11111ll1_opy_):
  if ((bstack1l1lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᡲ") in bs_config or not bstack11ll1llll_opy_(bs_config)) and bstack111l1ll1l_opy_.bstack1111ll1ll_opy_(bs_config)):
    bstack11l11111ll1_opy_[bstack1l1lll1_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦᡳ")] = True
  return bstack11l11111ll1_opy_
def bstack11l11l1llll_opy_(array, bstack11l1111l11l_opy_, bstack11l11111l11_opy_):
  result = {}
  for o in array:
    key = o[bstack11l1111l11l_opy_]
    result[key] = o[bstack11l11111l11_opy_]
  return result
def bstack11l111l11l1_opy_(bstack11ll1ll11_opy_=bstack1l1lll1_opy_ (u"ࠩࠪᡴ")):
  bstack11l111111l1_opy_ = bstack111l1ll1l_opy_.on()
  bstack11l1111l1l1_opy_ = bstack11l1ll1l1l_opy_.on()
  bstack11l1111llll_opy_ = percy.bstack1ll111ll1_opy_()
  if bstack11l1111llll_opy_ and not bstack11l1111l1l1_opy_ and not bstack11l111111l1_opy_:
    return bstack11ll1ll11_opy_ not in [bstack1l1lll1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᡵ"), bstack1l1lll1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᡶ")]
  elif bstack11l111111l1_opy_ and not bstack11l1111l1l1_opy_:
    return bstack11ll1ll11_opy_ not in [bstack1l1lll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᡷ"), bstack1l1lll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᡸ"), bstack1l1lll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᡹")]
  return bstack11l111111l1_opy_ or bstack11l1111l1l1_opy_ or bstack11l1111llll_opy_
@bstack111ll111l1_opy_(class_method=False)
def bstack11l11l1l11l_opy_(bstack11ll1ll11_opy_, test=None):
  bstack11l11111l1l_opy_ = bstack111l1ll1l_opy_.on()
  if not bstack11l11111l1l_opy_ or bstack11ll1ll11_opy_ not in [bstack1l1lll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᡺")] or test == None:
    return None
  return {
    bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᡻"): bstack11l11111l1l_opy_ and bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᡼"), None) == True and bstack111l1ll1l_opy_.bstack11lll1111_opy_(test[bstack1l1lll1_opy_ (u"ࠫࡹࡧࡧࡴࠩ᡽")])
  }
def bstack11l1111l1ll_opy_(bs_config, framework):
  bstack1l11lll11_opy_ = False
  bstack11lll1l11_opy_ = False
  bstack11l1111lll1_opy_ = False
  if bstack1l1lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᡾") in bs_config:
    bstack11l1111lll1_opy_ = True
  elif bstack1l1lll1_opy_ (u"࠭ࡡࡱࡲࠪ᡿") in bs_config:
    bstack1l11lll11_opy_ = True
  else:
    bstack11lll1l11_opy_ = True
  bstack1l1ll1ll1l_opy_ = {
    bstack1l1lll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᢀ"): bstack11l1ll1l1l_opy_.bstack11l1111l111_opy_(bs_config, framework),
    bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᢁ"): bstack111l1ll1l_opy_.bstack1ll111111l_opy_(bs_config),
    bstack1l1lll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᢂ"): bs_config.get(bstack1l1lll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᢃ"), False),
    bstack1l1lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᢄ"): bstack11lll1l11_opy_,
    bstack1l1lll1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᢅ"): bstack1l11lll11_opy_,
    bstack1l1lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᢆ"): bstack11l1111lll1_opy_
  }
  return bstack1l1ll1ll1l_opy_