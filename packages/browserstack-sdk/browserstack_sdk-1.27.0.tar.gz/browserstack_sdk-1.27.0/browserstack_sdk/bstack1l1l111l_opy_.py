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
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111ll11l1_opy_():
  def __init__(self, args, logger, bstack1111ll1l1l_opy_, bstack1111lll1ll_opy_, bstack1111l11ll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
    self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    self.bstack1111l11ll1_opy_ = bstack1111l11ll1_opy_
  def bstack1ll111l11l_opy_(self, bstack1111ll1l11_opy_, bstack1lll11l1l1_opy_, bstack1111l11l1l_opy_=False):
    bstack1111l1l1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1ll11_opy_ = manager.list()
    bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
    if bstack1111l11l1l_opy_:
      for index, platform in enumerate(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ာ")]):
        if index == 0:
          bstack1lll11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧိ")] = self.args
        bstack1111l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1l11_opy_,
                                                    args=(bstack1lll11l1l1_opy_, bstack1111l1ll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨီ")]):
        bstack1111l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1l11_opy_,
                                                    args=(bstack1lll11l1l1_opy_, bstack1111l1ll11_opy_)))
    i = 0
    for t in bstack1111l1l1l_opy_:
      try:
        if bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧု")):
          os.environ[bstack1l1lll1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨူ")] = json.dumps(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫေ")][i % self.bstack1111l11ll1_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤဲ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1111l1l1l_opy_:
      t.join()
    return list(bstack1111l1ll11_opy_)