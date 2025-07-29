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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l1ll11111_opy_ import bstack11l1l1ll1l1_opy_
from bstack_utils.constants import *
import json
class bstack11ll1ll111_opy_:
    def __init__(self, bstack11lll1llll_opy_, bstack111ll1l111l_opy_):
        self.bstack11lll1llll_opy_ = bstack11lll1llll_opy_
        self.bstack111ll1l111l_opy_ = bstack111ll1l111l_opy_
        self.bstack111ll11ll11_opy_ = None
    def __call__(self):
        bstack111ll11ll1l_opy_ = {}
        while True:
            self.bstack111ll11ll11_opy_ = bstack111ll11ll1l_opy_.get(
                bstack1l1lll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ᧼"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111ll1l1111_opy_ = self.bstack111ll11ll11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111ll1l1111_opy_ > 0:
                sleep(bstack111ll1l1111_opy_ / 1000)
            params = {
                bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᧽"): self.bstack11lll1llll_opy_,
                bstack1l1lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ᧾"): int(datetime.now().timestamp() * 1000)
            }
            bstack111ll11llll_opy_ = bstack1l1lll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᧿") + bstack111ll11lll1_opy_ + bstack1l1lll1_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᨀ")
            if self.bstack111ll1l111l_opy_.lower() == bstack1l1lll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᨁ"):
                bstack111ll11ll1l_opy_ = bstack11l1l1ll1l1_opy_.results(bstack111ll11llll_opy_, params)
            else:
                bstack111ll11ll1l_opy_ = bstack11l1l1ll1l1_opy_.bstack11l1l1lll11_opy_(bstack111ll11llll_opy_, params)
            if str(bstack111ll11ll1l_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᨂ"), bstack1l1lll1_opy_ (u"ࠩ࠵࠴࠵࠭ᨃ"))) != bstack1l1lll1_opy_ (u"ࠪ࠸࠵࠺ࠧᨄ"):
                break
        return bstack111ll11ll1l_opy_.get(bstack1l1lll1_opy_ (u"ࠫࡩࡧࡴࡢࠩᨅ"), bstack111ll11ll1l_opy_)