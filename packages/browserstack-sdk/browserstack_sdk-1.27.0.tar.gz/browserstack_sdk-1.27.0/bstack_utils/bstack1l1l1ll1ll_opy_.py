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
import tempfile
import math
from bstack_utils import bstack1l111111l_opy_
from bstack_utils.constants import bstack1l11ll111l_opy_
bstack11111111l1l_opy_ = {bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪ⁲"), bstack1l1lll1_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫ⁳")}
bstack11111111l11_opy_ = {bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⁴")}
logger = bstack1l111111l_opy_.get_logger(__name__, bstack1l11ll111l_opy_)
class bstack11ll1l1ll1_opy_:
    @staticmethod
    def bstack1lll1ll11l_opy_(config: dict) -> bool:
        bstack1111111l111_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫ⁵"), {}).get(bstack1l1lll1_opy_ (u"ࠨࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧ⁶"), {})
        return bstack1111111l111_opy_.get(bstack1l1lll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪ⁷"), False)
    @staticmethod
    def bstack11ll11l111_opy_(config: dict) -> int:
        bstack1111111l111_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧ⁸"), {}).get(bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠪ⁹"), {})
        retries = 0
        if bstack11ll1l1ll1_opy_.bstack1lll1ll11l_opy_(config):
            retries = bstack1111111l111_opy_.get(bstack1l1lll1_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩ⁺"), 1)
        return retries
    @staticmethod
    def bstack11l11ll1ll_opy_(config: dict) -> dict:
        bstack11111111lll_opy_ = config.get(bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪ⁻"), {})
        return {
            key: value for key, value in bstack11111111lll_opy_.items() if key in bstack11111111l1l_opy_
        }
    @staticmethod
    def bstack1111111ll11_opy_():
        bstack1l1lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⁼")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤ⁽").format(os.getenv(bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⁾")))))
    @staticmethod
    def bstack1111111l11l_opy_(test_name: str):
        bstack1l1lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢⁿ")
        bstack11111111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥ₀").format(os.getenv(bstack1l1lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ₁"))))
        with open(bstack11111111ll1_opy_, bstack1l1lll1_opy_ (u"࠭ࡡࠨ₂")) as file:
            file.write(bstack1l1lll1_opy_ (u"ࠢࡼࡿ࡟ࡲࠧ₃").format(test_name))
    @staticmethod
    def bstack1111111ll1l_opy_(framework: str) -> bool:
       return framework.lower() in bstack11111111l11_opy_
    @staticmethod
    def bstack111l11l111l_opy_(config: dict) -> bool:
        bstack111111111ll_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ₄"), {}).get(bstack1l1lll1_opy_ (u"ࠩࡤࡦࡴࡸࡴࡃࡷ࡬ࡰࡩࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠨ₅"), {})
        return bstack111111111ll_opy_.get(bstack1l1lll1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ₆"), False)
    @staticmethod
    def bstack111l11l1lll_opy_(config: dict, bstack111l11l1ll1_opy_: int = 0) -> int:
        bstack1l1lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡉࡨࡸࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩ࠲ࠠࡸࡪ࡬ࡧ࡭ࠦࡣࡢࡰࠣࡦࡪࠦࡡ࡯ࠢࡤࡦࡸࡵ࡬ࡶࡶࡨࠤࡳࡻ࡭ࡣࡧࡵࠤࡴࡸࠠࡢࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࠮ࡤࡪࡥࡷ࠭࠿ࠦࡔࡩࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡰࡶࡤࡰࡤࡺࡥࡴࡶࡶࠤ࠭࡯࡮ࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࠫࡶࡪࡷࡵࡪࡴࡨࡨࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪ࠳ࡢࡢࡵࡨࡨࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤࡴࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ₇")
        bstack111111111ll_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ₈"), {}).get(bstack1l1lll1_opy_ (u"࠭ࡡࡣࡱࡵࡸࡇࡻࡩ࡭ࡦࡒࡲࡋࡧࡩ࡭ࡷࡵࡩࠬ₉"), {})
        bstack1111111l1ll_opy_ = 0
        if bstack11ll1l1ll1_opy_.bstack111l11l111l_opy_(config):
            bstack1111111l1l1_opy_ = bstack111111111ll_opy_.get(bstack1l1lll1_opy_ (u"ࠧ࡮ࡣࡻࡊࡦ࡯࡬ࡶࡴࡨࡷࠬ₊"), 5)
            if isinstance(bstack1111111l1l1_opy_, str) and bstack1111111l1l1_opy_.endswith(bstack1l1lll1_opy_ (u"ࠨࠧࠪ₋")):
                try:
                    percentage = int(bstack1111111l1l1_opy_.strip(bstack1l1lll1_opy_ (u"ࠩࠨࠫ₌")))
                    if bstack111l11l1ll1_opy_ > 0:
                        bstack1111111l1ll_opy_ = bstack1111111l1ll_opy_ = math.ceil((percentage * bstack111l11l1ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1lll1_opy_ (u"ࠥࡘࡴࡺࡡ࡭ࠢࡷࡩࡸࡺࡳࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳ࠯ࠤ₍"))
                except ValueError as e:
                    raise ValueError(bstack1l1lll1_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦࠢࡹࡥࡱࡻࡥࠡࡨࡲࡶࠥࡳࡡࡹࡈࡤ࡭ࡱࡻࡲࡦࡵ࠽ࠤࢀࢃࠢ₎").format(bstack1111111l1l1_opy_)) from e
            else:
                bstack1111111l1ll_opy_ = int(bstack1111111l1l1_opy_)
        logger.info(bstack1l1lll1_opy_ (u"ࠧࡓࡡࡹࠢࡩࡥ࡮ࡲࡵࡳࡧࡶࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡴࡧࡷࠤࡹࡵ࠺ࠡࡽࢀࠤ࠭࡬ࡲࡰ࡯ࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࢀࢃࠩࠣ₏").format(bstack1111111l1ll_opy_, bstack1111111l1l1_opy_))
        return bstack1111111l1ll_opy_