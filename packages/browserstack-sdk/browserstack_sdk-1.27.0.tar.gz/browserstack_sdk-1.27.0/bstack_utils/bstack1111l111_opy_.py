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
from collections import deque
from bstack_utils.constants import *
class bstack1ll1ll11ll_opy_:
    def __init__(self):
        self._11ll11l1ll1_opy_ = deque()
        self._11ll111llll_opy_ = {}
        self._11ll11l1lll_opy_ = False
    def bstack11ll11l1l11_opy_(self, test_name, bstack11ll111lll1_opy_):
        bstack11ll11l111l_opy_ = self._11ll111llll_opy_.get(test_name, {})
        return bstack11ll11l111l_opy_.get(bstack11ll111lll1_opy_, 0)
    def bstack11ll11l1111_opy_(self, test_name, bstack11ll111lll1_opy_):
        bstack11ll11ll1ll_opy_ = self.bstack11ll11l1l11_opy_(test_name, bstack11ll111lll1_opy_)
        self.bstack11ll11l11ll_opy_(test_name, bstack11ll111lll1_opy_)
        return bstack11ll11ll1ll_opy_
    def bstack11ll11l11ll_opy_(self, test_name, bstack11ll111lll1_opy_):
        if test_name not in self._11ll111llll_opy_:
            self._11ll111llll_opy_[test_name] = {}
        bstack11ll11l111l_opy_ = self._11ll111llll_opy_[test_name]
        bstack11ll11ll1ll_opy_ = bstack11ll11l111l_opy_.get(bstack11ll111lll1_opy_, 0)
        bstack11ll11l111l_opy_[bstack11ll111lll1_opy_] = bstack11ll11ll1ll_opy_ + 1
    def bstack1lll1l111_opy_(self, bstack11ll11ll1l1_opy_, bstack11ll11l1l1l_opy_):
        bstack11ll11ll11l_opy_ = self.bstack11ll11l1111_opy_(bstack11ll11ll1l1_opy_, bstack11ll11l1l1l_opy_)
        event_name = bstack11ll11ll111_opy_[bstack11ll11l1l1l_opy_]
        bstack1l1ll111l1l_opy_ = bstack1l1lll1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᘕ").format(bstack11ll11ll1l1_opy_, event_name, bstack11ll11ll11l_opy_)
        self._11ll11l1ll1_opy_.append(bstack1l1ll111l1l_opy_)
    def bstack11l111ll11_opy_(self):
        return len(self._11ll11l1ll1_opy_) == 0
    def bstack11ll1l11_opy_(self):
        bstack11ll11l11l1_opy_ = self._11ll11l1ll1_opy_.popleft()
        return bstack11ll11l11l1_opy_
    def capturing(self):
        return self._11ll11l1lll_opy_
    def bstack1l111ll1ll_opy_(self):
        self._11ll11l1lll_opy_ = True
    def bstack11l1lll1l_opy_(self):
        self._11ll11l1lll_opy_ = False