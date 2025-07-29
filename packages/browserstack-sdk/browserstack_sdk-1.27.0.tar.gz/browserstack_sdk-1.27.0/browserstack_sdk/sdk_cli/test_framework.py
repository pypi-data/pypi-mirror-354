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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l11111_opy_ import bstack11111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1lllll1lll1_opy_, bstack1lllllll111_opy_
class bstack1lll11lllll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1lll1_opy_ (u"ࠥࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᔭ").format(self.name)
class bstack1ll1ll1lll1_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1lll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᔮ").format(self.name)
class bstack1llll1lll11_opy_(bstack1lllll1lll1_opy_):
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l11l1l111l_opy_: Dict[str, str]
    state: bstack1ll1ll1lll1_opy_
    bstack1111111111_opy_: datetime
    bstack11111l11ll_opy_: datetime
    def __init__(
        self,
        context: bstack1lllllll111_opy_,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l11l1l111l_opy_: Dict[str, str],
        state=bstack1ll1ll1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l11l1l111l_opy_ = bstack1l11l1l111l_opy_
        self.state = state
        self.bstack1111111111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111l11ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111lll_opy_(self, bstack11111111ll_opy_: bstack1ll1ll1lll1_opy_):
        bstack1lllllllll1_opy_ = bstack1ll1ll1lll1_opy_(bstack11111111ll_opy_).name
        if not bstack1lllllllll1_opy_:
            return False
        if bstack11111111ll_opy_ == self.state:
            return False
        self.state = bstack11111111ll_opy_
        self.bstack11111l11ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l11ll1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l11ll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1lllll_opy_: int = None
    bstack1l1lll11111_opy_: str = None
    bstack1l1111l_opy_: str = None
    bstack11lll1llll_opy_: str = None
    bstack1l1lllll1ll_opy_: str = None
    bstack1l11l1l11ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l11l11l_opy_ = bstack1l1lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣᔯ")
    bstack1l1111ll11l_opy_ = bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢᔰ")
    bstack1ll11l1llll_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠥᔱ")
    bstack1l11l111ll1_opy_ = bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠤᔲ")
    bstack1l111ll11l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡵࡣࡪࡷࠧᔳ")
    bstack1l1l1l1l11l_opy_ = bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࠣᔴ")
    bstack1l1lll111ll_opy_ = bstack1l1lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࡡࡤࡸࠧᔵ")
    bstack1l1llll111l_opy_ = bstack1l1lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔶ")
    bstack1l1lll11lll_opy_ = bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᔷ")
    bstack1l11l1lll11_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᔸ")
    bstack1ll11llllll_opy_ = bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠢᔹ")
    bstack1l1ll1ll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠦᔺ")
    bstack1l11l111l11_opy_ = bstack1l1lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡥࡲࡨࡪࠨᔻ")
    bstack1l1ll111l11_opy_ = bstack1l1lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪࠨᔼ")
    bstack1ll1l1lllll_opy_ = bstack1l1lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᔽ")
    bstack1l1l1l1l111_opy_ = bstack1l1lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠧᔾ")
    bstack1l11l11l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠦᔿ")
    bstack1l111l1l1ll_opy_ = bstack1l1lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡩࡶࠦᕀ")
    bstack1l111l11l1l_opy_ = bstack1l1lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡮ࡧࡷࡥࠧᕁ")
    bstack1l1111l11l1_opy_ = bstack1l1lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡵࡦࡳࡵ࡫ࡳࠨᕂ")
    bstack1l11lll1ll1_opy_ = bstack1l1lll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᕃ")
    bstack1l111l11l11_opy_ = bstack1l1lll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᕄ")
    bstack1l111llll11_opy_ = bstack1l1lll1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᕅ")
    bstack1l111ll111l_opy_ = bstack1l1lll1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤ࡯ࡤࠣᕆ")
    bstack1l11l1l1l11_opy_ = bstack1l1lll1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡦࡵࡸࡰࡹࠨᕇ")
    bstack1l11l11llll_opy_ = bstack1l1lll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡭ࡱࡪࡷࠧᕈ")
    bstack1l1111ll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪࠨᕉ")
    bstack1l111l1111l_opy_ = bstack1l1lll1_opy_ (u"ࠦࡱࡵࡧࡴࠤᕊ")
    bstack1l11l1lll1l_opy_ = bstack1l1lll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᕋ")
    bstack1l11l1llll1_opy_ = bstack1l1lll1_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᕌ")
    bstack1l111ll11ll_opy_ = bstack1l1lll1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᕍ")
    bstack1l1llll11ll_opy_ = bstack1l1lll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠥᕎ")
    bstack1l1lll1l1l1_opy_ = bstack1l1lll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡍࡑࡊࠦᕏ")
    bstack1l1lll11ll1_opy_ = bstack1l1lll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᕐ")
    bstack1lllllll11l_opy_: Dict[str, bstack1llll1lll11_opy_] = dict()
    bstack1l11111lll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1l1111_opy_: List[str]
    bstack1l11l1l111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1l1111_opy_: List[str],
        bstack1l11l1l111l_opy_: Dict[str, str],
        bstack1111l11111_opy_: bstack11111lll11_opy_
    ):
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_
        self.bstack1l11l1l111l_opy_ = bstack1l11l1l111l_opy_
        self.bstack1111l11111_opy_ = bstack1111l11111_opy_
    def track_event(
        self,
        context: bstack1l111l11ll1_opy_,
        test_framework_state: bstack1ll1ll1lll1_opy_,
        test_hook_state: bstack1lll11lllll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁࡽࠣᕑ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111ll1111_opy_(
        self,
        instance: bstack1llll1lll11_opy_,
        bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11ll11lll_opy_ = TestFramework.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        if not bstack1l11ll11lll_opy_ in TestFramework.bstack1l11111lll1_opy_:
            return
        self.logger.debug(bstack1l1lll1_opy_ (u"ࠧ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠨᕒ").format(len(TestFramework.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_])))
        for callback in TestFramework.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_]:
            try:
                callback(self, instance, bstack1llllll1l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂࠨᕓ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll1llll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1llllll1l_opy_(self, instance, bstack1llllll1l11_opy_):
        return
    @abc.abstractmethod
    def bstack1ll1111111l_opy_(self, instance, bstack1llllll1l11_opy_):
        return
    @staticmethod
    def bstack111111l11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lllll1lll1_opy_.create_context(target)
        instance = TestFramework.bstack1lllllll11l_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llllll11_opy_(reverse=True) -> List[bstack1llll1lll11_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllllll11l_opy_.values(),
            ),
            key=lambda t: t.bstack1111111111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllllll1l1_opy_(ctx: bstack1lllllll111_opy_, reverse=True) -> List[bstack1llll1lll11_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllllll11l_opy_.values(),
            ),
            key=lambda t: t.bstack1111111111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll11l_opy_(instance: bstack1llll1lll11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllllll11_opy_(instance: bstack1llll1lll11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111lll_opy_(instance: bstack1llll1lll11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1lll1_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᕔ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1ll11_opy_(instance: bstack1llll1lll11_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1lll1_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡴࡴࡳ࡫ࡨࡷࡂࢁࡽࠣᕕ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l111111l11_opy_(instance: bstack1ll1ll1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1lll1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᕖ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack111111l11l_opy_(target, strict)
        return TestFramework.bstack1llllllll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack111111l11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l11l111_opy_(instance: bstack1llll1lll11_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l11lll1_opy_(instance: bstack1llll1lll11_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_]):
        return bstack1l1lll1_opy_ (u"ࠥ࠾ࠧᕗ").join((bstack1ll1ll1lll1_opy_(bstack1llllll1l11_opy_[0]).name, bstack1lll11lllll_opy_(bstack1llllll1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1l1lll1l_opy_(bstack1llllll1l11_opy_: Tuple[bstack1ll1ll1lll1_opy_, bstack1lll11lllll_opy_], callback: Callable):
        bstack1l11ll11lll_opy_ = TestFramework.bstack1l11ll1lll1_opy_(bstack1llllll1l11_opy_)
        TestFramework.logger.debug(bstack1l1lll1_opy_ (u"ࠦࡸ࡫ࡴࡠࡪࡲࡳࡰࡥࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢ࡫ࡳࡴࡱ࡟ࡳࡧࡪ࡭ࡸࡺࡲࡺࡡ࡮ࡩࡾࡃࡻࡾࠤᕘ").format(bstack1l11ll11lll_opy_))
        if not bstack1l11ll11lll_opy_ in TestFramework.bstack1l11111lll1_opy_:
            TestFramework.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_] = []
        TestFramework.bstack1l11111lll1_opy_[bstack1l11ll11lll_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1l1lll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡷ࡭ࡳࡹࠢᕙ"):
            return klass.__qualname__
        return module + bstack1l1lll1_opy_ (u"ࠨ࠮ࠣᕚ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll11ll1l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}