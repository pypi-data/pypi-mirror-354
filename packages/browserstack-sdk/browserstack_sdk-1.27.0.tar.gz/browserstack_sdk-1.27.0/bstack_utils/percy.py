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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1llllll111_opy_, bstack1lll1l1ll1_opy_
from bstack_utils.measure import measure
class bstack111lll11l_opy_:
  working_dir = os.getcwd()
  bstack11ll111ll_opy_ = False
  config = {}
  bstack11lll11ll11_opy_ = bstack1l1lll1_opy_ (u"࠭ࠧᖒ")
  binary_path = bstack1l1lll1_opy_ (u"ࠧࠨᖓ")
  bstack11ll1ll1lll_opy_ = bstack1l1lll1_opy_ (u"ࠨࠩᖔ")
  bstack1l1l11l11_opy_ = False
  bstack11ll1ll111l_opy_ = None
  bstack11lll1l1ll1_opy_ = {}
  bstack11lll1111l1_opy_ = 300
  bstack11ll11lll1l_opy_ = False
  logger = None
  bstack11ll1llll11_opy_ = False
  bstack1lll111ll1_opy_ = False
  percy_build_id = None
  bstack11ll1lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠩࠪᖕ")
  bstack11ll1l1l11l_opy_ = {
    bstack1l1lll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᖖ") : 1,
    bstack1l1lll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᖗ") : 2,
    bstack1l1lll1_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᖘ") : 3,
    bstack1l1lll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᖙ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11lll11l1ll_opy_(self):
    bstack11ll1ll1l1l_opy_ = bstack1l1lll1_opy_ (u"ࠧࠨᖚ")
    bstack11lll1l11ll_opy_ = sys.platform
    bstack11ll1l1ll1l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᖛ")
    if re.match(bstack1l1lll1_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᖜ"), bstack11lll1l11ll_opy_) != None:
      bstack11ll1ll1l1l_opy_ = bstack11llll11l1l_opy_ + bstack1l1lll1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᖝ")
      self.bstack11ll1lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠫࡲࡧࡣࠨᖞ")
    elif re.match(bstack1l1lll1_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᖟ"), bstack11lll1l11ll_opy_) != None:
      bstack11ll1ll1l1l_opy_ = bstack11llll11l1l_opy_ + bstack1l1lll1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᖠ")
      bstack11ll1l1ll1l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᖡ")
      self.bstack11ll1lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠨࡹ࡬ࡲࠬᖢ")
    else:
      bstack11ll1ll1l1l_opy_ = bstack11llll11l1l_opy_ + bstack1l1lll1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᖣ")
      self.bstack11ll1lll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᖤ")
    return bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_
  def bstack11ll1ll1ll1_opy_(self):
    try:
      bstack11lll1lll1l_opy_ = [os.path.join(expanduser(bstack1l1lll1_opy_ (u"ࠦࢃࠨᖥ")), bstack1l1lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᖦ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11lll1lll1l_opy_:
        if(self.bstack11ll1l111l1_opy_(path)):
          return path
      raise bstack1l1lll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᖧ")
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤᖨ").format(e))
  def bstack11ll1l111l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11ll1l1lll1_opy_(self, bstack11ll1ll1111_opy_):
    return os.path.join(bstack11ll1ll1111_opy_, self.bstack11lll11ll11_opy_ + bstack1l1lll1_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢᖩ"))
  def bstack11ll11lll11_opy_(self, bstack11ll1ll1111_opy_, bstack11lll1ll1ll_opy_):
    if not bstack11lll1ll1ll_opy_: return
    try:
      bstack11ll1ll1l11_opy_ = self.bstack11ll1l1lll1_opy_(bstack11ll1ll1111_opy_)
      with open(bstack11ll1ll1l11_opy_, bstack1l1lll1_opy_ (u"ࠤࡺࠦᖪ")) as f:
        f.write(bstack11lll1ll1ll_opy_)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢᖫ"))
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᖬ").format(e))
  def bstack11ll1ll11l1_opy_(self, bstack11ll1ll1111_opy_):
    try:
      bstack11ll1ll1l11_opy_ = self.bstack11ll1l1lll1_opy_(bstack11ll1ll1111_opy_)
      if os.path.exists(bstack11ll1ll1l11_opy_):
        with open(bstack11ll1ll1l11_opy_, bstack1l1lll1_opy_ (u"ࠧࡸࠢᖭ")) as f:
          bstack11lll1ll1ll_opy_ = f.read().strip()
          return bstack11lll1ll1ll_opy_ if bstack11lll1ll1ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᖮ").format(e))
  def bstack11ll1l11l1l_opy_(self, bstack11ll1ll1111_opy_, bstack11ll1ll1l1l_opy_):
    bstack11lll11llll_opy_ = self.bstack11ll1ll11l1_opy_(bstack11ll1ll1111_opy_)
    if bstack11lll11llll_opy_:
      try:
        bstack11lll11ll1l_opy_ = self.bstack11lll11l11l_opy_(bstack11lll11llll_opy_, bstack11ll1ll1l1l_opy_)
        if not bstack11lll11ll1l_opy_:
          self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤᖯ"))
          return True
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢᖰ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᖱ").format(e))
    return False
  def bstack11lll11l11l_opy_(self, bstack11lll11llll_opy_, bstack11ll1ll1l1l_opy_):
    try:
      headers = {
        bstack1l1lll1_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥᖲ"): bstack11lll11llll_opy_
      }
      response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"ࠫࡌࡋࡔࠨᖳ"), bstack11ll1ll1l1l_opy_, {}, {bstack1l1lll1_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨᖴ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣᖵ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lllll1_opy_, stage=STAGE.bstack1lllll111l_opy_)
  def bstack11lll1l1111_opy_(self, bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_):
    try:
      bstack11llll11l11_opy_ = self.bstack11ll1ll1ll1_opy_()
      bstack11lll11111l_opy_ = os.path.join(bstack11llll11l11_opy_, bstack1l1lll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪᖶ"))
      bstack11lll111ll1_opy_ = os.path.join(bstack11llll11l11_opy_, bstack11ll1l1ll1l_opy_)
      if self.bstack11ll1l11l1l_opy_(bstack11llll11l11_opy_, bstack11ll1ll1l1l_opy_): # if bstack11lll1lllll_opy_, bstack1l1l1l1ll11_opy_ bstack11lll1ll1ll_opy_ is bstack11lll111lll_opy_ to bstack11llll1111l_opy_ version available (response 304)
        if os.path.exists(bstack11lll111ll1_opy_):
          self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᖷ").format(bstack11lll111ll1_opy_))
          return bstack11lll111ll1_opy_
        if os.path.exists(bstack11lll11111l_opy_):
          self.logger.info(bstack1l1lll1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢᖸ").format(bstack11lll11111l_opy_))
          return self.bstack11lll1lll11_opy_(bstack11lll11111l_opy_, bstack11ll1l1ll1l_opy_)
      self.logger.info(bstack1l1lll1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣᖹ").format(bstack11ll1ll1l1l_opy_))
      response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"ࠫࡌࡋࡔࠨᖺ"), bstack11ll1ll1l1l_opy_, {}, {})
      if response.status_code == 200:
        bstack11lll1l11l1_opy_ = response.headers.get(bstack1l1lll1_opy_ (u"ࠧࡋࡔࡢࡩࠥᖻ"), bstack1l1lll1_opy_ (u"ࠨࠢᖼ"))
        if bstack11lll1l11l1_opy_:
          self.bstack11ll11lll11_opy_(bstack11llll11l11_opy_, bstack11lll1l11l1_opy_)
        with open(bstack11lll11111l_opy_, bstack1l1lll1_opy_ (u"ࠧࡸࡤࠪᖽ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᖾ").format(bstack11lll11111l_opy_))
        return self.bstack11lll1lll11_opy_(bstack11lll11111l_opy_, bstack11ll1l1ll1l_opy_)
      else:
        raise(bstack1l1lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᖿ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᗀ").format(e))
  def bstack11lll111l1l_opy_(self, bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_):
    try:
      retry = 2
      bstack11lll111ll1_opy_ = None
      bstack11ll1l11ll1_opy_ = False
      while retry > 0:
        bstack11lll111ll1_opy_ = self.bstack11lll1l1111_opy_(bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_)
        bstack11ll1l11ll1_opy_ = self.bstack11ll1lll11l_opy_(bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_, bstack11lll111ll1_opy_)
        if bstack11ll1l11ll1_opy_:
          break
        retry -= 1
      return bstack11lll111ll1_opy_, bstack11ll1l11ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᗁ").format(e))
    return bstack11lll111ll1_opy_, False
  def bstack11ll1lll11l_opy_(self, bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_, bstack11lll111ll1_opy_, bstack11lll1l1l1l_opy_ = 0):
    if bstack11lll1l1l1l_opy_ > 1:
      return False
    if bstack11lll111ll1_opy_ == None or os.path.exists(bstack11lll111ll1_opy_) == False:
      self.logger.warn(bstack1l1lll1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᗂ"))
      return False
    bstack11lll11l111_opy_ = bstack1l1lll1_opy_ (u"ࡸࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯ࠠ࡝ࡦ࠮ࡠ࠳ࡢࡤࠬ࡞࠱ࡠࡩ࠱ࠢᗃ")
    command = bstack1l1lll1_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᗄ").format(bstack11lll111ll1_opy_)
    bstack11ll1lll111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11lll11l111_opy_, bstack11ll1lll111_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᗅ"))
      return False
  def bstack11lll1lll11_opy_(self, bstack11lll11111l_opy_, bstack11ll1l1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack11lll11111l_opy_)
      shutil.unpack_archive(bstack11lll11111l_opy_, working_dir)
      bstack11lll111ll1_opy_ = os.path.join(working_dir, bstack11ll1l1ll1l_opy_)
      os.chmod(bstack11lll111ll1_opy_, 0o755)
      return bstack11lll111ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᗆ"))
  def bstack11ll1l1l1l1_opy_(self):
    try:
      bstack11ll1l11111_opy_ = self.config.get(bstack1l1lll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᗇ"))
      bstack11ll1l1l1l1_opy_ = bstack11ll1l11111_opy_ or (bstack11ll1l11111_opy_ is None and self.bstack11ll111ll_opy_)
      if not bstack11ll1l1l1l1_opy_ or self.config.get(bstack1l1lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᗈ"), None) not in bstack11llll111l1_opy_:
        return False
      self.bstack1l1l11l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᗉ").format(e))
  def bstack11ll1lll1ll_opy_(self):
    try:
      bstack11ll1lll1ll_opy_ = self.percy_capture_mode
      return bstack11ll1lll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᗊ").format(e))
  def init(self, bstack11ll111ll_opy_, config, logger):
    self.bstack11ll111ll_opy_ = bstack11ll111ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11ll1l1l1l1_opy_():
      return
    self.bstack11lll1l1ll1_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗋ"), {})
    self.percy_capture_mode = config.get(bstack1l1lll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᗌ"))
    try:
      bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_ = self.bstack11lll11l1ll_opy_()
      self.bstack11lll11ll11_opy_ = bstack11ll1l1ll1l_opy_
      bstack11lll111ll1_opy_, bstack11ll1l11ll1_opy_ = self.bstack11lll111l1l_opy_(bstack11ll1ll1l1l_opy_, bstack11ll1l1ll1l_opy_)
      if bstack11ll1l11ll1_opy_:
        self.binary_path = bstack11lll111ll1_opy_
        thread = Thread(target=self.bstack11lll11lll1_opy_)
        thread.start()
      else:
        self.bstack11ll1llll11_opy_ = True
        self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᗍ").format(bstack11lll111ll1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᗎ").format(e))
  def bstack11llll111ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1lll1_opy_ (u"ࠫࡱࡵࡧࠨᗏ"), bstack1l1lll1_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᗐ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1lll1_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᗑ").format(logfile))
      self.bstack11ll1ll1lll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᗒ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l1l111_opy_, stage=STAGE.bstack1lllll111l_opy_)
  def bstack11lll11lll1_opy_(self):
    bstack11ll1llllll_opy_ = self.bstack11ll1ll11ll_opy_()
    if bstack11ll1llllll_opy_ == None:
      self.bstack11ll1llll11_opy_ = True
      self.logger.error(bstack1l1lll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᗓ"))
      return False
    command_args = [bstack1l1lll1_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᗔ") if self.bstack11ll111ll_opy_ else bstack1l1lll1_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᗕ")]
    bstack11lll1ll1l1_opy_ = self.bstack11llll11ll1_opy_()
    if bstack11lll1ll1l1_opy_ != None:
      command_args.append(bstack1l1lll1_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᗖ").format(bstack11lll1ll1l1_opy_))
    env = os.environ.copy()
    env[bstack1l1lll1_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᗗ")] = bstack11ll1llllll_opy_
    env[bstack1l1lll1_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᗘ")] = os.environ.get(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᗙ"), bstack1l1lll1_opy_ (u"ࠨࠩᗚ"))
    bstack11ll1l111ll_opy_ = [self.binary_path]
    self.bstack11llll111ll_opy_()
    self.bstack11ll1ll111l_opy_ = self.bstack11lll1llll1_opy_(bstack11ll1l111ll_opy_ + command_args, env)
    self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᗛ"))
    bstack11lll1l1l1l_opy_ = 0
    while self.bstack11ll1ll111l_opy_.poll() == None:
      bstack11lll111111_opy_ = self.bstack11ll1l1llll_opy_()
      if bstack11lll111111_opy_:
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᗜ"))
        self.bstack11ll11lll1l_opy_ = True
        return True
      bstack11lll1l1l1l_opy_ += 1
      self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᗝ").format(bstack11lll1l1l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᗞ").format(bstack11lll1l1l1l_opy_))
    self.bstack11ll1llll11_opy_ = True
    return False
  def bstack11ll1l1llll_opy_(self, bstack11lll1l1l1l_opy_ = 0):
    if bstack11lll1l1l1l_opy_ > 10:
      return False
    try:
      bstack11ll11llll1_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᗟ"), bstack1l1lll1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᗠ"))
      bstack11llll11111_opy_ = bstack11ll11llll1_opy_ + bstack11ll1l11l11_opy_
      response = requests.get(bstack11llll11111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᗡ"), {}).get(bstack1l1lll1_opy_ (u"ࠩ࡬ࡨࠬᗢ"), None)
      return True
    except:
      self.logger.debug(bstack1l1lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᗣ"))
      return False
  def bstack11ll1ll11ll_opy_(self):
    bstack11lll11l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠫࡦࡶࡰࠨᗤ") if self.bstack11ll111ll_opy_ else bstack1l1lll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᗥ")
    bstack11lll1ll11l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᗦ") if self.config.get(bstack1l1lll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᗧ")) is None else True
    bstack11ll1l11lll_opy_ = bstack1l1lll1_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᗨ").format(self.config[bstack1l1lll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᗩ")], bstack11lll11l1l1_opy_, bstack11lll1ll11l_opy_)
    if self.percy_capture_mode:
      bstack11ll1l11lll_opy_ += bstack1l1lll1_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᗪ").format(self.percy_capture_mode)
    uri = bstack1llllll111_opy_(bstack11ll1l11lll_opy_)
    try:
      response = bstack1lll1l1ll1_opy_(bstack1l1lll1_opy_ (u"ࠫࡌࡋࡔࠨᗫ"), uri, {}, {bstack1l1lll1_opy_ (u"ࠬࡧࡵࡵࡪࠪᗬ"): (self.config[bstack1l1lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᗭ")], self.config[bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᗮ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1l11l11_opy_ = data.get(bstack1l1lll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᗯ"))
        self.percy_capture_mode = data.get(bstack1l1lll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᗰ"))
        os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᗱ")] = str(self.bstack1l1l11l11_opy_)
        os.environ[bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᗲ")] = str(self.percy_capture_mode)
        if bstack11lll1ll11l_opy_ == bstack1l1lll1_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᗳ") and str(self.bstack1l1l11l11_opy_).lower() == bstack1l1lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦᗴ"):
          self.bstack1lll111ll1_opy_ = True
        if bstack1l1lll1_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᗵ") in data:
          return data[bstack1l1lll1_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᗶ")]
        else:
          raise bstack1l1lll1_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᗷ").format(data)
      else:
        raise bstack1l1lll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᗸ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᗹ").format(e))
  def bstack11llll11ll1_opy_(self):
    bstack11lll1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᗺ"))
    try:
      if bstack1l1lll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᗻ") not in self.bstack11lll1l1ll1_opy_:
        self.bstack11lll1l1ll1_opy_[bstack1l1lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᗼ")] = 2
      with open(bstack11lll1l1lll_opy_, bstack1l1lll1_opy_ (u"ࠨࡹࠪᗽ")) as fp:
        json.dump(self.bstack11lll1l1ll1_opy_, fp)
      return bstack11lll1l1lll_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᗾ").format(e))
  def bstack11lll1llll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11ll1lll1l1_opy_ == bstack1l1lll1_opy_ (u"ࠪࡻ࡮ࡴࠧᗿ"):
        bstack11ll1l1111l_opy_ = [bstack1l1lll1_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᘀ"), bstack1l1lll1_opy_ (u"ࠬ࠵ࡣࠨᘁ")]
        cmd = bstack11ll1l1111l_opy_ + cmd
      cmd = bstack1l1lll1_opy_ (u"࠭ࠠࠨᘂ").join(cmd)
      self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᘃ").format(cmd))
      with open(self.bstack11ll1ll1lll_opy_, bstack1l1lll1_opy_ (u"ࠣࡣࠥᘄ")) as bstack11lll1l111l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11lll1l111l_opy_, text=True, stderr=bstack11lll1l111l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11ll1llll11_opy_ = True
      self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᘅ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11ll11lll1l_opy_:
        self.logger.info(bstack1l1lll1_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᘆ"))
        cmd = [self.binary_path, bstack1l1lll1_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᘇ")]
        self.bstack11lll1llll1_opy_(cmd)
        self.bstack11ll11lll1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᘈ").format(cmd, e))
  def bstack11l11ll11l_opy_(self):
    if not self.bstack1l1l11l11_opy_:
      return
    try:
      bstack11ll1l1l1ll_opy_ = 0
      while not self.bstack11ll11lll1l_opy_ and bstack11ll1l1l1ll_opy_ < self.bstack11lll1111l1_opy_:
        if self.bstack11ll1llll11_opy_:
          self.logger.info(bstack1l1lll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᘉ"))
          return
        time.sleep(1)
        bstack11ll1l1l1ll_opy_ += 1
      os.environ[bstack1l1lll1_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᘊ")] = str(self.bstack11ll1llll1l_opy_())
      self.logger.info(bstack1l1lll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᘋ"))
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᘌ").format(e))
  def bstack11ll1llll1l_opy_(self):
    if self.bstack11ll111ll_opy_:
      return
    try:
      bstack11lll1ll111_opy_ = [platform[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘍ")].lower() for platform in self.config.get(bstack1l1lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘎ"), [])]
      bstack11lll1111ll_opy_ = sys.maxsize
      bstack11lll1l1l11_opy_ = bstack1l1lll1_opy_ (u"ࠬ࠭ᘏ")
      for browser in bstack11lll1ll111_opy_:
        if browser in self.bstack11ll1l1l11l_opy_:
          bstack11lll111l11_opy_ = self.bstack11ll1l1l11l_opy_[browser]
        if bstack11lll111l11_opy_ < bstack11lll1111ll_opy_:
          bstack11lll1111ll_opy_ = bstack11lll111l11_opy_
          bstack11lll1l1l11_opy_ = browser
      return bstack11lll1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᘐ").format(e))
  @classmethod
  def bstack1ll111ll1_opy_(self):
    return os.getenv(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᘑ"), bstack1l1lll1_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᘒ")).lower()
  @classmethod
  def bstack1l1ll111_opy_(self):
    return os.getenv(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᘓ"), bstack1l1lll1_opy_ (u"ࠪࠫᘔ"))
  @classmethod
  def bstack1l1ll11l1l1_opy_(cls, value):
    cls.bstack1lll111ll1_opy_ = value
  @classmethod
  def bstack11ll1l1ll11_opy_(cls):
    return cls.bstack1lll111ll1_opy_
  @classmethod
  def bstack1l1ll11l11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11ll11lllll_opy_(cls):
    return cls.percy_build_id