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
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1l1l_opy_, bstack1111lll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11l1ll_opy_(bstack1111l11l11_opy_):
        bstack1111l1111l_opy_ = []
        if bstack1111l11l11_opy_:
            tokens = str(os.path.basename(bstack1111l11l11_opy_)).split(bstack1l1lll1_opy_ (u"ࠥࡣࠧဳ"))
            camelcase_name = bstack1l1lll1_opy_ (u"ࠦࠥࠨဴ").join(t.title() for t in tokens)
            suite_name, bstack1111l111ll_opy_ = os.path.splitext(camelcase_name)
            bstack1111l1111l_opy_.append(suite_name)
        return bstack1111l1111l_opy_
    @staticmethod
    def bstack1111l111l1_opy_(typename):
        if bstack1l1lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣဵ") in typename:
            return bstack1l1lll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢံ")
        return bstack1l1lll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲ့ࠣ")