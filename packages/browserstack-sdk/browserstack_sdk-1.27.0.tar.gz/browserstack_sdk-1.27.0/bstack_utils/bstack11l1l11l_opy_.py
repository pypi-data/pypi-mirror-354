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
import json
from bstack_utils.bstack1l111111l_opy_ import get_logger
logger = get_logger(__name__)
class bstack111ll1l11ll_opy_(object):
  bstack11l1l111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1lll1_opy_ (u"ࠨࢀࠪ᧟")), bstack1l1lll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᧠"))
  bstack111ll1l1l1l_opy_ = os.path.join(bstack11l1l111ll_opy_, bstack1l1lll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪ᧡"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1l11ll_opy_ = None
  bstack1111l11l1_opy_ = None
  bstack111llll1l1l_opy_ = None
  bstack11l11l11111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1lll1_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭᧢")):
      cls.instance = super(bstack111ll1l11ll_opy_, cls).__new__(cls)
      cls.instance.bstack111ll1l1l11_opy_()
    return cls.instance
  def bstack111ll1l1l11_opy_(self):
    try:
      with open(self.bstack111ll1l1l1l_opy_, bstack1l1lll1_opy_ (u"ࠬࡸࠧ᧣")) as bstack11llll1lll_opy_:
        bstack111ll1l11l1_opy_ = bstack11llll1lll_opy_.read()
        data = json.loads(bstack111ll1l11l1_opy_)
        if bstack1l1lll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᧤") in data:
          self.bstack11l11l1l111_opy_(data[bstack1l1lll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ᧥")])
        if bstack1l1lll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᧦") in data:
          self.bstack1lllllll1l_opy_(data[bstack1l1lll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᧧")])
        if bstack1l1lll1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᧨") in data:
          self.bstack11l111ll1l1_opy_(data[bstack1l1lll1_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᧩")])
    except:
      pass
  def bstack11l111ll1l1_opy_(self, bstack11l11l11111_opy_):
    if bstack11l11l11111_opy_ != None:
      self.bstack11l11l11111_opy_ = bstack11l11l11111_opy_
  def bstack1lllllll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1lll1_opy_ (u"ࠬࡹࡣࡢࡰࠪ᧪"),bstack1l1lll1_opy_ (u"࠭ࠧ᧫"))
      self.bstack1l1l11ll_opy_ = scripts.get(bstack1l1lll1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫ᧬"),bstack1l1lll1_opy_ (u"ࠨࠩ᧭"))
      self.bstack1111l11l1_opy_ = scripts.get(bstack1l1lll1_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭᧮"),bstack1l1lll1_opy_ (u"ࠪࠫ᧯"))
      self.bstack111llll1l1l_opy_ = scripts.get(bstack1l1lll1_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩ᧰"),bstack1l1lll1_opy_ (u"ࠬ࠭᧱"))
  def bstack11l11l1l111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack111ll1l1l1l_opy_, bstack1l1lll1_opy_ (u"࠭ࡷࠨ᧲")) as file:
        json.dump({
          bstack1l1lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤ᧳"): self.commands_to_wrap,
          bstack1l1lll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤ᧴"): {
            bstack1l1lll1_opy_ (u"ࠤࡶࡧࡦࡴࠢ᧵"): self.perform_scan,
            bstack1l1lll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢ᧶"): self.bstack1l1l11ll_opy_,
            bstack1l1lll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣ᧷"): self.bstack1111l11l1_opy_,
            bstack1l1lll1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥ᧸"): self.bstack111llll1l1l_opy_
          },
          bstack1l1lll1_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥ᧹"): self.bstack11l11l11111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧ᧺").format(e))
      pass
  def bstack1l1111ll11_opy_(self, bstack1ll1l1l11ll_opy_):
    try:
      return any(command.get(bstack1l1lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭᧻")) == bstack1ll1l1l11ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11l1l11l_opy_ = bstack111ll1l11ll_opy_()