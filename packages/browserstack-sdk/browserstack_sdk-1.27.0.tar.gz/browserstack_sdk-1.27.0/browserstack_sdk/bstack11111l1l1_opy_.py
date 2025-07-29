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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack111l1ll1l_opy_
import subprocess
from browserstack_sdk.bstack1ll11l1l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1ll1l11_opy_
from bstack_utils.bstack1l1l1ll1ll_opy_ import bstack11ll1l1ll1_opy_
from bstack_utils.constants import bstack1111l1l1ll_opy_
class bstack1l111111ll_opy_:
    def __init__(self, args, logger, bstack1111ll1l1l_opy_, bstack1111lll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1l1lll1_opy_ = []
        self.bstack1111ll1lll_opy_ = None
        self.bstack1ll1l11lll_opy_ = []
        self.bstack1111ll11ll_opy_ = self.bstack1lll1l1l1l_opy_()
        self.bstack1lll1ll1ll_opy_ = -1
    def bstack1lll11l1l1_opy_(self, bstack1111lll1l1_opy_):
        self.parse_args()
        self.bstack1111ll1ll1_opy_()
        self.bstack1111ll111l_opy_(bstack1111lll1l1_opy_)
        self.bstack1111l1l111_opy_()
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111l11lll_opy_():
        import importlib
        if getattr(importlib, bstack1l1lll1_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧခ"), False):
            bstack1111l1l1l1_opy_ = importlib.find_loader(bstack1l1lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬဂ"))
        else:
            bstack1111l1l1l1_opy_ = importlib.util.find_spec(bstack1l1lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ဃ"))
    def bstack1111lll11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll1ll1ll_opy_ = -1
        if self.bstack1111lll1ll_opy_ and bstack1l1lll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬင") in self.bstack1111ll1l1l_opy_:
            self.bstack1lll1ll1ll_opy_ = int(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭စ")])
        try:
            bstack1111ll1111_opy_ = [bstack1l1lll1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩဆ"), bstack1l1lll1_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫဇ"), bstack1l1lll1_opy_ (u"ࠩ࠰ࡴࠬဈ")]
            if self.bstack1lll1ll1ll_opy_ >= 0:
                bstack1111ll1111_opy_.extend([bstack1l1lll1_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫဉ"), bstack1l1lll1_opy_ (u"ࠫ࠲ࡴࠧည")])
            for arg in bstack1111ll1111_opy_:
                self.bstack1111lll11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111ll1ll1_opy_(self):
        bstack1111ll1lll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_
        return bstack1111ll1lll_opy_
    def bstack1lllll1l11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111l11lll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1ll1l11_opy_)
    def bstack1111ll111l_opy_(self, bstack1111lll1l1_opy_):
        bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
        if bstack1111lll1l1_opy_:
            self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩဋ"))
            self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"࠭ࡔࡳࡷࡨࠫဌ"))
        if bstack111l111l1_opy_.bstack1111l1l11l_opy_():
            self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ဍ"))
            self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠨࡖࡵࡹࡪ࠭ဎ"))
        self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠩ࠰ࡴࠬဏ"))
        self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨတ"))
        self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ထ"))
        self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬဒ"))
        if self.bstack1lll1ll1ll_opy_ > 1:
            self.bstack1111ll1lll_opy_.append(bstack1l1lll1_opy_ (u"࠭࠭࡯ࠩဓ"))
            self.bstack1111ll1lll_opy_.append(str(self.bstack1lll1ll1ll_opy_))
    def bstack1111l1l111_opy_(self):
        if bstack11ll1l1ll1_opy_.bstack1lll1ll11l_opy_(self.bstack1111ll1l1l_opy_):
             self.bstack1111ll1lll_opy_ += [
                bstack1111l1l1ll_opy_.get(bstack1l1lll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭န")), str(bstack11ll1l1ll1_opy_.bstack11ll11l111_opy_(self.bstack1111ll1l1l_opy_)),
                bstack1111l1l1ll_opy_.get(bstack1l1lll1_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧပ")), str(bstack1111l1l1ll_opy_.get(bstack1l1lll1_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧဖ")))
            ]
    def bstack1111l1lll1_opy_(self):
        bstack1ll1l11lll_opy_ = []
        for spec in self.bstack11l1l1lll1_opy_:
            bstack11111lll_opy_ = [spec]
            bstack11111lll_opy_ += self.bstack1111ll1lll_opy_
            bstack1ll1l11lll_opy_.append(bstack11111lll_opy_)
        self.bstack1ll1l11lll_opy_ = bstack1ll1l11lll_opy_
        return bstack1ll1l11lll_opy_
    def bstack1lll1l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111ll11ll_opy_ = True
            return True
        except Exception as e:
            self.bstack1111ll11ll_opy_ = False
        return self.bstack1111ll11ll_opy_
    def bstack11l1llllll_opy_(self, logger):
        bstack1l1lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠡࡨ࡯ࡥ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤࡹࡵࡴࡢ࡮ࠣࡲࡺࡳࡢࡦࡴࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨဗ")
        try:
            logger.info(bstack1l1lll1_opy_ (u"ࠦࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢဘ"))
            bstack1111l1llll_opy_ = [bstack1l1lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧမ"), *self.bstack1111ll1lll_opy_, bstack1l1lll1_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢယ")]
            result = subprocess.run(bstack1111l1llll_opy_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                logger.error(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧရ").format(result.stderr))
                return 0
            test_count = result.stdout.count(bstack1l1lll1_opy_ (u"ࠣ࠾ࡉࡹࡳࡩࡴࡪࡱࡱࠤࠧလ"))
            logger.info(bstack1l1lll1_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠽ࠤࢀࢃࠢဝ").format(test_count))
            return test_count
        except Exception as e:
            logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢသ").format(e))
            return 0
    def bstack1ll111l11l_opy_(self, bstack1111ll1l11_opy_, bstack1lll11l1l1_opy_):
        bstack1lll11l1l1_opy_[bstack1l1lll1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫဟ")] = self.bstack1111ll1l1l_opy_
        multiprocessing.set_start_method(bstack1l1lll1_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫဠ"))
        bstack1111l1l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l1ll11_opy_ = manager.list()
        if bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩအ") in self.bstack1111ll1l1l_opy_:
            for index, platform in enumerate(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဢ")]):
                bstack1111l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111ll1l11_opy_,
                                                            args=(self.bstack1111ll1lll_opy_, bstack1lll11l1l1_opy_, bstack1111l1ll11_opy_)))
            bstack1111lll111_opy_ = len(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဣ")])
        else:
            bstack1111l1l1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111ll1l11_opy_,
                                                        args=(self.bstack1111ll1lll_opy_, bstack1lll11l1l1_opy_, bstack1111l1ll11_opy_)))
            bstack1111lll111_opy_ = 1
        i = 0
        for t in bstack1111l1l1l_opy_:
            os.environ[bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩဤ")] = str(i)
            if bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဥ") in self.bstack1111ll1l1l_opy_:
                os.environ[bstack1l1lll1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬဦ")] = json.dumps(self.bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဧ")][i % bstack1111lll111_opy_])
            i += 1
            t.start()
        for t in bstack1111l1l1l_opy_:
            t.join()
        return list(bstack1111l1ll11_opy_)
    @staticmethod
    def bstack1l1l1ll1l_opy_(driver, bstack1111ll11l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1lll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪဨ"), None)
        if item and getattr(item, bstack1l1lll1_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩဩ"), None) and not getattr(item, bstack1l1lll1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪဪ"), False):
            logger.info(
                bstack1l1lll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣါ"))
            bstack1111l1ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111l1ll1l_opy_.bstack1l11ll1lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)