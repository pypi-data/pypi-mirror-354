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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1llll1ll_opy_
bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
def bstack11l1lllll1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l1llllll1_opy_(bstack11ll1111111_opy_, bstack11ll11111l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11ll1111111_opy_):
        with open(bstack11ll1111111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l1lllll1l_opy_(bstack11ll1111111_opy_):
        pac = get_pac(url=bstack11ll1111111_opy_)
    else:
        raise Exception(bstack1l1lll1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᘯ").format(bstack11ll1111111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1lll1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᘰ"), 80))
        bstack11l1lllll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l1lllll11_opy_ = bstack1l1lll1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᘱ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11ll11111l1_opy_, bstack11l1lllll11_opy_)
    return proxy_url
def bstack1l1llll1l1_opy_(config):
    return bstack1l1lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᘲ") in config or bstack1l1lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᘳ") in config
def bstack1l111ll111_opy_(config):
    if not bstack1l1llll1l1_opy_(config):
        return
    if config.get(bstack1l1lll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᘴ")):
        return config.get(bstack1l1lll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᘵ"))
    if config.get(bstack1l1lll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᘶ")):
        return config.get(bstack1l1lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᘷ"))
def bstack1l11ll11l_opy_(config, bstack11ll11111l1_opy_):
    proxy = bstack1l111ll111_opy_(config)
    proxies = {}
    if config.get(bstack1l1lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᘸ")) or config.get(bstack1l1lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᘹ")):
        if proxy.endswith(bstack1l1lll1_opy_ (u"࠭࠮ࡱࡣࡦࠫᘺ")):
            proxies = bstack1l1l1lll_opy_(proxy, bstack11ll11111l1_opy_)
        else:
            proxies = {
                bstack1l1lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᘻ"): proxy
            }
    bstack111l111l1_opy_.bstack11l111ll1_opy_(bstack1l1lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᘼ"), proxies)
    return proxies
def bstack1l1l1lll_opy_(bstack11ll1111111_opy_, bstack11ll11111l1_opy_):
    proxies = {}
    global bstack11ll111111l_opy_
    if bstack1l1lll1_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᘽ") in globals():
        return bstack11ll111111l_opy_
    try:
        proxy = bstack11l1llllll1_opy_(bstack11ll1111111_opy_, bstack11ll11111l1_opy_)
        if bstack1l1lll1_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᘾ") in proxy:
            proxies = {}
        elif bstack1l1lll1_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᘿ") in proxy or bstack1l1lll1_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᙀ") in proxy or bstack1l1lll1_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᙁ") in proxy:
            bstack11l1lllllll_opy_ = proxy.split(bstack1l1lll1_opy_ (u"ࠢࠡࠤᙂ"))
            if bstack1l1lll1_opy_ (u"ࠣ࠼࠲࠳ࠧᙃ") in bstack1l1lll1_opy_ (u"ࠤࠥᙄ").join(bstack11l1lllllll_opy_[1:]):
                proxies = {
                    bstack1l1lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᙅ"): bstack1l1lll1_opy_ (u"ࠦࠧᙆ").join(bstack11l1lllllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᙇ"): str(bstack11l1lllllll_opy_[0]).lower() + bstack1l1lll1_opy_ (u"ࠨ࠺࠰࠱ࠥᙈ") + bstack1l1lll1_opy_ (u"ࠢࠣᙉ").join(bstack11l1lllllll_opy_[1:])
                }
        elif bstack1l1lll1_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᙊ") in proxy:
            bstack11l1lllllll_opy_ = proxy.split(bstack1l1lll1_opy_ (u"ࠤࠣࠦᙋ"))
            if bstack1l1lll1_opy_ (u"ࠥ࠾࠴࠵ࠢᙌ") in bstack1l1lll1_opy_ (u"ࠦࠧᙍ").join(bstack11l1lllllll_opy_[1:]):
                proxies = {
                    bstack1l1lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᙎ"): bstack1l1lll1_opy_ (u"ࠨࠢᙏ").join(bstack11l1lllllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᙐ"): bstack1l1lll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᙑ") + bstack1l1lll1_opy_ (u"ࠤࠥᙒ").join(bstack11l1lllllll_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᙓ"): proxy
            }
    except Exception as e:
        print(bstack1l1lll1_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᙔ"), bstack11l1llll1ll_opy_.format(bstack11ll1111111_opy_, str(e)))
    bstack11ll111111l_opy_ = proxies
    return proxies