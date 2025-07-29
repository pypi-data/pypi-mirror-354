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
import threading
import logging
import bstack_utils.accessibility as bstack111l1ll1l_opy_
from bstack_utils.helper import bstack1l1l1111l_opy_
logger = logging.getLogger(__name__)
def bstack1l1ll1l11l_opy_(bstack1ll1l111_opy_):
  return True if bstack1ll1l111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1lllll_opy_(context, *args):
    tags = getattr(args[0], bstack1l1lll1_opy_ (u"ࠬࡺࡡࡨࡵࠪᨆ"), [])
    bstack1l1l1l11l1_opy_ = bstack111l1ll1l_opy_.bstack11lll1111_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1l1l11l1_opy_
    try:
      bstack1111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1l11l_opy_(bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᨇ")) else context.browser
      if bstack1111111l1_opy_ and bstack1111111l1_opy_.session_id and bstack1l1l1l11l1_opy_ and bstack1l1l1111l_opy_(
              threading.current_thread(), bstack1l1lll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᨈ"), None):
          threading.current_thread().isA11yTest = bstack111l1ll1l_opy_.bstack1l111l1ll_opy_(bstack1111111l1_opy_, bstack1l1l1l11l1_opy_)
    except Exception as e:
       logger.debug(bstack1l1lll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᨉ").format(str(e)))
def bstack1llll111ll_opy_(bstack1111111l1_opy_):
    if bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᨊ"), None) and bstack1l1l1111l_opy_(
      threading.current_thread(), bstack1l1lll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᨋ"), None) and not bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᨌ"), False):
      threading.current_thread().a11y_stop = True
      bstack111l1ll1l_opy_.bstack1l11ll1lll_opy_(bstack1111111l1_opy_, name=bstack1l1lll1_opy_ (u"ࠧࠨᨍ"), path=bstack1l1lll1_opy_ (u"ࠨࠢᨎ"))