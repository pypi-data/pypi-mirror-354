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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l1llll1l_opy_, bstack111l1lllll1_opy_
import tempfile
import json
bstack111111ll1ll_opy_ = os.getenv(bstack1l1lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦῥ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨῦ"))
bstack111111l1l11_opy_ = os.path.join(bstack1l1lll1_opy_ (u"ࠧࡲ࡯ࡨࠤῧ"), bstack1l1lll1_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪῨ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1lll1_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪῩ"),
      datefmt=bstack1l1lll1_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭Ὺ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll11111_opy_():
  bstack111111lllll_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢΎ"), bstack1l1lll1_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤῬ"))
  return logging.DEBUG if bstack111111lllll_opy_.lower() == bstack1l1lll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ῭") else logging.INFO
def bstack1ll1111111l_opy_():
  global bstack111111ll1ll_opy_
  if os.path.exists(bstack111111ll1ll_opy_):
    os.remove(bstack111111ll1ll_opy_)
  if os.path.exists(bstack111111l1l11_opy_):
    os.remove(bstack111111l1l11_opy_)
def bstack1ll11l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11llllll_opy_(config, log_level):
  bstack111111l11l1_opy_ = log_level
  if bstack1l1lll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ΅") in config and config[bstack1l1lll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ`")] in bstack111l1llll1l_opy_:
    bstack111111l11l1_opy_ = bstack111l1llll1l_opy_[config[bstack1l1lll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ῰")]]
  if config.get(bstack1l1lll1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ῱"), False):
    logging.getLogger().setLevel(bstack111111l11l1_opy_)
    return bstack111111l11l1_opy_
  global bstack111111ll1ll_opy_
  bstack1ll11l111l_opy_()
  bstack111111l1lll_opy_ = logging.Formatter(
    fmt=bstack1l1lll1_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬῲ"),
    datefmt=bstack1l1lll1_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨῳ"),
  )
  bstack111111ll11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111111ll1ll_opy_)
  file_handler.setFormatter(bstack111111l1lll_opy_)
  bstack111111ll11l_opy_.setFormatter(bstack111111l1lll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111111ll11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1lll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ῴ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111111ll11l_opy_.setLevel(bstack111111l11l1_opy_)
  logging.getLogger().addHandler(bstack111111ll11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111111l11l1_opy_
def bstack11111l11l11_opy_(config):
  try:
    bstack111111lll1l_opy_ = set(bstack111l1lllll1_opy_)
    bstack11111l1111l_opy_ = bstack1l1lll1_opy_ (u"ࠬ࠭῵")
    with open(bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩῶ")) as bstack111111l11ll_opy_:
      bstack111111ll111_opy_ = bstack111111l11ll_opy_.read()
      bstack11111l1111l_opy_ = re.sub(bstack1l1lll1_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨῷ"), bstack1l1lll1_opy_ (u"ࠨࠩῸ"), bstack111111ll111_opy_, flags=re.M)
      bstack11111l1111l_opy_ = re.sub(
        bstack1l1lll1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬΌ") + bstack1l1lll1_opy_ (u"ࠪࢀࠬῺ").join(bstack111111lll1l_opy_) + bstack1l1lll1_opy_ (u"ࠫ࠮࠴ࠪࠥࠩΏ"),
        bstack1l1lll1_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧῼ"),
        bstack11111l1111l_opy_, flags=re.M | re.I
      )
    def bstack11111l11lll_opy_(dic):
      bstack111111ll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111111lll1l_opy_:
          bstack111111ll1l1_opy_[key] = bstack1l1lll1_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪ´")
        else:
          if isinstance(value, dict):
            bstack111111ll1l1_opy_[key] = bstack11111l11lll_opy_(value)
          else:
            bstack111111ll1l1_opy_[key] = value
      return bstack111111ll1l1_opy_
    bstack111111ll1l1_opy_ = bstack11111l11lll_opy_(config)
    return {
      bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ῾"): bstack11111l1111l_opy_,
      bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ῿"): json.dumps(bstack111111ll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack11111l111l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1lll1_opy_ (u"ࠩ࡯ࡳ࡬࠭ "))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11lll1ll1l1_opy_ = os.path.join(log_dir, bstack1l1lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ "))
  if not os.path.exists(bstack11lll1ll1l1_opy_):
    bstack111111llll1_opy_ = {
      bstack1l1lll1_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ "): str(inipath),
      bstack1l1lll1_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ "): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ ")), bstack1l1lll1_opy_ (u"ࠧࡸࠩ ")) as bstack111111l1ll1_opy_:
      bstack111111l1ll1_opy_.write(json.dumps(bstack111111llll1_opy_))
def bstack11111l11l1l_opy_():
  try:
    bstack11lll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1lll1_opy_ (u"ࠨ࡮ࡲ࡫ࠬ "), bstack1l1lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ "))
    if os.path.exists(bstack11lll1ll1l1_opy_):
      with open(bstack11lll1ll1l1_opy_, bstack1l1lll1_opy_ (u"ࠪࡶࠬ ")) as bstack111111l1ll1_opy_:
        bstack11111l11111_opy_ = json.load(bstack111111l1ll1_opy_)
      return bstack11111l11111_opy_.get(bstack1l1lll1_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ "), bstack1l1lll1_opy_ (u"ࠬ࠭ ")), bstack11111l11111_opy_.get(bstack1l1lll1_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ​"), bstack1l1lll1_opy_ (u"ࠧࠨ‌"))
  except:
    pass
  return None, None
def bstack11111l11ll1_opy_():
  try:
    bstack11lll1ll1l1_opy_ = os.path.join(os.getcwd(), bstack1l1lll1_opy_ (u"ࠨ࡮ࡲ࡫ࠬ‍"), bstack1l1lll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ‎"))
    if os.path.exists(bstack11lll1ll1l1_opy_):
      os.remove(bstack11lll1ll1l1_opy_)
  except:
    pass
def bstack1111ll111_opy_(config):
  from bstack_utils.helper import bstack111l111l1_opy_
  global bstack111111ll1ll_opy_
  try:
    if config.get(bstack1l1lll1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ‏"), False):
      return
    uuid = os.getenv(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ‐")) if os.getenv(bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ‑")) else bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣ‒"))
    if not uuid or uuid == bstack1l1lll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ–"):
      return
    bstack11111l111ll_opy_ = [bstack1l1lll1_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫ—"), bstack1l1lll1_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪ―"), bstack1l1lll1_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫ‖"), bstack111111ll1ll_opy_, bstack111111l1l11_opy_]
    bstack111111l1l1l_opy_, root_path = bstack11111l11l1l_opy_()
    if bstack111111l1l1l_opy_ != None:
      bstack11111l111ll_opy_.append(bstack111111l1l1l_opy_)
    if root_path != None:
      bstack11111l111ll_opy_.append(os.path.join(root_path, bstack1l1lll1_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩ‗")))
    bstack1ll11l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫ‘") + uuid + bstack1l1lll1_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧ’"))
    with tarfile.open(output_file, bstack1l1lll1_opy_ (u"ࠢࡸ࠼ࡪࡾࠧ‚")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11111l111ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111l11l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111111lll11_opy_ = data.encode()
        tarinfo.size = len(bstack111111lll11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111111lll11_opy_))
    bstack1l1ll11ll1_opy_ = MultipartEncoder(
      fields= {
        bstack1l1lll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭‛"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1lll1_opy_ (u"ࠩࡵࡦࠬ“")), bstack1l1lll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨ”")),
        bstack1l1lll1_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭„"): uuid
      }
    )
    response = requests.post(
      bstack1l1lll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢ‟"),
      data=bstack1l1ll11ll1_opy_,
      headers={bstack1l1lll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ†"): bstack1l1ll11ll1_opy_.content_type},
      auth=(config[bstack1l1lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ‡")], config[bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ•")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ‣") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1lll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ․") + str(e))
  finally:
    try:
      bstack1ll1111111l_opy_()
      bstack11111l11ll1_opy_()
    except:
      pass