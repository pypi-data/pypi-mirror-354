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
import threading
from bstack_utils.helper import bstack11l11l111_opy_
from bstack_utils.constants import bstack111lllllll1_opy_, EVENTS, STAGE
from bstack_utils.bstack1l111111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll1l1l_opy_:
    bstack11l1ll111l1_opy_ = None
    @classmethod
    def bstack1ll11lll11_opy_(cls):
        if cls.on() and os.getenv(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧᢇ")):
            logger.info(
                bstack1l1lll1_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫᢈ").format(os.getenv(bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢᢉ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᢊ"), None) is None or os.environ[bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᢋ")] == bstack1l1lll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᢌ"):
            return False
        return True
    @classmethod
    def bstack11l1111l111_opy_(cls, bs_config, framework=bstack1l1lll1_opy_ (u"ࠨࠢᢍ")):
        bstack111lllll1ll_opy_ = False
        for fw in bstack111lllllll1_opy_:
            if fw in framework:
                bstack111lllll1ll_opy_ = True
        return bstack11l11l111_opy_(bs_config.get(bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᢎ"), bstack111lllll1ll_opy_))
    @classmethod
    def bstack111llllll11_opy_(cls, framework):
        return framework in bstack111lllllll1_opy_
    @classmethod
    def bstack11l111l1l1l_opy_(cls, bs_config, framework):
        return cls.bstack11l1111l111_opy_(bs_config, framework) is True and cls.bstack111llllll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᢏ"), None)
    @staticmethod
    def bstack111lll1lll_opy_():
        if getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᢐ"), None):
            return {
                bstack1l1lll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᢑ"): bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᢒ"),
                bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᢓ"): getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᢔ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᢕ"), None):
            return {
                bstack1l1lll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᢖ"): bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᢗ"),
                bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᢘ"): getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᢙ"), None)
            }
        return None
    @staticmethod
    def bstack111lllll1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll1l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11l1ll_opy_(test, hook_name=None):
        bstack11l11111111_opy_ = test.parent
        if hook_name in [bstack1l1lll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᢚ"), bstack1l1lll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᢛ"), bstack1l1lll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᢜ"), bstack1l1lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᢝ")]:
            bstack11l11111111_opy_ = test
        scope = []
        while bstack11l11111111_opy_ is not None:
            scope.append(bstack11l11111111_opy_.name)
            bstack11l11111111_opy_ = bstack11l11111111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111llllll1l_opy_(hook_type):
        if hook_type == bstack1l1lll1_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᢞ"):
            return bstack1l1lll1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᢟ")
        elif hook_type == bstack1l1lll1_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᢠ"):
            return bstack1l1lll1_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᢡ")
    @staticmethod
    def bstack111llllllll_opy_(bstack11l1l1lll1_opy_):
        try:
            if not bstack11l1ll1l1l_opy_.on():
                return bstack11l1l1lll1_opy_
            if os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᢢ"), None) == bstack1l1lll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᢣ"):
                tests = os.environ.get(bstack1l1lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᢤ"), None)
                if tests is None or tests == bstack1l1lll1_opy_ (u"ࠤࡱࡹࡱࡲࠢᢥ"):
                    return bstack11l1l1lll1_opy_
                bstack11l1l1lll1_opy_ = tests.split(bstack1l1lll1_opy_ (u"ࠪ࠰ࠬᢦ"))
                return bstack11l1l1lll1_opy_
        except Exception as exc:
            logger.debug(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᢧ") + str(str(exc)) + bstack1l1lll1_opy_ (u"ࠧࠨᢨ"))
        return bstack11l1l1lll1_opy_