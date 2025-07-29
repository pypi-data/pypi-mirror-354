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
from browserstack_sdk.bstack11111l1l1_opy_ import bstack1l111111ll_opy_
from browserstack_sdk.bstack111l111l1l_opy_ import RobotHandler
def bstack1lllll11_opy_(framework):
    if framework.lower() == bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᵸ"):
        return bstack1l111111ll_opy_.version()
    elif framework.lower() == bstack1l1lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᵹ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1lll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᵺ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1lll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᵻ")
def bstack11lll1l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1lll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᵼ"))
        framework_version.append(importlib.metadata.version(bstack1l1lll1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᵽ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1lll1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᵾ"))
        framework_version.append(importlib.metadata.version(bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᵿ")))
    except:
        pass
    return {
        bstack1l1lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᶀ"): bstack1l1lll1_opy_ (u"ࠧࡠࠩᶁ").join(framework_name),
        bstack1l1lll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᶂ"): bstack1l1lll1_opy_ (u"ࠩࡢࠫᶃ").join(framework_version)
    }