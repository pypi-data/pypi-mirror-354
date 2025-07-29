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
from uuid import uuid4
from bstack_utils.helper import bstack11l1ll1lll_opy_, bstack11l11llll1l_opy_
from bstack_utils.bstack1ll111l1l_opy_ import bstack11l1lll1ll1_opy_
class bstack1111llll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack11l1l11l11l_opy_=None, bstack11l1l111ll1_opy_=True, bstack1l111lll11l_opy_=None, bstack11ll1ll11_opy_=None, result=None, duration=None, bstack111ll11ll1_opy_=None, meta={}):
        self.bstack111ll11ll1_opy_ = bstack111ll11ll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11l1l111ll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11l1l11l11l_opy_ = bstack11l1l11l11l_opy_
        self.bstack1l111lll11l_opy_ = bstack1l111lll11l_opy_
        self.bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1l1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1111_opy_(self, meta):
        self.meta = meta
    def bstack111ll1lll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack11l11llll11_opy_(self):
        bstack11l1l1111ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᜂ"): bstack11l1l1111ll_opy_,
            bstack1l1lll1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᜃ"): bstack11l1l1111ll_opy_,
            bstack1l1lll1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᜄ"): bstack11l1l1111ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1lll1_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᜅ") + key)
            setattr(self, key, val)
    def bstack11l1l11l1l1_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᜆ"): self.name,
            bstack1l1lll1_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᜇ"): {
                bstack1l1lll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᜈ"): bstack1l1lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᜉ"),
                bstack1l1lll1_opy_ (u"ࠫࡨࡵࡤࡦࠩᜊ"): self.code
            },
            bstack1l1lll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᜋ"): self.scope,
            bstack1l1lll1_opy_ (u"࠭ࡴࡢࡩࡶࠫᜌ"): self.tags,
            bstack1l1lll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᜍ"): self.framework,
            bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜎ"): self.started_at
        }
    def bstack11l11lll11l_opy_(self):
        return {
         bstack1l1lll1_opy_ (u"ࠩࡰࡩࡹࡧࠧᜏ"): self.meta
        }
    def bstack11l1l1111l1_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᜐ"): {
                bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᜑ"): self.bstack11l1l11l11l_opy_
            }
        }
    def bstack11l11llllll_opy_(self, bstack11l11lllll1_opy_, details):
        step = next(filter(lambda st: st[bstack1l1lll1_opy_ (u"ࠬ࡯ࡤࠨᜒ")] == bstack11l11lllll1_opy_, self.meta[bstack1l1lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᜓ")]), None)
        step.update(details)
    def bstack11l11l1l1_opy_(self, bstack11l11lllll1_opy_):
        step = next(filter(lambda st: st[bstack1l1lll1_opy_ (u"ࠧࡪࡦ᜔ࠪ")] == bstack11l11lllll1_opy_, self.meta[bstack1l1lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹ᜕ࠧ")]), None)
        step.update({
            bstack1l1lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᜖"): bstack11l1ll1lll_opy_()
        })
    def bstack111ll1llll_opy_(self, bstack11l11lllll1_opy_, result, duration=None):
        bstack1l111lll11l_opy_ = bstack11l1ll1lll_opy_()
        if bstack11l11lllll1_opy_ is not None and self.meta.get(bstack1l1lll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᜗")):
            step = next(filter(lambda st: st[bstack1l1lll1_opy_ (u"ࠫ࡮ࡪࠧ᜘")] == bstack11l11lllll1_opy_, self.meta[bstack1l1lll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᜙")]), None)
            step.update({
                bstack1l1lll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᜚"): bstack1l111lll11l_opy_,
                bstack1l1lll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ᜛"): duration if duration else bstack11l11llll1l_opy_(step[bstack1l1lll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᜜")], bstack1l111lll11l_opy_),
                bstack1l1lll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜝"): result.result,
                bstack1l1lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᜞"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack11l1l111lll_opy_):
        if self.meta.get(bstack1l1lll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᜟ")):
            self.meta[bstack1l1lll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᜠ")].append(bstack11l1l111lll_opy_)
        else:
            self.meta[bstack1l1lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᜡ")] = [ bstack11l1l111lll_opy_ ]
    def bstack11l1l11111l_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᜢ"): self.bstack111ll1l1l1_opy_(),
            **self.bstack11l1l11l1l1_opy_(),
            **self.bstack11l11llll11_opy_(),
            **self.bstack11l11lll11l_opy_()
        }
    def bstack11l1l111l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1lll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᜣ"): self.bstack1l111lll11l_opy_,
            bstack1l1lll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᜤ"): self.duration,
            bstack1l1lll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜥ"): self.result.result
        }
        if data[bstack1l1lll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᜦ")] == bstack1l1lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᜧ"):
            data[bstack1l1lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᜨ")] = self.result.bstack1111l111l1_opy_()
            data[bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᜩ")] = [{bstack1l1lll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᜪ"): self.result.bstack11l1l111l11_opy_()}]
        return data
    def bstack11l1l11l111_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜫ"): self.bstack111ll1l1l1_opy_(),
            **self.bstack11l1l11l1l1_opy_(),
            **self.bstack11l11llll11_opy_(),
            **self.bstack11l1l111l1l_opy_(),
            **self.bstack11l11lll11l_opy_()
        }
    def bstack111l1lllll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1lll1_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᜬ") in event:
            return self.bstack11l1l11111l_opy_()
        elif bstack1l1lll1_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᜭ") in event:
            return self.bstack11l1l11l111_opy_()
    def bstack111l1l1l11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lll11l_opy_ = time if time else bstack11l1ll1lll_opy_()
        self.duration = duration if duration else bstack11l11llll1l_opy_(self.started_at, self.bstack1l111lll11l_opy_)
        if result:
            self.result = result
class bstack111lllll1l_opy_(bstack1111llll1l_opy_):
    def __init__(self, hooks=[], bstack11l111111l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack11ll1ll11_opy_=bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࠪᜮ"))
    @classmethod
    def bstack11l1l11l1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1lll1_opy_ (u"࠭ࡩࡥࠩᜯ"): id(step),
                bstack1l1lll1_opy_ (u"ࠧࡵࡧࡻࡸࠬᜰ"): step.name,
                bstack1l1lll1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᜱ"): step.keyword,
            })
        return bstack111lllll1l_opy_(
            **kwargs,
            meta={
                bstack1l1lll1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᜲ"): {
                    bstack1l1lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᜳ"): feature.name,
                    bstack1l1lll1_opy_ (u"ࠫࡵࡧࡴࡩ᜴ࠩ"): feature.filename,
                    bstack1l1lll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᜵"): feature.description
                },
                bstack1l1lll1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ᜶"): {
                    bstack1l1lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᜷"): scenario.name
                },
                bstack1l1lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᜸"): steps,
                bstack1l1lll1_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ᜹"): bstack11l1lll1ll1_opy_(test)
            }
        )
    def bstack11l11lll1ll_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᜺"): self.hooks
        }
    def bstack11l11lll1l1_opy_(self):
        if self.bstack11l111111l_opy_:
            return {
                bstack1l1lll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ᜻"): self.bstack11l111111l_opy_
            }
        return {}
    def bstack11l1l11l111_opy_(self):
        return {
            **super().bstack11l1l11l111_opy_(),
            **self.bstack11l11lll1ll_opy_()
        }
    def bstack11l1l11111l_opy_(self):
        return {
            **super().bstack11l1l11111l_opy_(),
            **self.bstack11l11lll1l1_opy_()
        }
    def bstack111l1l1l11_opy_(self):
        return bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ᜼")
class bstack111ll1ll1l_opy_(bstack1111llll1l_opy_):
    def __init__(self, hook_type, *args,bstack11l111111l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack11l11lll111_opy_ = None
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack11ll1ll11_opy_=bstack1l1lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᜽"))
    def bstack111l1l1lll_opy_(self):
        return self.hook_type
    def bstack11l1l111111_opy_(self):
        return {
            bstack1l1lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ᜾"): self.hook_type
        }
    def bstack11l1l11l111_opy_(self):
        return {
            **super().bstack11l1l11l111_opy_(),
            **self.bstack11l1l111111_opy_()
        }
    def bstack11l1l11111l_opy_(self):
        return {
            **super().bstack11l1l11111l_opy_(),
            bstack1l1lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭᜿"): self.bstack11l11lll111_opy_,
            **self.bstack11l1l111111_opy_()
        }
    def bstack111l1l1l11_opy_(self):
        return bstack1l1lll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᝀ")
    def bstack111lll1ll1_opy_(self, bstack11l11lll111_opy_):
        self.bstack11l11lll111_opy_ = bstack11l11lll111_opy_