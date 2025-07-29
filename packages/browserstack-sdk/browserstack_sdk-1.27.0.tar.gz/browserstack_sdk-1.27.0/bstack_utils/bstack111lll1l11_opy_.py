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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111ll11l_opy_, bstack11l111ll111_opy_, bstack1lll1l1ll1_opy_, bstack111ll111l1_opy_, bstack11l11l111ll_opy_, bstack11l11l111l1_opy_, bstack11l11l1111l_opy_, bstack11l1ll1lll_opy_, bstack1l1l1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1ll111l1_opy_ import bstack11l1ll1l1l1_opy_
import bstack_utils.bstack1l1l111111_opy_ as bstack1111l11ll_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1ll1l1l_opy_
import bstack_utils.accessibility as bstack111l1ll1l_opy_
from bstack_utils.bstack11l1l11l_opy_ import bstack11l1l11l_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack1111llll1l_opy_
bstack11l11l11l11_opy_ = bstack1l1lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᝁ")
logger = logging.getLogger(__name__)
class bstack1lll11lll_opy_:
    bstack11l1ll111l1_opy_ = None
    bs_config = None
    bstack11l1l1l1l_opy_ = None
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l11ll1lll_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def launch(cls, bs_config, bstack11l1l1l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1l1l1l_opy_ = bstack11l1l1l1l_opy_
        try:
            cls.bstack11l111l1lll_opy_()
            bstack11l11l1l1l1_opy_ = bstack11l111ll11l_opy_(bs_config)
            bstack11l11ll11l1_opy_ = bstack11l111ll111_opy_(bs_config)
            data = bstack1111l11ll_opy_.bstack11l11l11lll_opy_(bs_config, bstack11l1l1l1l_opy_)
            config = {
                bstack1l1lll1_opy_ (u"ࠫࡦࡻࡴࡩࠩᝂ"): (bstack11l11l1l1l1_opy_, bstack11l11ll11l1_opy_),
                bstack1l1lll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᝃ"): cls.default_headers()
            }
            response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"࠭ࡐࡐࡕࡗࠫᝄ"), cls.request_url(bstack1l1lll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧᝅ")), data, config)
            if response.status_code != 200:
                bstack1ll1ll11l1_opy_ = response.json()
                if bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᝆ")] == False:
                    cls.bstack11l11ll1ll1_opy_(bstack1ll1ll11l1_opy_)
                    return
                cls.bstack11l111l111l_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᝇ")])
                cls.bstack11l111l11ll_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᝈ")])
                return None
            bstack11l111lll11_opy_ = cls.bstack11l111lll1l_opy_(response)
            return bstack11l111lll11_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤᝉ").format(str(error)))
            return None
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def stop(cls, bstack11l111l1ll1_opy_=None):
        if not bstack11l1ll1l1l_opy_.on() and not bstack111l1ll1l_opy_.on():
            return
        if os.environ.get(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᝊ")) == bstack1l1lll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᝋ") or os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᝌ")) == bstack1l1lll1_opy_ (u"ࠣࡰࡸࡰࡱࠨᝍ"):
            logger.error(bstack1l1lll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᝎ"))
            return {
                bstack1l1lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝏ"): bstack1l1lll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᝐ"),
                bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᝑ"): bstack1l1lll1_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᝒ")
            }
        try:
            cls.bstack11l1ll111l1_opy_.shutdown()
            data = {
                bstack1l1lll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᝓ"): bstack11l1ll1lll_opy_()
            }
            if not bstack11l111l1ll1_opy_ is None:
                data[bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬ᝔")] = [{
                    bstack1l1lll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ᝕"): bstack1l1lll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ᝖"),
                    bstack1l1lll1_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫ᝗"): bstack11l111l1ll1_opy_
                }]
            config = {
                bstack1l1lll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᝘"): cls.default_headers()
            }
            bstack11ll1l11lll_opy_ = bstack1l1lll1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧ᝙").format(os.environ[bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ᝚")])
            bstack11l111llll1_opy_ = cls.request_url(bstack11ll1l11lll_opy_)
            response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"ࠨࡒࡘࡘࠬ᝛"), bstack11l111llll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1lll1_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣ᝜"))
        except Exception as error:
            logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢ᝝") + str(error))
            return {
                bstack1l1lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᝞"): bstack1l1lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᝟"),
                bstack1l1lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᝠ"): str(error)
            }
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def bstack11l111lll1l_opy_(cls, response):
        bstack1ll1ll11l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack11l111lll11_opy_ = {}
        if bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠧ࡫ࡹࡷࠫᝡ")) is None:
            os.environ[bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᝢ")] = bstack1l1lll1_opy_ (u"ࠩࡱࡹࡱࡲࠧᝣ")
        else:
            os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᝤ")] = bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠫ࡯ࡽࡴࠨᝥ"), bstack1l1lll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᝦ"))
        os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᝧ")] = bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᝨ"), bstack1l1lll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᝩ"))
        logger.info(bstack1l1lll1_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧᝪ") + os.getenv(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᝫ")));
        if bstack11l1ll1l1l_opy_.bstack11l111l1l1l_opy_(cls.bs_config, cls.bstack11l1l1l1l_opy_.get(bstack1l1lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᝬ"), bstack1l1lll1_opy_ (u"ࠬ࠭᝭"))) is True:
            bstack11l1ll1111l_opy_, build_hashed_id, bstack11l11l1l1ll_opy_ = cls.bstack11l11ll1l1l_opy_(bstack1ll1ll11l1_opy_)
            if bstack11l1ll1111l_opy_ != None and build_hashed_id != None:
                bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᝮ")] = {
                    bstack1l1lll1_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪᝯ"): bstack11l1ll1111l_opy_,
                    bstack1l1lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᝰ"): build_hashed_id,
                    bstack1l1lll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭᝱"): bstack11l11l1l1ll_opy_
                }
            else:
                bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᝲ")] = {}
        else:
            bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᝳ")] = {}
        bstack11l11ll1l11_opy_, build_hashed_id = cls.bstack11l111l1l11_opy_(bstack1ll1ll11l1_opy_)
        if bstack11l11ll1l11_opy_ != None and build_hashed_id != None:
            bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᝴")] = {
                bstack1l1lll1_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪ᝵"): bstack11l11ll1l11_opy_,
                bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ᝶"): build_hashed_id,
            }
        else:
            bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝷")] = {}
        if bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᝸")].get(bstack1l1lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ᝹")) != None or bstack11l111lll11_opy_[bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᝺")].get(bstack1l1lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ᝻")) != None:
            cls.bstack11l11l1ll1l_opy_(bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡪࡸࡶࠪ᝼")), bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ᝽")))
        return bstack11l111lll11_opy_
    @classmethod
    def bstack11l11ll1l1l_opy_(cls, bstack1ll1ll11l1_opy_):
        if bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᝾")) == None:
            cls.bstack11l111l111l_opy_()
            return [None, None, None]
        if bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᝿")][bstack1l1lll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫក")] != True:
            cls.bstack11l111l111l_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫខ")])
            return [None, None, None]
        logger.debug(bstack1l1lll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩគ"))
        os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬឃ")] = bstack1l1lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬង")
        if bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠨ࡬ࡺࡸࠬច")):
            os.environ[bstack1l1lll1_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ឆ")] = json.dumps({
                bstack1l1lll1_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬជ"): bstack11l111ll11l_opy_(cls.bs_config),
                bstack1l1lll1_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ឈ"): bstack11l111ll111_opy_(cls.bs_config)
            })
        if bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧញ")):
            os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬដ")] = bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩឋ")]
        if bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨឌ")].get(bstack1l1lll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪឍ"), {}).get(bstack1l1lll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧណ")):
            os.environ[bstack1l1lll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬត")] = str(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬថ")][bstack1l1lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧទ")][bstack1l1lll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫធ")])
        else:
            os.environ[bstack1l1lll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩន")] = bstack1l1lll1_opy_ (u"ࠤࡱࡹࡱࡲࠢប")
        return [bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪ࡮ࡼࡺࠧផ")], bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ព")], os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ភ")]]
    @classmethod
    def bstack11l111l1l11_opy_(cls, bstack1ll1ll11l1_opy_):
        if bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ម")) == None:
            cls.bstack11l111l11ll_opy_()
            return [None, None]
        if bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧយ")][bstack1l1lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩរ")] != True:
            cls.bstack11l111l11ll_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩល")])
            return [None, None]
        if bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪវ")].get(bstack1l1lll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬឝ")):
            logger.debug(bstack1l1lll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩឞ"))
            parsed = json.loads(os.getenv(bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧស"), bstack1l1lll1_opy_ (u"ࠧࡼࡿࠪហ")))
            capabilities = bstack1111l11ll_opy_.bstack11l11l1llll_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨឡ")][bstack1l1lll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪអ")][bstack1l1lll1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩឣ")], bstack1l1lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩឤ"), bstack1l1lll1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫឥ"))
            bstack11l11ll1l11_opy_ = capabilities[bstack1l1lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫឦ")]
            os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬឧ")] = bstack11l11ll1l11_opy_
            if bstack1l1lll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥឨ") in bstack1ll1ll11l1_opy_ and bstack1ll1ll11l1_opy_.get(bstack1l1lll1_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣឩ")) is None:
                parsed[bstack1l1lll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫឪ")] = capabilities[bstack1l1lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬឫ")]
            os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ឬ")] = json.dumps(parsed)
            scripts = bstack1111l11ll_opy_.bstack11l11l1llll_opy_(bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ឭ")][bstack1l1lll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨឮ")][bstack1l1lll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩឯ")], bstack1l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧឰ"), bstack1l1lll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫឱ"))
            bstack11l1l11l_opy_.bstack1lllllll1l_opy_(scripts)
            commands = bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឲ")][bstack1l1lll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ឳ")][bstack1l1lll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ឴")].get(bstack1l1lll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ឵"))
            bstack11l1l11l_opy_.bstack11l11l1l111_opy_(commands)
            bstack11l11l11111_opy_ = capabilities.get(bstack1l1lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ា"))
            bstack11l1l11l_opy_.bstack11l111ll1l1_opy_(bstack11l11l11111_opy_)
            bstack11l1l11l_opy_.store()
        return [bstack11l11ll1l11_opy_, bstack1ll1ll11l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫិ")]]
    @classmethod
    def bstack11l111l111l_opy_(cls, response=None):
        os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨី")] = bstack1l1lll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩឹ")
        os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩឺ")] = bstack1l1lll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫុ")
        os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ូ")] = bstack1l1lll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧួ")
        os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨើ")] = bstack1l1lll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣឿ")
        os.environ[bstack1l1lll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬៀ")] = bstack1l1lll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥេ")
        cls.bstack11l11ll1ll1_opy_(response, bstack1l1lll1_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨែ"))
        return [None, None, None]
    @classmethod
    def bstack11l111l11ll_opy_(cls, response=None):
        os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬៃ")] = bstack1l1lll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ោ")
        os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧៅ")] = bstack1l1lll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨំ")
        os.environ[bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨះ")] = bstack1l1lll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪៈ")
        cls.bstack11l11ll1ll1_opy_(response, bstack1l1lll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨ៉"))
        return [None, None, None]
    @classmethod
    def bstack11l11l1ll1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ៊")] = jwt
        os.environ[bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭់")] = build_hashed_id
    @classmethod
    def bstack11l11ll1ll1_opy_(cls, response=None, product=bstack1l1lll1_opy_ (u"ࠤࠥ៌")):
        if response == None or response.get(bstack1l1lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ៍")) == None:
            logger.error(product + bstack1l1lll1_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨ៎"))
            return
        for error in response[bstack1l1lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ៏")]:
            bstack11l11l11ll1_opy_ = error[bstack1l1lll1_opy_ (u"࠭࡫ࡦࡻࠪ័")]
            error_message = error[bstack1l1lll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៑")]
            if error_message:
                if bstack11l11l11ll1_opy_ == bstack1l1lll1_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊ្ࠢ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1lll1_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥ៓") + product + bstack1l1lll1_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ។"))
    @classmethod
    def bstack11l111l1lll_opy_(cls):
        if cls.bstack11l1ll111l1_opy_ is not None:
            return
        cls.bstack11l1ll111l1_opy_ = bstack11l1ll1l1l1_opy_(cls.bstack11l111ll1ll_opy_)
        cls.bstack11l1ll111l1_opy_.start()
    @classmethod
    def bstack111l1llll1_opy_(cls):
        if cls.bstack11l1ll111l1_opy_ is None:
            return
        cls.bstack11l1ll111l1_opy_.shutdown()
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def bstack11l111ll1ll_opy_(cls, bstack111l11l1l1_opy_, event_url=bstack1l1lll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ៕")):
        config = {
            bstack1l1lll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭៖"): cls.default_headers()
        }
        logger.debug(bstack1l1lll1_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨៗ").format(bstack1l1lll1_opy_ (u"ࠧ࠭ࠢࠪ៘").join([event[bstack1l1lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ៙")] for event in bstack111l11l1l1_opy_])))
        response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ៚"), cls.request_url(event_url), bstack111l11l1l1_opy_, config)
        bstack11l11ll11ll_opy_ = response.json()
    @classmethod
    def bstack11l1lll1l1_opy_(cls, bstack111l11l1l1_opy_, event_url=bstack1l1lll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ៛")):
        logger.debug(bstack1l1lll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦៜ").format(bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ៝")]))
        if not bstack1111l11ll_opy_.bstack11l111l11l1_opy_(bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ៞")]):
            logger.debug(bstack1l1lll1_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ៟").format(bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ០")]))
            return
        bstack1l1ll1ll1l_opy_ = bstack1111l11ll_opy_.bstack11l11l1l11l_opy_(bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭១")], bstack111l11l1l1_opy_.get(bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ២")))
        if bstack1l1ll1ll1l_opy_ != None:
            if bstack111l11l1l1_opy_.get(bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭៣")) != None:
                bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ៤")][bstack1l1lll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ៥")] = bstack1l1ll1ll1l_opy_
            else:
                bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ៦")] = bstack1l1ll1ll1l_opy_
        if event_url == bstack1l1lll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ៧"):
            cls.bstack11l111l1lll_opy_()
            logger.debug(bstack1l1lll1_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ៨").format(bstack111l11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ៩")]))
            cls.bstack11l1ll111l1_opy_.add(bstack111l11l1l1_opy_)
        elif event_url == bstack1l1lll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ៪"):
            cls.bstack11l111ll1ll_opy_([bstack111l11l1l1_opy_], event_url)
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def bstack1111ll111_opy_(cls, logs):
        bstack11l111l1111_opy_ = []
        for log in logs:
            bstack11l11l1ll11_opy_ = {
                bstack1l1lll1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ៫"): bstack1l1lll1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨ៬"),
                bstack1l1lll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭៭"): log[bstack1l1lll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ៮")],
                bstack1l1lll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ៯"): log[bstack1l1lll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭៰")],
                bstack1l1lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫ៱"): {},
                bstack1l1lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭៲"): log[bstack1l1lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ៳")],
            }
            if bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៴") in log:
                bstack11l11l1ll11_opy_[bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៵")] = log[bstack1l1lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ៶")]
            elif bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៷") in log:
                bstack11l11l1ll11_opy_[bstack1l1lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៸")] = log[bstack1l1lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៹")]
            bstack11l111l1111_opy_.append(bstack11l11l1ll11_opy_)
        cls.bstack11l1lll1l1_opy_({
            bstack1l1lll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ៺"): bstack1l1lll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ៻"),
            bstack1l1lll1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭៼"): bstack11l111l1111_opy_
        })
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def bstack11l11l1lll1_opy_(cls, steps):
        bstack11l11ll111l_opy_ = []
        for step in steps:
            bstack11l11l11l1l_opy_ = {
                bstack1l1lll1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ៽"): bstack1l1lll1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭៾"),
                bstack1l1lll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ៿"): step[bstack1l1lll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᠀")],
                bstack1l1lll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᠁"): step[bstack1l1lll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᠂")],
                bstack1l1lll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᠃"): step[bstack1l1lll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᠄")],
                bstack1l1lll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ᠅"): step[bstack1l1lll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭᠆")]
            }
            if bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᠇") in step:
                bstack11l11l11l1l_opy_[bstack1l1lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᠈")] = step[bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠉")]
            elif bstack1l1lll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᠊") in step:
                bstack11l11l11l1l_opy_[bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᠋")] = step[bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᠌")]
            bstack11l11ll111l_opy_.append(bstack11l11l11l1l_opy_)
        cls.bstack11l1lll1l1_opy_({
            bstack1l1lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ᠍"): bstack1l1lll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ᠎"),
            bstack1l1lll1_opy_ (u"࠭࡬ࡰࡩࡶࠫ᠏"): bstack11l11ll111l_opy_
        })
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1_opy_, stage=STAGE.bstack1lllll111l_opy_)
    def bstack1lll111l11_opy_(cls, screenshot):
        cls.bstack11l1lll1l1_opy_({
            bstack1l1lll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ᠐"): bstack1l1lll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ᠑"),
            bstack1l1lll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ᠒"): [{
                bstack1l1lll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ᠓"): bstack1l1lll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭᠔"),
                bstack1l1lll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᠕"): datetime.datetime.utcnow().isoformat() + bstack1l1lll1_opy_ (u"࡚࠭ࠨ᠖"),
                bstack1l1lll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᠗"): screenshot[bstack1l1lll1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ᠘")],
                bstack1l1lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᠙"): screenshot[bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᠚")]
            }]
        }, event_url=bstack1l1lll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ᠛"))
    @classmethod
    @bstack111ll111l1_opy_(class_method=True)
    def bstack1llllllll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1lll1l1_opy_({
            bstack1l1lll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᠜"): bstack1l1lll1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ᠝"),
            bstack1l1lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᠞"): {
                bstack1l1lll1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᠟"): cls.current_test_uuid(),
                bstack1l1lll1_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᠠ"): cls.bstack111lll11l1_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1111111_opy_(cls, event: str, bstack111l11l1l1_opy_: bstack1111llll1l_opy_):
        bstack111l1l11l1_opy_ = {
            bstack1l1lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᠡ"): event,
            bstack111l11l1l1_opy_.bstack111l1l1l11_opy_(): bstack111l11l1l1_opy_.bstack111l1lllll_opy_(event)
        }
        cls.bstack11l1lll1l1_opy_(bstack111l1l11l1_opy_)
        result = getattr(bstack111l11l1l1_opy_, bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᠢ"), None)
        if event == bstack1l1lll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᠣ"):
            threading.current_thread().bstackTestMeta = {bstack1l1lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᠤ"): bstack1l1lll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᠥ")}
        elif event == bstack1l1lll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᠦ"):
            threading.current_thread().bstackTestMeta = {bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᠧ"): getattr(result, bstack1l1lll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᠨ"), bstack1l1lll1_opy_ (u"ࠫࠬᠩ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᠪ"), None) is None or os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᠫ")] == bstack1l1lll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᠬ")) and (os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᠭ"), None) is None or os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᠮ")] == bstack1l1lll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᠯ")):
            return False
        return True
    @staticmethod
    def bstack11l11ll1111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᠰ"): bstack1l1lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᠱ"),
            bstack1l1lll1_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᠲ"): bstack1l1lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᠳ")
        }
        if os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᠴ"), None):
            headers[bstack1l1lll1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᠵ")] = bstack1l1lll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᠶ").format(os.environ[bstack1l1lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣᠷ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1lll1_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᠸ").format(bstack11l11l11l11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᠹ"), None)
    @staticmethod
    def bstack111lll11l1_opy_(driver):
        return {
            bstack11l11l111ll_opy_(): bstack11l11l111l1_opy_(driver)
        }
    @staticmethod
    def bstack11l111lllll_opy_(exception_info, report):
        return [{bstack1l1lll1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᠺ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l111l1_opy_(typename):
        if bstack1l1lll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᠻ") in typename:
            return bstack1l1lll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᠼ")
        return bstack1l1lll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᠽ")