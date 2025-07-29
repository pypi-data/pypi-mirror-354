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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l111111l_opy_ import get_logger
from bstack_utils.bstack11l1l1lll_opy_ import bstack1lll11l11l1_opy_
bstack11l1l1lll_opy_ = bstack1lll11l11l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll1llllll_opy_: Optional[str] = None):
    bstack1l1lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡉ࡫ࡣࡰࡴࡤࡸࡴࡸࠠࡵࡱࠣࡰࡴ࡭ࠠࡵࡪࡨࠤࡸࡺࡡࡳࡶࠣࡸ࡮ࡳࡥࠡࡱࡩࠤࡦࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠎࠥࠦࠠࠡࡣ࡯ࡳࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ‥")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l11l111_opy_: str = bstack11l1l1lll_opy_.bstack11ll111l1ll_opy_(label)
            start_mark: str = label + bstack1l1lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ…")
            end_mark: str = label + bstack1l1lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ‧")
            result = None
            try:
                if stage.value == STAGE.bstack1lll1lll1l_opy_.value:
                    bstack11l1l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11l1l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll1llllll_opy_)
                elif stage.value == STAGE.bstack1lllll111l_opy_.value:
                    start_mark: str = bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ ")
                    end_mark: str = bstack1ll1l11l111_opy_ + bstack1l1lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ ")
                    bstack11l1l1lll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11l1l1lll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll1llllll_opy_)
            except Exception as e:
                bstack11l1l1lll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll1llllll_opy_)
            return result
        return wrapper
    return decorator