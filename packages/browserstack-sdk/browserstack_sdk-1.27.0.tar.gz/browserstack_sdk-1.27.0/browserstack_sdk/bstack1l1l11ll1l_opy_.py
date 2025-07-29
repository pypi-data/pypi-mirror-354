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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11ll1ll1_opy_ = {}
        bstack11l1111l1l_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ຾"), bstack1l1lll1_opy_ (u"ࠩࠪ຿"))
        if not bstack11l1111l1l_opy_:
            return bstack11ll1ll1_opy_
        try:
            bstack11l1111ll1_opy_ = json.loads(bstack11l1111l1l_opy_)
            if bstack1l1lll1_opy_ (u"ࠥࡳࡸࠨເ") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠦࡴࡹࠢແ")] = bstack11l1111ll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡵࡳࠣໂ")]
            if bstack1l1lll1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥໃ") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥໄ") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ໅")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨໆ"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ໇")))
            if bstack1l1lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ່ࠧ") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧ້ࠥ") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ໊ࠦ")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲ໋ࠣ"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ໌")))
            if bstack1l1lll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦໍ") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦ໎") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໏")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໐"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ໑")))
            if bstack1l1lll1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢ໒") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ໓") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ໔")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ໕"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ໖")))
            if bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ໗") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ໘") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໙")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ໚"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ໛")))
            if bstack1l1lll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨໜ") in bstack11l1111ll1_opy_ or bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨໝ") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢໞ")] = bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤໟ"), bstack11l1111ll1_opy_.get(bstack1l1lll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ໠")))
            if bstack1l1lll1_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໡") in bstack11l1111ll1_opy_:
                bstack11ll1ll1_opy_[bstack1l1lll1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ໢")] = bstack11l1111ll1_opy_[bstack1l1lll1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໣")]
        except Exception as error:
            logger.error(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥ໤") +  str(error))
        return bstack11ll1ll1_opy_