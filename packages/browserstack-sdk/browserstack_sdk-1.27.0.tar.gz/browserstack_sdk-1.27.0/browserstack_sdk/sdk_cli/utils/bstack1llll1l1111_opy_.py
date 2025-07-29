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
from typing import List, Dict, Any
from bstack_utils.bstack1l111111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll11ll1ll_opy_:
    bstack1l1lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡷࡷ࡭ࡱ࡯ࡴࡺࠢࡰࡩࡹ࡮࡯ࡥࡵࠣࡸࡴࠦࡳࡦࡶࠣࡥࡳࡪࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࠦ࡭ࡦࡶࡤࡨࡦࡺࡡ࠯ࠌࠣࠤࠥࠦࡉࡵࠢࡰࡥ࡮ࡴࡴࡢ࡫ࡱࡷࠥࡺࡷࡰࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡡ࡯ࡦࠣࡦࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸ࠴ࠊࠡࠢࠣࠤࡊࡧࡣࡩࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡪࡴࡴࡳࡻࠣ࡭ࡸࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡧ࡫ࠠࡴࡶࡵࡹࡨࡺࡵࡳࡧࡧࠤࡦࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡦࡪࡧ࡯ࡨࡤࡺࡹࡱࡧࠥ࠾ࠥࠨ࡭ࡶ࡮ࡷ࡭ࡤࡪࡲࡰࡲࡧࡳࡼࡴࠢ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡷࡣ࡯ࡹࡪࡹࠢ࠻ࠢ࡞ࡰ࡮ࡹࡴࠡࡱࡩࠤࡹࡧࡧࠡࡸࡤࡰࡺ࡫ࡳ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠤࠥࠦᕞ")
    _1l1111111l1_opy_: Dict[str, Dict[str, Any]] = {}
    _11llllll1ll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1ll1l111_opy_: str, key_value: str, bstack11lllllll1l_opy_: bool = False) -> None:
        if not bstack1ll1l111_opy_ or not key_value or bstack1ll1l111_opy_.strip() == bstack1l1lll1_opy_ (u"ࠦࠧᕟ") or key_value.strip() == bstack1l1lll1_opy_ (u"ࠧࠨᕠ"):
            logger.error(bstack1l1lll1_opy_ (u"ࠨ࡫ࡦࡻࡢࡲࡦࡳࡥࠡࡣࡱࡨࠥࡱࡥࡺࡡࡹࡥࡱࡻࡥࠡ࡯ࡸࡷࡹࠦࡢࡦࠢࡱࡳࡳ࠳࡮ࡶ࡮࡯ࠤࡦࡴࡤࠡࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠦᕡ"))
        values: List[str] = bstack1lll11ll1ll_opy_.bstack11lllllllll_opy_(key_value)
        bstack11llllll1l1_opy_ = {bstack1l1lll1_opy_ (u"ࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦᕢ"): bstack1l1lll1_opy_ (u"ࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤᕣ"), bstack1l1lll1_opy_ (u"ࠤࡹࡥࡱࡻࡥࡴࠤᕤ"): values}
        bstack1l111111111_opy_ = bstack1lll11ll1ll_opy_._11llllll1ll_opy_ if bstack11lllllll1l_opy_ else bstack1lll11ll1ll_opy_._1l1111111l1_opy_
        if bstack1ll1l111_opy_ in bstack1l111111111_opy_:
            bstack11llllllll1_opy_ = bstack1l111111111_opy_[bstack1ll1l111_opy_]
            bstack11lllllll11_opy_ = bstack11llllllll1_opy_.get(bstack1l1lll1_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥᕥ"), [])
            for val in values:
                if val not in bstack11lllllll11_opy_:
                    bstack11lllllll11_opy_.append(val)
            bstack11llllllll1_opy_[bstack1l1lll1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᕦ")] = bstack11lllllll11_opy_
        else:
            bstack1l111111111_opy_[bstack1ll1l111_opy_] = bstack11llllll1l1_opy_
    @staticmethod
    def bstack1l1111lllll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll11ll1ll_opy_._1l1111111l1_opy_
    @staticmethod
    def bstack11llllll11l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll11ll1ll_opy_._11llllll1ll_opy_
    @staticmethod
    def bstack11lllllllll_opy_(bstack1l11111111l_opy_: str) -> List[str]:
        bstack1l1lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡴࡱ࡯ࡴࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡲࡸࡸࠥࡹࡴࡳ࡫ࡱ࡫ࠥࡨࡹࠡࡥࡲࡱࡲࡧࡳࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡧࡶࡴࡪࡩࡴࡪࡰࡪࠤࡩࡵࡵࡣ࡮ࡨ࠱ࡶࡻ࡯ࡵࡧࡧࠤࡸࡻࡢࡴࡶࡵ࡭ࡳ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡦࡺࡤࡱࡵࡲࡥ࠻ࠢࠪࡥ࠱ࠦࠢࡣ࠮ࡦࠦ࠱ࠦࡤࠨࠢ࠰ࡂࠥࡡࠧࡢࠩ࠯ࠤࠬࡨࠬࡤࠩ࠯ࠤࠬࡪࠧ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᕧ")
        pattern = re.compile(bstack1l1lll1_opy_ (u"ࡸࠧࠣࠪ࡞ࡢࠧࡣࠪࠪࠤࡿࠬࡠࡤࠬ࡞࠭ࠬࠫᕨ"))
        result = []
        for match in pattern.finditer(bstack1l11111111l_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l1lll1_opy_ (u"ࠢࡖࡶ࡬ࡰ࡮ࡺࡹࠡࡥ࡯ࡥࡸࡹࠠࡴࡪࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡪࡰࡶࡸࡦࡴࡴࡪࡣࡷࡩࡩࠨᕩ"))