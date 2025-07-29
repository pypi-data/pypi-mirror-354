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
import builtins
import logging
class bstack11l1111l11_opy_:
    def __init__(self, handler):
        self._111ll11l111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111ll11l1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1lll1_opy_ (u"ࠧࡪࡰࡩࡳࠬᨏ"), bstack1l1lll1_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᨐ"), bstack1l1lll1_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᨑ"), bstack1l1lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᨒ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111ll111ll1_opy_
        self._111ll11l11l_opy_()
    def _111ll111ll1_opy_(self, *args, **kwargs):
        self._111ll11l111_opy_(*args, **kwargs)
        message = bstack1l1lll1_opy_ (u"ࠫࠥ࠭ᨓ").join(map(str, args)) + bstack1l1lll1_opy_ (u"ࠬࡢ࡮ࠨᨔ")
        self._log_message(bstack1l1lll1_opy_ (u"࠭ࡉࡏࡈࡒࠫᨕ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1lll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᨖ"): level, bstack1l1lll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᨗ"): msg})
    def _111ll11l11l_opy_(self):
        for level, bstack111ll111lll_opy_ in self._111ll11l1ll_opy_.items():
            setattr(logging, level, self._111ll11l1l1_opy_(level, bstack111ll111lll_opy_))
    def _111ll11l1l1_opy_(self, level, bstack111ll111lll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111ll111lll_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111ll11l111_opy_
        for level, bstack111ll111lll_opy_ in self._111ll11l1ll_opy_.items():
            setattr(logging, level, bstack111ll111lll_opy_)