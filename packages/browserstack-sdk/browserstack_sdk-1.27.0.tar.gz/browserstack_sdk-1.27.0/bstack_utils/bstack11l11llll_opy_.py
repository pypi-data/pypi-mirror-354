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
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l1ll11111_opy_ import bstack11l1l1ll1l1_opy_
from bstack_utils.constants import bstack111l1ll1ll1_opy_, bstack1l11ll111l_opy_
from bstack_utils.bstack1l1l1ll1ll_opy_ import bstack11ll1l1ll1_opy_
from bstack_utils import bstack1l111111l_opy_
bstack111l11l11ll_opy_ = 10
class bstack1llll11l1_opy_:
    def __init__(self, bstack11ll11ll_opy_, config, bstack111l11l1ll1_opy_=0):
        self.bstack111l1l1111l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l1l11l11_opy_ = bstack1l1lll1_opy_ (u"ࠢࡼࡿ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤᵐ").format(bstack111l1ll1ll1_opy_)
        self.bstack111l11ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤᵑ").format(os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᵒ"))))
        self.bstack111l1l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤᵓ").format(os.environ.get(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᵔ"))))
        self.bstack111l11llll1_opy_ = 2
        self.bstack11ll11ll_opy_ = bstack11ll11ll_opy_
        self.config = config
        self.logger = bstack1l111111l_opy_.get_logger(__name__, bstack1l11ll111l_opy_)
        self.bstack111l11l1ll1_opy_ = bstack111l11l1ll1_opy_
        self.bstack111l11ll111_opy_ = False
        self.bstack111l11lllll_opy_ = not (
                            os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦᵕ")) and
                            os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᵖ")) and
                            os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᵗ"))
                        )
        if bstack11ll1l1ll1_opy_.bstack111l11l111l_opy_(config):
            self.bstack111l11llll1_opy_ = bstack11ll1l1ll1_opy_.bstack111l11l1lll_opy_(config, self.bstack111l11l1ll1_opy_)
            self.bstack111l11l1l1l_opy_()
    def bstack111l11lll1l_opy_(self):
        return bstack1l1lll1_opy_ (u"ࠣࡽࢀࡣࢀࢃࠢᵘ").format(self.config.get(bstack1l1lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᵙ")), os.environ.get(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᵚ")))
    def bstack111l11l11l1_opy_(self):
        try:
            if self.bstack111l11lllll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l1l111l1_opy_, bstack1l1lll1_opy_ (u"ࠦࡷࠨᵛ")) as f:
                        bstack111l11lll11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111l11lll11_opy_ = set()
                bstack111l11ll1l1_opy_ = bstack111l11lll11_opy_ - self.bstack111l1l1111l_opy_
                if not bstack111l11ll1l1_opy_:
                    return
                self.bstack111l1l1111l_opy_.update(bstack111l11ll1l1_opy_)
                data = {bstack1l1lll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࠥᵜ"): list(self.bstack111l1l1111l_opy_), bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤᵝ"): self.config.get(bstack1l1lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᵞ")), bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨᵟ"): os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᵠ")), bstack1l1lll1_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣᵡ"): self.config.get(bstack1l1lll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᵢ"))}
            response = bstack11l1l1ll1l1_opy_.bstack11l1l1l1ll1_opy_(self.bstack111l1l11l11_opy_, data)
            if response.get(bstack1l1lll1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᵣ")) == 200:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡹࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᵤ").format(data))
            else:
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᵥ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᵦ").format(e))
    def bstack11l1l1l1lll_opy_(self):
        if self.bstack111l11lllll_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l1l111l1_opy_, bstack1l1lll1_opy_ (u"ࠤࡵࠦᵧ")) as f:
                        bstack111l11l1l11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111l11l1l11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠨᵨ").format(failed_count))
                if failed_count >= self.bstack111l11llll1_opy_:
                    self.logger.info(bstack1l1lll1_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᵩ").format(failed_count, self.bstack111l11llll1_opy_))
                    self.bstack111l1l11111_opy_(failed_count)
                    self.bstack111l11ll111_opy_ = True
            return
        try:
            response = bstack11l1l1ll1l1_opy_.bstack11l1l1l1lll_opy_(bstack1l1lll1_opy_ (u"ࠧࢁࡽࡀࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࡁࢀࢃࠦࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࡂࢁࡽࠧࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࡃࡻࡾࠤᵪ").format(self.bstack111l1l11l11_opy_, self.config.get(bstack1l1lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᵫ")), os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᵬ")), self.config.get(bstack1l1lll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᵭ"))))
            if response.get(bstack1l1lll1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᵮ")) == 200:
                failed_count = response.get(bstack1l1lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࡄࡱࡸࡲࡹࠨᵯ"), 0)
                self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨᵰ").format(failed_count))
                if failed_count >= self.bstack111l11llll1_opy_:
                    self.logger.info(bstack1l1lll1_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᵱ").format(failed_count, self.bstack111l11llll1_opy_))
                    self.bstack111l1l11111_opy_(failed_count)
                    self.bstack111l11ll111_opy_ = True
            else:
                self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡳࡱࡲࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᵲ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡴࡲ࡬ࡪࡰࡪ࠾ࠥࢁࡽࠣᵳ").format(e))
    def bstack111l1l11111_opy_(self, failed_count):
        with open(self.bstack111l11ll11l_opy_, bstack1l1lll1_opy_ (u"ࠣࡹࠥᵴ")) as f:
            f.write(bstack1l1lll1_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࡡࡵࠢࡾࢁࡡࡴࠢᵵ").format(datetime.now()))
            f.write(bstack1l1lll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࡡࡴࠢᵶ").format(failed_count))
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡆࡨ࡯ࡳࡶࠣࡆࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࢁࠧᵷ").format(self.bstack111l11ll11l_opy_))
    def bstack111l11l1l1l_opy_(self):
        def bstack111l11ll1ll_opy_():
            while not self.bstack111l11ll111_opy_:
                time.sleep(bstack111l11l11ll_opy_)
                self.bstack111l11l11l1_opy_()
                self.bstack11l1l1l1lll_opy_()
        bstack111l1l111ll_opy_ = threading.Thread(target=bstack111l11ll1ll_opy_, daemon=True)
        bstack111l1l111ll_opy_.start()