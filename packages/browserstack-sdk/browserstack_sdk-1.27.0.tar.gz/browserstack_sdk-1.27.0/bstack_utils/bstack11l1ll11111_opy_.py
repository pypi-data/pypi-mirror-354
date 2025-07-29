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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11l1l1ll1l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack11l1l1ll1ll_opy_ = urljoin(builder, bstack1l1lll1_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬᚍ"))
        if params:
            bstack11l1l1ll1ll_opy_ += bstack1l1lll1_opy_ (u"ࠨ࠿ࡼࡿࠥᚎ").format(urlencode({bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᚏ"): params.get(bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᚐ"))}))
        return bstack11l1l1ll1l1_opy_.bstack11l1l1lll1l_opy_(bstack11l1l1ll1ll_opy_)
    @staticmethod
    def bstack11l1l1lll11_opy_(builder,params=None):
        bstack11l1l1ll1ll_opy_ = urljoin(builder, bstack1l1lll1_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᚑ"))
        if params:
            bstack11l1l1ll1ll_opy_ += bstack1l1lll1_opy_ (u"ࠥࡃࢀࢃࠢᚒ").format(urlencode({bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᚓ"): params.get(bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᚔ"))}))
        return bstack11l1l1ll1l1_opy_.bstack11l1l1lll1l_opy_(bstack11l1l1ll1ll_opy_)
    @staticmethod
    def bstack11l1l1lll1l_opy_(bstack11l1l1lllll_opy_):
        bstack11l1ll1111l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᚕ"), os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᚖ"), bstack1l1lll1_opy_ (u"ࠨࠩᚗ")))
        headers = {bstack1l1lll1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᚘ"): bstack1l1lll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᚙ").format(bstack11l1ll1111l_opy_)}
        response = requests.get(bstack11l1l1lllll_opy_, headers=headers)
        bstack11l1l1ll11l_opy_ = {}
        try:
            bstack11l1l1ll11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥᚚ").format(e))
            pass
        if bstack11l1l1ll11l_opy_ is not None:
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭᚛")] = response.headers.get(bstack1l1lll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ᚜"), str(int(datetime.now().timestamp() * 1000)))
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᚝")] = response.status_code
        return bstack11l1l1ll11l_opy_
    @staticmethod
    def bstack11l1l1ll111_opy_(bstack11l1l1lllll_opy_, data):
        bstack1l1lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡐࡕࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᚞")
        bstack11l1ll1111l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᚟"), bstack1l1lll1_opy_ (u"ࠪࠫᚠ"))
        headers = {
            bstack1l1lll1_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᚡ"): bstack1l1lll1_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᚢ").format(bstack11l1ll1111l_opy_),
            bstack1l1lll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᚣ"): bstack1l1lll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᚤ")
        }
        response = requests.post(bstack11l1l1lllll_opy_, headers=headers, json=data)
        bstack11l1l1ll11l_opy_ = {}
        try:
            bstack11l1l1ll11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢᚥ").format(e))
            pass
        if bstack11l1l1ll11l_opy_ is not None:
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᚦ")] = response.headers.get(
                bstack1l1lll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᚧ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᚨ")] = response.status_code
        return bstack11l1l1ll11l_opy_
    @staticmethod
    def bstack11l1l1llll1_opy_(bstack11l1l1lllll_opy_, data):
        bstack1l1lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦ࡯ࡳࡦࡨࡶࡪࡪࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᚩ")
        bstack11l1ll1111l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᚪ"), bstack1l1lll1_opy_ (u"ࠧࠨᚫ"))
        headers = {
            bstack1l1lll1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᚬ"): bstack1l1lll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᚭ").format(bstack11l1ll1111l_opy_),
            bstack1l1lll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᚮ"): bstack1l1lll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᚯ")
        }
        response = requests.get(bstack11l1l1lllll_opy_, headers=headers, json=data)
        bstack11l1l1ll11l_opy_ = {}
        try:
            bstack11l1l1ll11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦᚰ").format(e))
            pass
        if bstack11l1l1ll11l_opy_ is not None:
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᚱ")] = response.headers.get(
                bstack1l1lll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᚲ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᚳ")] = response.status_code
        return bstack11l1l1ll11l_opy_
    @staticmethod
    def bstack11l1l1l1ll1_opy_(bstack11l1l1lllll_opy_, data):
        bstack1l1lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᚴ")
        bstack11l1ll1111l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᚵ"), bstack1l1lll1_opy_ (u"ࠫࠬᚶ"))
        headers = {
            bstack1l1lll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᚷ"): bstack1l1lll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᚸ").format(bstack11l1ll1111l_opy_),
            bstack1l1lll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᚹ"): bstack1l1lll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᚺ")
        }
        response = requests.put(bstack11l1l1lllll_opy_, headers=headers, json=data)
        bstack11l1l1ll11l_opy_ = {}
        try:
            bstack11l1l1ll11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣᚻ").format(e))
            pass
        logger.debug(bstack1l1lll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧᚼ").format(bstack11l1l1ll11l_opy_))
        if bstack11l1l1ll11l_opy_ is not None:
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᚽ")] = response.headers.get(
                bstack1l1lll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᚾ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᚿ")] = response.status_code
        return bstack11l1l1ll11l_opy_
    @staticmethod
    def bstack11l1l1l1lll_opy_(bstack11l1l1lllll_opy_):
        bstack1l1lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᛀ")
        bstack11l1ll1111l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᛁ"), bstack1l1lll1_opy_ (u"ࠩࠪᛂ"))
        headers = {
            bstack1l1lll1_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᛃ"): bstack1l1lll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᛄ").format(bstack11l1ll1111l_opy_),
            bstack1l1lll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᛅ"): bstack1l1lll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᛆ")
        }
        response = requests.get(bstack11l1l1lllll_opy_, headers=headers)
        bstack11l1l1ll11l_opy_ = {}
        try:
            bstack11l1l1ll11l_opy_ = response.json()
            logger.debug(bstack1l1lll1_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤᛇ").format(bstack11l1l1ll11l_opy_))
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧᛈ").format(e, response.text))
            pass
        if bstack11l1l1ll11l_opy_ is not None:
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᛉ")] = response.headers.get(
                bstack1l1lll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᛊ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack11l1l1ll11l_opy_[bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᛋ")] = response.status_code
        return bstack11l1l1ll11l_opy_