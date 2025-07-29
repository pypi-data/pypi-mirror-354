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
import logging
logger = logging.getLogger(__name__)
bstack11l1ll11l1l_opy_ = 1000
bstack11l1ll1ll11_opy_ = 2
class bstack11l1ll1l1l1_opy_:
    def __init__(self, handler, bstack11l1ll11ll1_opy_=bstack11l1ll11l1l_opy_, bstack11l1ll1l111_opy_=bstack11l1ll1ll11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11l1ll11ll1_opy_ = bstack11l1ll11ll1_opy_
        self.bstack11l1ll1l111_opy_ = bstack11l1ll1l111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack11111llll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack11l1ll111ll_opy_()
    def bstack11l1ll111ll_opy_(self):
        self.bstack11111llll1_opy_ = threading.Event()
        def bstack11l1ll1l11l_opy_():
            self.bstack11111llll1_opy_.wait(self.bstack11l1ll1l111_opy_)
            if not self.bstack11111llll1_opy_.is_set():
                self.bstack11l1ll11lll_opy_()
        self.timer = threading.Thread(target=bstack11l1ll1l11l_opy_, daemon=True)
        self.timer.start()
    def bstack11l1ll1l1ll_opy_(self):
        try:
            if self.bstack11111llll1_opy_ and not self.bstack11111llll1_opy_.is_set():
                self.bstack11111llll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫᚈ") + (str(e) or bstack1l1lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤᚉ")))
        finally:
            self.timer = None
    def bstack11l1ll11l11_opy_(self):
        if self.timer:
            self.bstack11l1ll1l1ll_opy_()
        self.bstack11l1ll111ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11l1ll11ll1_opy_:
                threading.Thread(target=self.bstack11l1ll11lll_opy_).start()
    def bstack11l1ll11lll_opy_(self, source = bstack1l1lll1_opy_ (u"ࠩࠪᚊ")):
        with self.lock:
            if not self.queue:
                self.bstack11l1ll11l11_opy_()
                return
            data = self.queue[:self.bstack11l1ll11ll1_opy_]
            del self.queue[:self.bstack11l1ll11ll1_opy_]
        self.handler(data)
        if source != bstack1l1lll1_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬᚋ"):
            self.bstack11l1ll11l11_opy_()
    def shutdown(self):
        self.bstack11l1ll1l1ll_opy_()
        while self.queue:
            self.bstack11l1ll11lll_opy_(source=bstack1l1lll1_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᚌ"))