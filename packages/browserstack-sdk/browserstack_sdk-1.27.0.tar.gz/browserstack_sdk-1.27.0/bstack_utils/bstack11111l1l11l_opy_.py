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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111lllll1l_opy_
from browserstack_sdk.bstack11111l1l1_opy_ import bstack1l111111ll_opy_
def _11111l1l111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11111l1llll_opy_:
    def __init__(self, handler):
        self._11111l1l1ll_opy_ = {}
        self._11111ll111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l111111ll_opy_.version()
        if bstack1111lllll1l_opy_(pytest_version, bstack1l1lll1_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᾺ")) >= 0:
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ά")] = Module._register_setup_function_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᾼ")] = Module._register_setup_module_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᾽")] = Class._register_setup_class_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧι")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᾿"))
            Module._register_setup_module_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ῀"))
            Class._register_setup_class_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ῁"))
            Class._register_setup_method_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫῂ"))
        else:
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧῃ")] = Module._inject_setup_function_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ῄ")] = Module._inject_setup_module_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭῅")] = Class._inject_setup_class_fixture
            self._11111l1l1ll_opy_[bstack1l1lll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨῆ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫῇ"))
            Module._inject_setup_module_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪῈ"))
            Class._inject_setup_class_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪΈ"))
            Class._inject_setup_method_fixture = self.bstack11111l1l1l1_opy_(bstack1l1lll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬῊ"))
    def bstack11111ll1111_opy_(self, bstack11111l1lll1_opy_, hook_type):
        bstack11111l1ll11_opy_ = id(bstack11111l1lll1_opy_.__class__)
        if (bstack11111l1ll11_opy_, hook_type) in self._11111ll111l_opy_:
            return
        meth = getattr(bstack11111l1lll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11111ll111l_opy_[(bstack11111l1ll11_opy_, hook_type)] = meth
            setattr(bstack11111l1lll1_opy_, hook_type, self.bstack11111ll1lll_opy_(hook_type, bstack11111l1ll11_opy_))
    def bstack11111ll11l1_opy_(self, instance, bstack11111ll1ll1_opy_):
        if bstack11111ll1ll1_opy_ == bstack1l1lll1_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣΉ"):
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢῌ"))
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦ῍"))
        if bstack11111ll1ll1_opy_ == bstack1l1lll1_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ῎"):
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣ῏"))
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧῐ"))
        if bstack11111ll1ll1_opy_ == bstack1l1lll1_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦῑ"):
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥῒ"))
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢΐ"))
        if bstack11111ll1ll1_opy_ == bstack1l1lll1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ῔"):
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢ῕"))
            self.bstack11111ll1111_opy_(instance.obj, bstack1l1lll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦῖ"))
    @staticmethod
    def bstack11111ll11ll_opy_(hook_type, func, args):
        if hook_type in [bstack1l1lll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩῗ"), bstack1l1lll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ῐ")]:
            _11111l1l111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111ll1lll_opy_(self, hook_type, bstack11111l1ll11_opy_):
        def bstack11111l1ll1l_opy_(arg=None):
            self.handler(hook_type, bstack1l1lll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬῙ"))
            result = None
            try:
                bstack1111111l1l_opy_ = self._11111ll111l_opy_[(bstack11111l1ll11_opy_, hook_type)]
                self.bstack11111ll11ll_opy_(hook_type, bstack1111111l1l_opy_, (arg,))
                result = Result(result=bstack1l1lll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ὶ"))
            except Exception as e:
                result = Result(result=bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧΊ"), exception=e)
                self.handler(hook_type, bstack1l1lll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ῜"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1lll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ῝"), result)
        def bstack11111ll1l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1lll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ῞"))
            result = None
            exception = None
            try:
                self.bstack11111ll11ll_opy_(hook_type, self._11111ll111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ῟"))
            except Exception as e:
                result = Result(result=bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬῠ"), exception=e)
                self.handler(hook_type, bstack1l1lll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬῡ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1lll1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ῢ"), result)
        if hook_type in [bstack1l1lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧΰ"), bstack1l1lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫῤ")]:
            return bstack11111ll1l1l_opy_
        return bstack11111l1ll1l_opy_
    def bstack11111l1l1l1_opy_(self, bstack11111ll1ll1_opy_):
        def bstack11111ll1l11_opy_(this, *args, **kwargs):
            self.bstack11111ll11l1_opy_(this, bstack11111ll1ll1_opy_)
            self._11111l1l1ll_opy_[bstack11111ll1ll1_opy_](this, *args, **kwargs)
        return bstack11111ll1l11_opy_