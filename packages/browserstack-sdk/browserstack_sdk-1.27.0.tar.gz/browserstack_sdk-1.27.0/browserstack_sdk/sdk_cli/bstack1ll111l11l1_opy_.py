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
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack11111ll1l1_opy_ import (
    bstack1llllll111l_opy_,
    bstack1llllll1l1l_opy_,
    bstack11111l1l1l_opy_,
    bstack1lllllll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll11l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllllll_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1lllllll111_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1lll1llll1l_opy_
import weakref
class bstack1ll111ll1l1_opy_(bstack1lll1llll1l_opy_):
    bstack1ll111l11ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllllll1ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllllll1ll_opy_]]
    def __init__(self, bstack1ll111l11ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll111l111l_opy_ = dict()
        self.bstack1ll111l11ll_opy_ = bstack1ll111l11ll_opy_
        self.frameworks = frameworks
        bstack1ll1ll1llll_opy_.bstack1ll1l1lll1l_opy_((bstack1llllll111l_opy_.bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_.POST), self.__1ll111ll11l_opy_)
        if any(bstack1lll11l1l11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_(
                (bstack1llllll111l_opy_.bstack111111111l_opy_, bstack1llllll1l1l_opy_.PRE), self.__1ll111ll1ll_opy_
            )
            bstack1lll11l1l11_opy_.bstack1ll1l1lll1l_opy_(
                (bstack1llllll111l_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.__1ll111l1ll1_opy_
            )
    def __1ll111ll11l_opy_(
        self,
        f: bstack1ll1ll1llll_opy_,
        bstack1ll111lll1l_opy_: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1lll1_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣᇌ"):
                return
            contexts = bstack1ll111lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1lll1_opy_ (u"ࠢࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠧᇍ") in page.url:
                                self.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡕࡷࡳࡷ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᇎ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, self.bstack1ll111l11ll_opy_, True)
                                self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡱࡣࡪࡩࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᇏ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠥࠦᇐ"))
        except Exception as e:
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡲࡪࡰࡪࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦ࠺ࠣᇑ"),e)
    def __1ll111ll1ll_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111l1l1l_opy_.bstack1llllllll11_opy_(instance, self.bstack1ll111l11ll_opy_, False):
            return
        if not f.bstack1ll11l1111l_opy_(f.hub_url(driver)):
            self.bstack1ll111l111l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, self.bstack1ll111l11ll_opy_, True)
            self.logger.debug(bstack1l1lll1_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᇒ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠨࠢᇓ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, self.bstack1ll111l11ll_opy_, True)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᇔ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠣࠤᇕ"))
    def __1ll111l1ll1_opy_(
        self,
        f: bstack1lll11l1l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll1ll_opy_, str],
        bstack1llllll1l11_opy_: Tuple[bstack1llllll111l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll111l1l11_opy_(instance)
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᇖ") + str(instance.ref()) + bstack1l1lll1_opy_ (u"ࠥࠦᇗ"))
    def bstack1ll111lll11_opy_(self, context: bstack1lllllll111_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllllll1ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll111l1111_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll11l1l11_opy_.bstack1ll111l1l1l_opy_(data[1])
                    and data[1].bstack1ll111l1111_opy_(context)
                    and getattr(data[0](), bstack1l1lll1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᇘ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111111111_opy_, reverse=reverse)
    def bstack1ll111ll111_opy_(self, context: bstack1lllllll111_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllllll1ll_opy_]]:
        matches = []
        for data in self.bstack1ll111l111l_opy_.values():
            if (
                data[1].bstack1ll111l1111_opy_(context)
                and getattr(data[0](), bstack1l1lll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᇙ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111111111_opy_, reverse=reverse)
    def bstack1ll111l1lll_opy_(self, instance: bstack1lllllll1ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll111l1l11_opy_(self, instance: bstack1lllllll1ll_opy_) -> bool:
        if self.bstack1ll111l1lll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111l1l1l_opy_.bstack1111111lll_opy_(instance, self.bstack1ll111l11ll_opy_, False)
            return True
        return False