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
import re
from bstack_utils.bstack1lll11llll_opy_ import bstack11l1ll1lll1_opy_
def bstack11l1lll111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙕ")):
        return bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᙖ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙗ")):
        return bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙘ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙙ")):
        return bstack1l1lll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᙚ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᙛ")):
        return bstack1l1lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙜ")
def bstack11l1ll1ll1l_opy_(fixture_name):
    return bool(re.match(bstack1l1lll1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᙝ"), fixture_name))
def bstack11l1lll1lll_opy_(fixture_name):
    return bool(re.match(bstack1l1lll1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᙞ"), fixture_name))
def bstack11l1llll11l_opy_(fixture_name):
    return bool(re.match(bstack1l1lll1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᙟ"), fixture_name))
def bstack11l1lll1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᙠ")):
        return bstack1l1lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᙡ"), bstack1l1lll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᙢ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᙣ")):
        return bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᙤ"), bstack1l1lll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᙥ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᙦ")):
        return bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᙧ"), bstack1l1lll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᙨ")
    elif fixture_name.startswith(bstack1l1lll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙩ")):
        return bstack1l1lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙪ"), bstack1l1lll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᙫ")
    return None, None
def bstack11l1lll11ll_opy_(hook_name):
    if hook_name in [bstack1l1lll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᙬ"), bstack1l1lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ᙭")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l1lll11l1_opy_(hook_name):
    if hook_name in [bstack1l1lll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ᙮"), bstack1l1lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᙯ")]:
        return bstack1l1lll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᙰ")
    elif hook_name in [bstack1l1lll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᙱ"), bstack1l1lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᙲ")]:
        return bstack1l1lll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᙳ")
    elif hook_name in [bstack1l1lll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᙴ"), bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᙵ")]:
        return bstack1l1lll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᙶ")
    elif hook_name in [bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᙷ"), bstack1l1lll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᙸ")]:
        return bstack1l1lll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᙹ")
    return hook_name
def bstack11l1lll1111_opy_(node, scenario):
    if hasattr(node, bstack1l1lll1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᙺ")):
        parts = node.nodeid.rsplit(bstack1l1lll1_opy_ (u"ࠣ࡝ࠥᙻ"))
        params = parts[-1]
        return bstack1l1lll1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᙼ").format(scenario.name, params)
    return scenario.name
def bstack11l1lll1ll1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1lll1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᙽ")):
            examples = list(node.callspec.params[bstack1l1lll1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᙾ")].values())
        return examples
    except:
        return []
def bstack11l1llll1l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l1llll111_opy_(report):
    try:
        status = bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᙿ")
        if report.passed or (report.failed and hasattr(report, bstack1l1lll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ "))):
            status = bstack1l1lll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᚁ")
        elif report.skipped:
            status = bstack1l1lll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᚂ")
        bstack11l1ll1lll1_opy_(status)
    except:
        pass
def bstack1lllll11ll_opy_(status):
    try:
        bstack11l1lll1l11_opy_ = bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᚃ")
        if status == bstack1l1lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚄ"):
            bstack11l1lll1l11_opy_ = bstack1l1lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᚅ")
        elif status == bstack1l1lll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᚆ"):
            bstack11l1lll1l11_opy_ = bstack1l1lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᚇ")
        bstack11l1ll1lll1_opy_(bstack11l1lll1l11_opy_)
    except:
        pass
def bstack11l1ll1llll_opy_(item=None, report=None, summary=None, extra=None):
    return