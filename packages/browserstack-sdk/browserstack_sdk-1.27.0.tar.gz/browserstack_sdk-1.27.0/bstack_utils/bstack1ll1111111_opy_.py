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
class bstack1lll1l111l_opy_:
    def __init__(self, handler):
        self._11l1l1l11l1_opy_ = None
        self.handler = handler
        self._11l1l1l1l11_opy_ = self.bstack11l1l1l11ll_opy_()
        self.patch()
    def patch(self):
        self._11l1l1l11l1_opy_ = self._11l1l1l1l11_opy_.execute
        self._11l1l1l1l11_opy_.execute = self.bstack11l1l1l1l1l_opy_()
    def bstack11l1l1l1l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1lll1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᛌ"), driver_command, None, this, args)
            response = self._11l1l1l11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1lll1_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᛍ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11l1l1l1l11_opy_.execute = self._11l1l1l11l1_opy_
    @staticmethod
    def bstack11l1l1l11ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver