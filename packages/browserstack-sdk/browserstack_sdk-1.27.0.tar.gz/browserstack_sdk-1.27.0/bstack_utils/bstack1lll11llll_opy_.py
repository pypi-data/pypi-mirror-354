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
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11ll11_opy_, bstack1l11l1l1l_opy_, bstack1l1l1111l_opy_, bstack1lll111ll_opy_, \
    bstack11l1l11lll1_opy_
from bstack_utils.measure import measure
def bstack1ll111ll_opy_(bstack11l1l1l1111_opy_):
    for driver in bstack11l1l1l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll11111_opy_, stage=STAGE.bstack1lllll111l_opy_)
def bstack1l111ll1l_opy_(driver, status, reason=bstack1l1lll1_opy_ (u"ࠧࠨᛎ")):
    bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
    if bstack111l111l1_opy_.bstack1111l1l11l_opy_():
        return
    bstack1l1llllll_opy_ = bstack1ll1l11ll_opy_(bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᛏ"), bstack1l1lll1_opy_ (u"ࠩࠪᛐ"), status, reason, bstack1l1lll1_opy_ (u"ࠪࠫᛑ"), bstack1l1lll1_opy_ (u"ࠫࠬᛒ"))
    driver.execute_script(bstack1l1llllll_opy_)
@measure(event_name=EVENTS.bstack1ll11111_opy_, stage=STAGE.bstack1lllll111l_opy_)
def bstack1lll1llll_opy_(page, status, reason=bstack1l1lll1_opy_ (u"ࠬ࠭ᛓ")):
    try:
        if page is None:
            return
        bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
        if bstack111l111l1_opy_.bstack1111l1l11l_opy_():
            return
        bstack1l1llllll_opy_ = bstack1ll1l11ll_opy_(bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᛔ"), bstack1l1lll1_opy_ (u"ࠧࠨᛕ"), status, reason, bstack1l1lll1_opy_ (u"ࠨࠩᛖ"), bstack1l1lll1_opy_ (u"ࠩࠪᛗ"))
        page.evaluate(bstack1l1lll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᛘ"), bstack1l1llllll_opy_)
    except Exception as e:
        print(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᛙ"), e)
def bstack1ll1l11ll_opy_(type, name, status, reason, bstack1lll1l1ll_opy_, bstack1111l1111_opy_):
    bstack1l1ll11l1_opy_ = {
        bstack1l1lll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᛚ"): type,
        bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛛ"): {}
    }
    if type == bstack1l1lll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᛜ"):
        bstack1l1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᛝ")][bstack1l1lll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᛞ")] = bstack1lll1l1ll_opy_
        bstack1l1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᛟ")][bstack1l1lll1_opy_ (u"ࠫࡩࡧࡴࡢࠩᛠ")] = json.dumps(str(bstack1111l1111_opy_))
    if type == bstack1l1lll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᛡ"):
        bstack1l1ll11l1_opy_[bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛢ")][bstack1l1lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛣ")] = name
    if type == bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᛤ"):
        bstack1l1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᛥ")][bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᛦ")] = status
        if status == bstack1l1lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛧ") and str(reason) != bstack1l1lll1_opy_ (u"ࠧࠨᛨ"):
            bstack1l1ll11l1_opy_[bstack1l1lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛩ")][bstack1l1lll1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᛪ")] = json.dumps(str(reason))
    bstack11ll11111l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭᛫").format(json.dumps(bstack1l1ll11l1_opy_))
    return bstack11ll11111l_opy_
def bstack1l11l1l111_opy_(url, config, logger, bstack1lll1l1lll_opy_=False):
    hostname = bstack1l11l1l1l_opy_(url)
    is_private = bstack1lll111ll_opy_(hostname)
    try:
        if is_private or bstack1lll1l1lll_opy_:
            file_path = bstack11l1l11ll11_opy_(bstack1l1lll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᛬"), bstack1l1lll1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ᛭"), logger)
            if os.environ.get(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᛮ")) and eval(
                    os.environ.get(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᛯ"))):
                return
            if (bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᛰ") in config and not config[bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᛱ")]):
                os.environ[bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᛲ")] = str(True)
                bstack11l1l1l111l_opy_ = {bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᛳ"): hostname}
                bstack11l1l11lll1_opy_(bstack1l1lll1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᛴ"), bstack1l1lll1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᛵ"), bstack11l1l1l111l_opy_, logger)
    except Exception as e:
        pass
def bstack1l11111l11_opy_(caps, bstack11l1l11llll_opy_):
    if bstack1l1lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛶ") in caps:
        caps[bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᛷ")][bstack1l1lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᛸ")] = True
        if bstack11l1l11llll_opy_:
            caps[bstack1l1lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᛹")][bstack1l1lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ᛺")] = bstack11l1l11llll_opy_
    else:
        caps[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ᛻")] = True
        if bstack11l1l11llll_opy_:
            caps[bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᛼")] = bstack11l1l11llll_opy_
def bstack11l1ll1lll1_opy_(bstack1111llllll_opy_):
    bstack11l1l11ll1l_opy_ = bstack1l1l1111l_opy_(threading.current_thread(), bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ᛽"), bstack1l1lll1_opy_ (u"࠭ࠧ᛾"))
    if bstack11l1l11ll1l_opy_ == bstack1l1lll1_opy_ (u"ࠧࠨ᛿") or bstack11l1l11ll1l_opy_ == bstack1l1lll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᜀ"):
        threading.current_thread().testStatus = bstack1111llllll_opy_
    else:
        if bstack1111llllll_opy_ == bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᜁ"):
            threading.current_thread().testStatus = bstack1111llllll_opy_