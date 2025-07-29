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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111l1l1l1l1_opy_, bstack11l111l111_opy_, bstack1l1ll111l_opy_, bstack1l1l1l11l_opy_,
                                    bstack111l1ll11l1_opy_, bstack111l1l1l1ll_opy_, bstack111l1lllll1_opy_, bstack111l1l1l11l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1l1llll_opy_, bstack1l1111l11l_opy_
from bstack_utils.proxy import bstack1l11ll11l_opy_, bstack1l111ll111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l111111l_opy_
from browserstack_sdk._version import __version__
bstack111l111l1_opy_ = Config.bstack1ll1l1l11_opy_()
logger = bstack1l111111l_opy_.get_logger(__name__, bstack1l111111l_opy_.bstack1lllll11111_opy_())
def bstack11l111ll11l_opy_(config):
    return config[bstack1l1lll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᶄ")]
def bstack11l111ll111_opy_(config):
    return config[bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᶅ")]
def bstack11l1lll11l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111l1l11ll_opy_(obj):
    values = []
    bstack1111ll111ll_opy_ = re.compile(bstack1l1lll1_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᶆ"), re.I)
    for key in obj.keys():
        if bstack1111ll111ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1111ll11_opy_(config):
    tags = []
    tags.extend(bstack1111l1l11ll_opy_(os.environ))
    tags.extend(bstack1111l1l11ll_opy_(config))
    return tags
def bstack1111ll11l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111ll1l1ll_opy_(bstack1111l111111_opy_):
    if not bstack1111l111111_opy_:
        return bstack1l1lll1_opy_ (u"࠭ࠧᶇ")
    return bstack1l1lll1_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᶈ").format(bstack1111l111111_opy_.name, bstack1111l111111_opy_.email)
def bstack11l1111ll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l111l11l_opy_ = repo.common_dir
        info = {
            bstack1l1lll1_opy_ (u"ࠣࡵ࡫ࡥࠧᶉ"): repo.head.commit.hexsha,
            bstack1l1lll1_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᶊ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1lll1_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᶋ"): repo.active_branch.name,
            bstack1l1lll1_opy_ (u"ࠦࡹࡧࡧࠣᶌ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᶍ"): bstack1111ll1l1ll_opy_(repo.head.commit.committer),
            bstack1l1lll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᶎ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1lll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᶏ"): bstack1111ll1l1ll_opy_(repo.head.commit.author),
            bstack1l1lll1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᶐ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1lll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᶑ"): repo.head.commit.message,
            bstack1l1lll1_opy_ (u"ࠥࡶࡴࡵࡴࠣᶒ"): repo.git.rev_parse(bstack1l1lll1_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᶓ")),
            bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᶔ"): bstack111l111l11l_opy_,
            bstack1l1lll1_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᶕ"): subprocess.check_output([bstack1l1lll1_opy_ (u"ࠢࡨ࡫ࡷࠦᶖ"), bstack1l1lll1_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᶗ"), bstack1l1lll1_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᶘ")]).strip().decode(
                bstack1l1lll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᶙ")),
            bstack1l1lll1_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᶚ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1lll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᶛ"): repo.git.rev_list(
                bstack1l1lll1_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᶜ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111llll11l_opy_ = []
        for remote in remotes:
            bstack1111ll11ll1_opy_ = {
                bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᶝ"): remote.name,
                bstack1l1lll1_opy_ (u"ࠣࡷࡵࡰࠧᶞ"): remote.url,
            }
            bstack1111llll11l_opy_.append(bstack1111ll11ll1_opy_)
        bstack1111l1l1l1l_opy_ = {
            bstack1l1lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶟ"): bstack1l1lll1_opy_ (u"ࠥ࡫࡮ࡺࠢᶠ"),
            **info,
            bstack1l1lll1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᶡ"): bstack1111llll11l_opy_
        }
        bstack1111l1l1l1l_opy_ = bstack1111l11ll1l_opy_(bstack1111l1l1l1l_opy_)
        return bstack1111l1l1l1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᶢ").format(err))
        return {}
def bstack1111l11ll1l_opy_(bstack1111l1l1l1l_opy_):
    bstack111l11111l1_opy_ = bstack1111ll11l11_opy_(bstack1111l1l1l1l_opy_)
    if bstack111l11111l1_opy_ and bstack111l11111l1_opy_ > bstack111l1ll11l1_opy_:
        bstack1111llll1l1_opy_ = bstack111l11111l1_opy_ - bstack111l1ll11l1_opy_
        bstack1111lll11l1_opy_ = bstack111l1111111_opy_(bstack1111l1l1l1l_opy_[bstack1l1lll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᶣ")], bstack1111llll1l1_opy_)
        bstack1111l1l1l1l_opy_[bstack1l1lll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᶤ")] = bstack1111lll11l1_opy_
        logger.info(bstack1l1lll1_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥᶥ")
                    .format(bstack1111ll11l11_opy_(bstack1111l1l1l1l_opy_) / 1024))
    return bstack1111l1l1l1l_opy_
def bstack1111ll11l11_opy_(bstack1l1llllll1_opy_):
    try:
        if bstack1l1llllll1_opy_:
            bstack1111l11l111_opy_ = json.dumps(bstack1l1llllll1_opy_)
            bstack1111l11l11l_opy_ = sys.getsizeof(bstack1111l11l111_opy_)
            return bstack1111l11l11l_opy_
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤᶦ").format(e))
    return -1
def bstack111l1111111_opy_(field, bstack1111lllll11_opy_):
    try:
        bstack111l111ll11_opy_ = len(bytes(bstack111l1l1l1ll_opy_, bstack1l1lll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᶧ")))
        bstack111l111l111_opy_ = bytes(field, bstack1l1lll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᶨ"))
        bstack111l1111l11_opy_ = len(bstack111l111l111_opy_)
        bstack1111l111l1l_opy_ = ceil(bstack111l1111l11_opy_ - bstack1111lllll11_opy_ - bstack111l111ll11_opy_)
        if bstack1111l111l1l_opy_ > 0:
            bstack1111l1l1lll_opy_ = bstack111l111l111_opy_[:bstack1111l111l1l_opy_].decode(bstack1l1lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᶩ"), errors=bstack1l1lll1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ᶪ")) + bstack111l1l1l1ll_opy_
            return bstack1111l1l1lll_opy_
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧᶫ").format(e))
    return field
def bstack1111ll11_opy_():
    env = os.environ
    if (bstack1l1lll1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᶬ") in env and len(env[bstack1l1lll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᶭ")]) > 0) or (
            bstack1l1lll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᶮ") in env and len(env[bstack1l1lll1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥᶯ")]) > 0):
        return {
            bstack1l1lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᶰ"): bstack1l1lll1_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢᶱ"),
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᶲ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᶳ")),
            bstack1l1lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶴ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᶵ")),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶶ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᶷ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠨࡃࡊࠤᶸ")) == bstack1l1lll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᶹ") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥᶺ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶻ"): bstack1l1lll1_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧᶼ"),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᶽ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᶾ")),
            bstack1l1lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᶿ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᷀")),
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᷁"): env.get(bstack1l1lll1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑ᷂ࠧ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠥࡇࡎࠨ᷃")) == bstack1l1lll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ᷄") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ᷅"))):
        return {
            bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᷆"): bstack1l1lll1_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ᷇"),
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᷈"): env.get(bstack1l1lll1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ᷉")),
            bstack1l1lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩ᷊ࠧ"): env.get(bstack1l1lll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᷋")),
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᷌"): env.get(bstack1l1lll1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᷍"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡋ᷎ࠥ")) == bstack1l1lll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᷏") and env.get(bstack1l1lll1_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇ᷐ࠥ")) == bstack1l1lll1_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ᷑"):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᷒"): bstack1l1lll1_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢᷓ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᷔ"): None,
            bstack1l1lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᷕ"): None,
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᷖ"): None
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧᷗ")) and env.get(bstack1l1lll1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᷘ")):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᷙ"): bstack1l1lll1_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣᷚ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᷛ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧᷜ")),
            bstack1l1lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᷝ"): None,
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᷞ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᷟ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡏࠢᷠ")) == bstack1l1lll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᷡ") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᷢ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᷣ"): bstack1l1lll1_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢᷤ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᷥ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᷦ")),
            bstack1l1lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᷧ"): None,
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᷨ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᷩ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡋࠥᷪ")) == bstack1l1lll1_opy_ (u"ࠣࡶࡵࡹࡪࠨᷫ") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᷬ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᷭ"): bstack1l1lll1_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᷮ"),
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᷯ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧᷰ")),
            bstack1l1lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᷱ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᷲ")),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᷳ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᷴ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡏࠢ᷵")) == bstack1l1lll1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᷶") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ᷷"))):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩ᷸ࠧ"): bstack1l1lll1_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢ᷹ࠣ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰ᷺ࠧ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ᷻")),
            bstack1l1lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᷼"): env.get(bstack1l1lll1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇ᷽ࠥ")),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᷾"): env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆ᷿ࠥ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠣࡅࡌࠦḀ")) == bstack1l1lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢḁ") and bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨḂ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤḃ"): bstack1l1lll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣḄ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤḅ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨḆ")),
            bstack1l1lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥḇ"): env.get(bstack1l1lll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦḈ")) or env.get(bstack1l1lll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨḉ")),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥḊ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢḋ"))
        }
    if bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣḌ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧḍ"): bstack1l1lll1_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣḎ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧḏ"): bstack1l1lll1_opy_ (u"ࠥࡿࢂࢁࡽࠣḐ").format(env.get(bstack1l1lll1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧḑ")), env.get(bstack1l1lll1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬḒ"))),
            bstack1l1lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣḓ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨḔ")),
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢḕ"): env.get(bstack1l1lll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤḖ"))
        }
    if bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧḗ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤḘ"): bstack1l1lll1_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢḙ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤḚ"): bstack1l1lll1_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨḛ").format(env.get(bstack1l1lll1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧḜ")), env.get(bstack1l1lll1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪḝ")), env.get(bstack1l1lll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫḞ")), env.get(bstack1l1lll1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨḟ"))),
            bstack1l1lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢḠ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥḡ")),
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨḢ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤḣ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥḤ")) and env.get(bstack1l1lll1_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧḥ")):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤḦ"): bstack1l1lll1_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢḧ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤḨ"): bstack1l1lll1_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥḩ").format(env.get(bstack1l1lll1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫḪ")), env.get(bstack1l1lll1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧḫ")), env.get(bstack1l1lll1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪḬ"))),
            bstack1l1lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨḭ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧḮ")),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧḯ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢḰ"))
        }
    if any([env.get(bstack1l1lll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨḱ")), env.get(bstack1l1lll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣḲ")), env.get(bstack1l1lll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢḳ"))]):
        return {
            bstack1l1lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤḴ"): bstack1l1lll1_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧḵ"),
            bstack1l1lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤḶ"): env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨḷ")),
            bstack1l1lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥḸ"): env.get(bstack1l1lll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢḹ")),
            bstack1l1lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤḺ"): env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤḻ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥḼ")):
        return {
            bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦḽ"): bstack1l1lll1_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢḾ"),
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦḿ"): env.get(bstack1l1lll1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦṀ")),
            bstack1l1lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧṁ"): env.get(bstack1l1lll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥṂ")),
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦṃ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦṄ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣṅ")) or env.get(bstack1l1lll1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥṆ")):
        return {
            bstack1l1lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢṇ"): bstack1l1lll1_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦṈ"),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢṉ"): env.get(bstack1l1lll1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤṊ")),
            bstack1l1lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣṋ"): bstack1l1lll1_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢṌ") if env.get(bstack1l1lll1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥṍ")) else None,
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣṎ"): env.get(bstack1l1lll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣṏ"))
        }
    if any([env.get(bstack1l1lll1_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤṐ")), env.get(bstack1l1lll1_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨṑ")), env.get(bstack1l1lll1_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨṒ"))]):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧṓ"): bstack1l1lll1_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢṔ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧṕ"): None,
            bstack1l1lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧṖ"): env.get(bstack1l1lll1_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣṗ")),
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦṘ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣṙ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥṚ")):
        return {
            bstack1l1lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨṛ"): bstack1l1lll1_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧṜ"),
            bstack1l1lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨṝ"): env.get(bstack1l1lll1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥṞ")),
            bstack1l1lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢṟ"): bstack1l1lll1_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢṠ").format(env.get(bstack1l1lll1_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪṡ"))) if env.get(bstack1l1lll1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦṢ")) else None,
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣṣ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧṤ"))
        }
    if bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧṥ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥṦ"): bstack1l1lll1_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢṧ"),
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥṨ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧṩ")),
            bstack1l1lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦṪ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨṫ")),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥṬ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢṭ"))
        }
    if bstack11l11l111_opy_(env.get(bstack1l1lll1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢṮ"))):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧṯ"): bstack1l1lll1_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤṰ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧṱ"): bstack1l1lll1_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦṲ").format(env.get(bstack1l1lll1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨṳ")), env.get(bstack1l1lll1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩṴ")), env.get(bstack1l1lll1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ṵ"))),
            bstack1l1lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤṶ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥṷ")),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣṸ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥṹ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡏࠢṺ")) == bstack1l1lll1_opy_ (u"ࠧࡺࡲࡶࡧࠥṻ") and env.get(bstack1l1lll1_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨṼ")) == bstack1l1lll1_opy_ (u"ࠢ࠲ࠤṽ"):
        return {
            bstack1l1lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨṾ"): bstack1l1lll1_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤṿ"),
            bstack1l1lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨẀ"): bstack1l1lll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢẁ").format(env.get(bstack1l1lll1_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩẂ"))),
            bstack1l1lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣẃ"): None,
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨẄ"): None,
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦẅ")):
        return {
            bstack1l1lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢẆ"): bstack1l1lll1_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧẇ"),
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢẈ"): None,
            bstack1l1lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢẉ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢẊ")),
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨẋ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢẌ"))
        }
    if any([env.get(bstack1l1lll1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧẍ")), env.get(bstack1l1lll1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥẎ")), env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤẏ")), env.get(bstack1l1lll1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨẐ"))]):
        return {
            bstack1l1lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦẑ"): bstack1l1lll1_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥẒ"),
            bstack1l1lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦẓ"): None,
            bstack1l1lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦẔ"): env.get(bstack1l1lll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦẕ")) or None,
            bstack1l1lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥẖ"): env.get(bstack1l1lll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢẗ"), 0)
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦẘ")):
        return {
            bstack1l1lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧẙ"): bstack1l1lll1_opy_ (u"ࠣࡉࡲࡇࡉࠨẚ"),
            bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧẛ"): None,
            bstack1l1lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧẜ"): env.get(bstack1l1lll1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤẝ")),
            bstack1l1lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦẞ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧẟ"))
        }
    if env.get(bstack1l1lll1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧẠ")):
        return {
            bstack1l1lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨạ"): bstack1l1lll1_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧẢ"),
            bstack1l1lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨả"): env.get(bstack1l1lll1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥẤ")),
            bstack1l1lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢấ"): env.get(bstack1l1lll1_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤẦ")),
            bstack1l1lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨầ"): env.get(bstack1l1lll1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨẨ"))
        }
    return {bstack1l1lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣẩ"): None}
def get_host_info():
    return {
        bstack1l1lll1_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧẪ"): platform.node(),
        bstack1l1lll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨẫ"): platform.system(),
        bstack1l1lll1_opy_ (u"ࠧࡺࡹࡱࡧࠥẬ"): platform.machine(),
        bstack1l1lll1_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢậ"): platform.version(),
        bstack1l1lll1_opy_ (u"ࠢࡢࡴࡦ࡬ࠧẮ"): platform.architecture()[0]
    }
def bstack1ll11llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11l111ll_opy_():
    if bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩắ")):
        return bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨẰ")
    return bstack1l1lll1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩằ")
def bstack11l11l111l1_opy_(driver):
    info = {
        bstack1l1lll1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪẲ"): driver.capabilities,
        bstack1l1lll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩẳ"): driver.session_id,
        bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧẴ"): driver.capabilities.get(bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬẵ"), None),
        bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪẶ"): driver.capabilities.get(bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪặ"), None),
        bstack1l1lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬẸ"): driver.capabilities.get(bstack1l1lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪẹ"), None),
        bstack1l1lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨẺ"):driver.capabilities.get(bstack1l1lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨẻ"), None),
    }
    if bstack11l11l111ll_opy_() == bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ẽ"):
        if bstack11ll111ll_opy_():
            info[bstack1l1lll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩẽ")] = bstack1l1lll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨẾ")
        elif driver.capabilities.get(bstack1l1lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫế"), {}).get(bstack1l1lll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨỀ"), False):
            info[bstack1l1lll1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ề")] = bstack1l1lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪỂ")
        else:
            info[bstack1l1lll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨể")] = bstack1l1lll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪỄ")
    return info
def bstack11ll111ll_opy_():
    if bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨễ")):
        return True
    if bstack11l11l111_opy_(os.environ.get(bstack1l1lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫỆ"), None)):
        return True
    return False
def bstack1lll1l1ll1_opy_(bstack1111ll1llll_opy_, url, data, config):
    headers = config.get(bstack1l1lll1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬệ"), None)
    proxies = bstack1l11ll11l_opy_(config, url)
    auth = config.get(bstack1l1lll1_opy_ (u"ࠬࡧࡵࡵࡪࠪỈ"), None)
    response = requests.request(
            bstack1111ll1llll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1llll1ll1_opy_(bstack1llll1ll1l_opy_, size):
    bstack1l11lll11l_opy_ = []
    while len(bstack1llll1ll1l_opy_) > size:
        bstack1ll1lll1ll_opy_ = bstack1llll1ll1l_opy_[:size]
        bstack1l11lll11l_opy_.append(bstack1ll1lll1ll_opy_)
        bstack1llll1ll1l_opy_ = bstack1llll1ll1l_opy_[size:]
    bstack1l11lll11l_opy_.append(bstack1llll1ll1l_opy_)
    return bstack1l11lll11l_opy_
def bstack11l11l1111l_opy_(message, bstack1111l111ll1_opy_=False):
    os.write(1, bytes(message, bstack1l1lll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬỉ")))
    os.write(1, bytes(bstack1l1lll1_opy_ (u"ࠧ࡝ࡰࠪỊ"), bstack1l1lll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧị")))
    if bstack1111l111ll1_opy_:
        with open(bstack1l1lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨỌ") + os.environ[bstack1l1lll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩọ")] + bstack1l1lll1_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩỎ"), bstack1l1lll1_opy_ (u"ࠬࡧࠧỏ")) as f:
            f.write(message + bstack1l1lll1_opy_ (u"࠭࡜࡯ࠩỐ"))
def bstack1l1llll1111_opy_():
    return os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪố")].lower() == bstack1l1lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ồ")
def bstack1llllll111_opy_(bstack11ll1l11lll_opy_):
    return bstack1l1lll1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨồ").format(bstack111l1l1l1l1_opy_, bstack11ll1l11lll_opy_)
def bstack11l1ll1lll_opy_():
    return bstack111l1l11ll_opy_().replace(tzinfo=None).isoformat() + bstack1l1lll1_opy_ (u"ࠪ࡞ࠬỔ")
def bstack11l11llll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1lll1_opy_ (u"ࠫ࡟࠭ổ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1lll1_opy_ (u"ࠬࡠࠧỖ")))).total_seconds() * 1000
def bstack1111lll1111_opy_(timestamp):
    return bstack111l111l1l1_opy_(timestamp).isoformat() + bstack1l1lll1_opy_ (u"࡚࠭ࠨỗ")
def bstack1111l1lllll_opy_(bstack1111llll111_opy_):
    date_format = bstack1l1lll1_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬỘ")
    bstack1111ll1111l_opy_ = datetime.datetime.strptime(bstack1111llll111_opy_, date_format)
    return bstack1111ll1111l_opy_.isoformat() + bstack1l1lll1_opy_ (u"ࠨ࡜ࠪộ")
def bstack1111l1l1ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩỚ")
    else:
        return bstack1l1lll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪớ")
def bstack11l11l111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩỜ")
def bstack1111l11lll1_opy_(val):
    return val.__str__().lower() == bstack1l1lll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫờ")
def bstack111ll111l1_opy_(bstack11l11l11ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11l11ll1_opy_ as e:
                print(bstack1l1lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨỞ").format(func.__name__, bstack11l11l11ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l111l1ll_opy_(bstack111l1111lll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1111lll_opy_(cls, *args, **kwargs)
            except bstack11l11l11ll1_opy_ as e:
                print(bstack1l1lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢở").format(bstack111l1111lll_opy_.__name__, bstack11l11l11ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l111l1ll_opy_
    else:
        return decorator
def bstack11ll1llll_opy_(bstack1111ll1l1l_opy_):
    if os.getenv(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫỠ")) is not None:
        return bstack11l11l111_opy_(os.getenv(bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬỡ")))
    if bstack1l1lll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧỢ") in bstack1111ll1l1l_opy_ and bstack1111l11lll1_opy_(bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨợ")]):
        return False
    if bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧỤ") in bstack1111ll1l1l_opy_ and bstack1111l11lll1_opy_(bstack1111ll1l1l_opy_[bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨụ")]):
        return False
    return True
def bstack1l1ll1lll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack111l1111ll1_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢỦ"), None)
        return bstack111l1111ll1_opy_ is None or bstack111l1111ll1_opy_ == bstack1l1lll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧủ")
    except Exception as e:
        return False
def bstack1l1l1l1l1_opy_(hub_url, CONFIG):
    if bstack1l111l111l_opy_() <= version.parse(bstack1l1lll1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩỨ")):
        if hub_url:
            return bstack1l1lll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦứ") + hub_url + bstack1l1lll1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣỪ")
        return bstack1l1ll111l_opy_
    if hub_url:
        return bstack1l1lll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢừ") + hub_url + bstack1l1lll1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢỬ")
    return bstack1l1l1l11l_opy_
def bstack1111l1111ll_opy_():
    return isinstance(os.getenv(bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ử")), str)
def bstack1l11l1l1l_opy_(url):
    return urlparse(url).hostname
def bstack1lll111ll_opy_(hostname):
    for bstack1l1l1lll1_opy_ in bstack11l111l111_opy_:
        regex = re.compile(bstack1l1l1lll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11ll11_opy_(bstack1111ll1l111_opy_, file_name, logger):
    bstack11l1l111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1lll1_opy_ (u"ࠨࢀࠪỮ")), bstack1111ll1l111_opy_)
    try:
        if not os.path.exists(bstack11l1l111ll_opy_):
            os.makedirs(bstack11l1l111ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1lll1_opy_ (u"ࠩࢁࠫữ")), bstack1111ll1l111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1lll1_opy_ (u"ࠪࡻࠬỰ")):
                pass
            with open(file_path, bstack1l1lll1_opy_ (u"ࠦࡼ࠱ࠢự")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1l1llll_opy_.format(str(e)))
def bstack11l1l11lll1_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11ll11_opy_(bstack1l1lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬỲ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11l111_opy_ = json.load(open(file_path, bstack1l1lll1_opy_ (u"࠭ࡲࡣࠩỳ")))
        else:
            bstack1l11l111_opy_ = {}
        bstack1l11l111_opy_[key] = value
        with open(file_path, bstack1l1lll1_opy_ (u"ࠢࡸ࠭ࠥỴ")) as outfile:
            json.dump(bstack1l11l111_opy_, outfile)
def bstack11l1ll11ll_opy_(file_name, logger):
    file_path = bstack11l1l11ll11_opy_(bstack1l1lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨỵ"), file_name, logger)
    bstack1l11l111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1lll1_opy_ (u"ࠩࡵࠫỶ")) as bstack11llll1lll_opy_:
            bstack1l11l111_opy_ = json.load(bstack11llll1lll_opy_)
    return bstack1l11l111_opy_
def bstack11llll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧỷ") + file_path + bstack1l1lll1_opy_ (u"ࠫࠥ࠭Ỹ") + str(e))
def bstack1l111l111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1lll1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢỹ")
def bstack1lll1ll1l1_opy_(config):
    if bstack1l1lll1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬỺ") in config:
        del (config[bstack1l1lll1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ỻ")])
        return False
    if bstack1l111l111l_opy_() < version.parse(bstack1l1lll1_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧỼ")):
        return False
    if bstack1l111l111l_opy_() >= version.parse(bstack1l1lll1_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨỽ")):
        return True
    if bstack1l1lll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪỾ") in config and config[bstack1l1lll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫỿ")] is False:
        return False
    else:
        return True
def bstack111lllll1_opy_(args_list, bstack1111l1l1l11_opy_):
    index = -1
    for value in bstack1111l1l1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111ll1ll1ll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111ll1ll1ll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111llll11l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111llll11l_opy_ = bstack111llll11l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1lll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬἀ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ἁ"), exception=exception)
    def bstack1111l111l1_opy_(self):
        if self.result != bstack1l1lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἂ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1lll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦἃ") in self.exception_type:
            return bstack1l1lll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥἄ")
        return bstack1l1lll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦἅ")
    def bstack11l1l111l11_opy_(self):
        if self.result != bstack1l1lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫἆ"):
            return None
        if self.bstack111llll11l_opy_:
            return self.bstack111llll11l_opy_
        return bstack11111lll111_opy_(self.exception)
def bstack11111lll111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l11l1111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1l1111l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11111llll_opy_(config, logger):
    try:
        import playwright
        bstack1111ll1ll11_opy_ = playwright.__file__
        bstack1111lll1l11_opy_ = os.path.split(bstack1111ll1ll11_opy_)
        bstack11111lll1l1_opy_ = bstack1111lll1l11_opy_[0] + bstack1l1lll1_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨἇ")
        os.environ[bstack1l1lll1_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩἈ")] = bstack1l111ll111_opy_(config)
        with open(bstack11111lll1l1_opy_, bstack1l1lll1_opy_ (u"ࠧࡳࠩἉ")) as f:
            bstack1l111l111_opy_ = f.read()
            bstack1111ll1lll1_opy_ = bstack1l1lll1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧἊ")
            bstack1111l1ll11l_opy_ = bstack1l111l111_opy_.find(bstack1111ll1lll1_opy_)
            if bstack1111l1ll11l_opy_ == -1:
              process = subprocess.Popen(bstack1l1lll1_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨἋ"), shell=True, cwd=bstack1111lll1l11_opy_[0])
              process.wait()
              bstack1111l1llll1_opy_ = bstack1l1lll1_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪἌ")
              bstack1111l1ll1l1_opy_ = bstack1l1lll1_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣἍ")
              bstack1111l11111l_opy_ = bstack1l111l111_opy_.replace(bstack1111l1llll1_opy_, bstack1111l1ll1l1_opy_)
              with open(bstack11111lll1l1_opy_, bstack1l1lll1_opy_ (u"ࠬࡽࠧἎ")) as f:
                f.write(bstack1111l11111l_opy_)
    except Exception as e:
        logger.error(bstack1l1111l11l_opy_.format(str(e)))
def bstack111l1111_opy_():
  try:
    bstack1111l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭Ἇ"))
    bstack1111l11l1l1_opy_ = []
    if os.path.exists(bstack1111l1ll111_opy_):
      with open(bstack1111l1ll111_opy_) as f:
        bstack1111l11l1l1_opy_ = json.load(f)
      os.remove(bstack1111l1ll111_opy_)
    return bstack1111l11l1l1_opy_
  except:
    pass
  return []
def bstack1ll11ll11_opy_(bstack11ll1111l1_opy_):
  try:
    bstack1111l11l1l1_opy_ = []
    bstack1111l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧἐ"))
    if os.path.exists(bstack1111l1ll111_opy_):
      with open(bstack1111l1ll111_opy_) as f:
        bstack1111l11l1l1_opy_ = json.load(f)
    bstack1111l11l1l1_opy_.append(bstack11ll1111l1_opy_)
    with open(bstack1111l1ll111_opy_, bstack1l1lll1_opy_ (u"ࠨࡹࠪἑ")) as f:
        json.dump(bstack1111l11l1l1_opy_, f)
  except:
    pass
def bstack11111l1l_opy_(logger, bstack1111lll1l1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1lll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬἒ"), bstack1l1lll1_opy_ (u"ࠪࠫἓ"))
    if test_name == bstack1l1lll1_opy_ (u"ࠫࠬἔ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫἕ"), bstack1l1lll1_opy_ (u"࠭ࠧ἖"))
    bstack1111l111l11_opy_ = bstack1l1lll1_opy_ (u"ࠧ࠭ࠢࠪ἗").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111lll1l1l_opy_:
        bstack1l1l11111_opy_ = os.environ.get(bstack1l1lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨἘ"), bstack1l1lll1_opy_ (u"ࠩ࠳ࠫἙ"))
        bstack11llllll1_opy_ = {bstack1l1lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨἚ"): test_name, bstack1l1lll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪἛ"): bstack1111l111l11_opy_, bstack1l1lll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫἜ"): bstack1l1l11111_opy_}
        bstack1111l11l1ll_opy_ = []
        bstack1111llll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬἝ"))
        if os.path.exists(bstack1111llll1ll_opy_):
            with open(bstack1111llll1ll_opy_) as f:
                bstack1111l11l1ll_opy_ = json.load(f)
        bstack1111l11l1ll_opy_.append(bstack11llllll1_opy_)
        with open(bstack1111llll1ll_opy_, bstack1l1lll1_opy_ (u"ࠧࡸࠩ἞")) as f:
            json.dump(bstack1111l11l1ll_opy_, f)
    else:
        bstack11llllll1_opy_ = {bstack1l1lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭἟"): test_name, bstack1l1lll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨἠ"): bstack1111l111l11_opy_, bstack1l1lll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩἡ"): str(multiprocessing.current_process().name)}
        if bstack1l1lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨἢ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llllll1_opy_)
  except Exception as e:
      logger.warn(bstack1l1lll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤἣ").format(e))
def bstack1l111111l1_opy_(error_message, test_name, index, logger):
  try:
    bstack111l11111ll_opy_ = []
    bstack11llllll1_opy_ = {bstack1l1lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫἤ"): test_name, bstack1l1lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ἥ"): error_message, bstack1l1lll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧἦ"): index}
    bstack111l111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪἧ"))
    if os.path.exists(bstack111l111llll_opy_):
        with open(bstack111l111llll_opy_) as f:
            bstack111l11111ll_opy_ = json.load(f)
    bstack111l11111ll_opy_.append(bstack11llllll1_opy_)
    with open(bstack111l111llll_opy_, bstack1l1lll1_opy_ (u"ࠪࡻࠬἨ")) as f:
        json.dump(bstack111l11111ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢἩ").format(e))
def bstack1l11111lll_opy_(bstack1llll11ll_opy_, name, logger):
  try:
    bstack11llllll1_opy_ = {bstack1l1lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἪ"): name, bstack1l1lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬἫ"): bstack1llll11ll_opy_, bstack1l1lll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭Ἤ"): str(threading.current_thread()._name)}
    return bstack11llllll1_opy_
  except Exception as e:
    logger.warn(bstack1l1lll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧἭ").format(e))
  return
def bstack1111l1l111l_opy_():
    return platform.system() == bstack1l1lll1_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪἮ")
def bstack11l11lll1_opy_(bstack1111lll1ll1_opy_, config, logger):
    bstack11111lll11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111lll1ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤἯ").format(e))
    return bstack11111lll11l_opy_
def bstack1111lllll1l_opy_(bstack11111lllll1_opy_, bstack1111ll1l11l_opy_):
    bstack1111llllll1_opy_ = version.parse(bstack11111lllll1_opy_)
    bstack1111ll111l1_opy_ = version.parse(bstack1111ll1l11l_opy_)
    if bstack1111llllll1_opy_ > bstack1111ll111l1_opy_:
        return 1
    elif bstack1111llllll1_opy_ < bstack1111ll111l1_opy_:
        return -1
    else:
        return 0
def bstack111l1l11ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l111l1l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1lll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1lllll_opy_(options, framework, config, bstack1l1ll1ll1l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1lll1_opy_ (u"ࠫ࡬࡫ࡴࠨἰ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1l11111_opy_ = caps.get(bstack1l1lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ἱ"))
    bstack1111l11llll_opy_ = True
    bstack1ll111l111_opy_ = os.environ[bstack1l1lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫἲ")]
    bstack1ll1l1ll11l_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧἳ"), False)
    if bstack1ll1l1ll11l_opy_:
        bstack1lllll11l1l_opy_ = config.get(bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨἴ"), {})
        bstack1lllll11l1l_opy_[bstack1l1lll1_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬἵ")] = os.getenv(bstack1l1lll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨἶ"))
        bstack111llll11ll_opy_ = json.loads(os.getenv(bstack1l1lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬἷ"), bstack1l1lll1_opy_ (u"ࠬࢁࡽࠨἸ"))).get(bstack1l1lll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧἹ"))
    if bstack1111l11lll1_opy_(caps.get(bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭Ἲ"))) or bstack1111l11lll1_opy_(caps.get(bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨἻ"))):
        bstack1111l11llll_opy_ = False
    if bstack1lll1ll1l1_opy_({bstack1l1lll1_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤἼ"): bstack1111l11llll_opy_}):
        bstack11l1l11111_opy_ = bstack11l1l11111_opy_ or {}
        bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬἽ")] = bstack1111l1lll11_opy_(framework)
        bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ἶ")] = bstack1l1llll1111_opy_()
        bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨἿ")] = bstack1ll111l111_opy_
        bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨὀ")] = bstack1l1ll1ll1l_opy_
        if bstack1ll1l1ll11l_opy_:
            bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὁ")] = bstack1ll1l1ll11l_opy_
            bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨὂ")] = bstack1lllll11l1l_opy_
            bstack11l1l11111_opy_[bstack1l1lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩὃ")][bstack1l1lll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫὄ")] = bstack111llll11ll_opy_
        if getattr(options, bstack1l1lll1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬὅ"), None):
            options.set_capability(bstack1l1lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭὆"), bstack11l1l11111_opy_)
        else:
            options[bstack1l1lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ὇")] = bstack11l1l11111_opy_
    else:
        if getattr(options, bstack1l1lll1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨὈ"), None):
            options.set_capability(bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩὉ"), bstack1111l1lll11_opy_(framework))
            options.set_capability(bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪὊ"), bstack1l1llll1111_opy_())
            options.set_capability(bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬὋ"), bstack1ll111l111_opy_)
            options.set_capability(bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬὌ"), bstack1l1ll1ll1l_opy_)
            if bstack1ll1l1ll11l_opy_:
                options.set_capability(bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫὍ"), bstack1ll1l1ll11l_opy_)
                options.set_capability(bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ὎"), bstack1lllll11l1l_opy_)
                options.set_capability(bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ὏"), bstack111llll11ll_opy_)
        else:
            options[bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩὐ")] = bstack1111l1lll11_opy_(framework)
            options[bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪὑ")] = bstack1l1llll1111_opy_()
            options[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬὒ")] = bstack1ll111l111_opy_
            options[bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬὓ")] = bstack1l1ll1ll1l_opy_
            if bstack1ll1l1ll11l_opy_:
                options[bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫὔ")] = bstack1ll1l1ll11l_opy_
                options[bstack1l1lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬὕ")] = bstack1lllll11l1l_opy_
                options[bstack1l1lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ὖ")][bstack1l1lll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩὗ")] = bstack111llll11ll_opy_
    return options
def bstack111l111111l_opy_(bstack11111llllll_opy_, framework):
    bstack1l1ll1ll1l_opy_ = bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ὘"))
    if bstack11111llllll_opy_ and len(bstack11111llllll_opy_.split(bstack1l1lll1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩὙ"))) > 1:
        ws_url = bstack11111llllll_opy_.split(bstack1l1lll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ὚"))[0]
        if bstack1l1lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨὛ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111ll11111_opy_ = json.loads(urllib.parse.unquote(bstack11111llllll_opy_.split(bstack1l1lll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ὜"))[1]))
            bstack1111ll11111_opy_ = bstack1111ll11111_opy_ or {}
            bstack1ll111l111_opy_ = os.environ[bstack1l1lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬὝ")]
            bstack1111ll11111_opy_[bstack1l1lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ὞")] = str(framework) + str(__version__)
            bstack1111ll11111_opy_[bstack1l1lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪὟ")] = bstack1l1llll1111_opy_()
            bstack1111ll11111_opy_[bstack1l1lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬὠ")] = bstack1ll111l111_opy_
            bstack1111ll11111_opy_[bstack1l1lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬὡ")] = bstack1l1ll1ll1l_opy_
            bstack11111llllll_opy_ = bstack11111llllll_opy_.split(bstack1l1lll1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫὢ"))[0] + bstack1l1lll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬὣ") + urllib.parse.quote(json.dumps(bstack1111ll11111_opy_))
    return bstack11111llllll_opy_
def bstack1lll1111l_opy_():
    global bstack11l11lllll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l11lllll_opy_ = BrowserType.connect
    return bstack11l11lllll_opy_
def bstack1111lll1l_opy_(framework_name):
    global bstack1l1111llll_opy_
    bstack1l1111llll_opy_ = framework_name
    return framework_name
def bstack11lll1l1l_opy_(self, *args, **kwargs):
    global bstack11l11lllll_opy_
    try:
        global bstack1l1111llll_opy_
        if bstack1l1lll1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫὤ") in kwargs:
            kwargs[bstack1l1lll1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬὥ")] = bstack111l111111l_opy_(
                kwargs.get(bstack1l1lll1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ὦ"), None),
                bstack1l1111llll_opy_
            )
    except Exception as e:
        logger.error(bstack1l1lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥὧ").format(str(e)))
    return bstack11l11lllll_opy_(self, *args, **kwargs)
def bstack1111lllllll_opy_(bstack1111ll11lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l11ll11l_opy_(bstack1111ll11lll_opy_, bstack1l1lll1_opy_ (u"ࠦࠧὨ"))
        if proxies and proxies.get(bstack1l1lll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦὩ")):
            parsed_url = urlparse(proxies.get(bstack1l1lll1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧὪ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1lll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪὫ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫὬ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬὭ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭Ὦ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll11111_opy_(bstack1111ll11lll_opy_):
    bstack111l1111l1l_opy_ = {
        bstack111l1l1l11l_opy_[bstack11111llll1l_opy_]: bstack1111ll11lll_opy_[bstack11111llll1l_opy_]
        for bstack11111llll1l_opy_ in bstack1111ll11lll_opy_
        if bstack11111llll1l_opy_ in bstack111l1l1l11l_opy_
    }
    bstack111l1111l1l_opy_[bstack1l1lll1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦὯ")] = bstack1111lllllll_opy_(bstack1111ll11lll_opy_, bstack111l111l1_opy_.get_property(bstack1l1lll1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧὰ")))
    bstack111l111lll1_opy_ = [element.lower() for element in bstack111l1lllll1_opy_]
    bstack111l111ll1l_opy_(bstack111l1111l1l_opy_, bstack111l111lll1_opy_)
    return bstack111l1111l1l_opy_
def bstack111l111ll1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1lll1_opy_ (u"ࠨࠪࠫࠬ࠭ࠦά")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l111ll1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l111ll1l_opy_(item, keys)
def bstack1l1ll1lll11_opy_():
    bstack1111l111lll_opy_ = [os.environ.get(bstack1l1lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤὲ")), os.path.join(os.path.expanduser(bstack1l1lll1_opy_ (u"ࠣࢀࠥέ")), bstack1l1lll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩὴ")), os.path.join(bstack1l1lll1_opy_ (u"ࠪ࠳ࡹࡳࡰࠨή"), bstack1l1lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫὶ"))]
    for path in bstack1111l111lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1lll1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧί") + str(path) + bstack1l1lll1_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤὸ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1lll1_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦό") + str(path) + bstack1l1lll1_opy_ (u"ࠣࠩࠥὺ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1lll1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤύ") + str(path) + bstack1l1lll1_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣὼ"))
            else:
                logger.debug(bstack1l1lll1_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨώ") + str(path) + bstack1l1lll1_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ὾"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1lll1_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ὿") + str(path) + bstack1l1lll1_opy_ (u"ࠢࠨ࠰ࠥᾀ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᾁ") + str(e) + bstack1l1lll1_opy_ (u"ࠤࠥᾂ"))
    logger.debug(bstack1l1lll1_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᾃ"))
    return None
@measure(event_name=EVENTS.bstack111l1l1l111_opy_, stage=STAGE.bstack1lllll111l_opy_)
def bstack1lll11lll1l_opy_(binary_path, bstack1lll1lll111_opy_, bs_config):
    logger.debug(bstack1l1lll1_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᾄ").format(binary_path))
    bstack1111lll111l_opy_ = bstack1l1lll1_opy_ (u"ࠬ࠭ᾅ")
    bstack1111l1lll1l_opy_ = {
        bstack1l1lll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᾆ"): __version__,
        bstack1l1lll1_opy_ (u"ࠢࡰࡵࠥᾇ"): platform.system(),
        bstack1l1lll1_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᾈ"): platform.machine(),
        bstack1l1lll1_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᾉ"): bstack1l1lll1_opy_ (u"ࠪ࠴ࠬᾊ"),
        bstack1l1lll1_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᾋ"): bstack1l1lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᾌ")
    }
    bstack1111l1l1111_opy_(bstack1111l1lll1l_opy_)
    try:
        if binary_path:
            bstack1111l1lll1l_opy_[bstack1l1lll1_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᾍ")] = subprocess.check_output([binary_path, bstack1l1lll1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᾎ")]).strip().decode(bstack1l1lll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᾏ"))
        response = requests.request(
            bstack1l1lll1_opy_ (u"ࠩࡊࡉ࡙࠭ᾐ"),
            url=bstack1llllll111_opy_(bstack111l1l11l1l_opy_),
            headers=None,
            auth=(bs_config[bstack1l1lll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᾑ")], bs_config[bstack1l1lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᾒ")]),
            json=None,
            params=bstack1111l1lll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1lll1_opy_ (u"ࠬࡻࡲ࡭ࠩᾓ") in data.keys() and bstack1l1lll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᾔ") in data.keys():
            logger.debug(bstack1l1lll1_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᾕ").format(bstack1111l1lll1l_opy_[bstack1l1lll1_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᾖ")]))
            if bstack1l1lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᾗ") in os.environ:
                logger.debug(bstack1l1lll1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥᾘ"))
                data[bstack1l1lll1_opy_ (u"ࠫࡺࡸ࡬ࠨᾙ")] = os.environ[bstack1l1lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᾚ")]
            bstack11lll11ll11_opy_ = bstack1111l1ll1ll_opy_(data[bstack1l1lll1_opy_ (u"࠭ࡵࡳ࡮ࠪᾛ")], bstack1lll1lll111_opy_)
            bstack1111lll111l_opy_ = os.path.join(bstack1lll1lll111_opy_, bstack11lll11ll11_opy_)
            os.chmod(bstack1111lll111l_opy_, 0o777) # bstack1111ll1l1l1_opy_ permission
            return bstack1111lll111l_opy_
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᾜ").format(e))
    return binary_path
def bstack1111l1l1111_opy_(bstack1111l1lll1l_opy_):
    try:
        if bstack1l1lll1_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᾝ") not in bstack1111l1lll1l_opy_[bstack1l1lll1_opy_ (u"ࠩࡲࡷࠬᾞ")].lower():
            return
        if os.path.exists(bstack1l1lll1_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᾟ")):
            with open(bstack1l1lll1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᾠ"), bstack1l1lll1_opy_ (u"ࠧࡸࠢᾡ")) as f:
                bstack1111lll1lll_opy_ = {}
                for line in f:
                    if bstack1l1lll1_opy_ (u"ࠨ࠽ࠣᾢ") in line:
                        key, value = line.rstrip().split(bstack1l1lll1_opy_ (u"ࠢ࠾ࠤᾣ"), 1)
                        bstack1111lll1lll_opy_[key] = value.strip(bstack1l1lll1_opy_ (u"ࠨࠤ࡟ࠫࠬᾤ"))
                bstack1111l1lll1l_opy_[bstack1l1lll1_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᾥ")] = bstack1111lll1lll_opy_.get(bstack1l1lll1_opy_ (u"ࠥࡍࡉࠨᾦ"), bstack1l1lll1_opy_ (u"ࠦࠧᾧ"))
        elif os.path.exists(bstack1l1lll1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᾨ")):
            bstack1111l1lll1l_opy_[bstack1l1lll1_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᾩ")] = bstack1l1lll1_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᾪ")
    except Exception as e:
        logger.debug(bstack1l1lll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᾫ") + e)
@measure(event_name=EVENTS.bstack111l1ll1l1l_opy_, stage=STAGE.bstack1lllll111l_opy_)
def bstack1111l1ll1ll_opy_(bstack11111llll11_opy_, bstack1111l1111l1_opy_):
    logger.debug(bstack1l1lll1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᾬ") + str(bstack11111llll11_opy_) + bstack1l1lll1_opy_ (u"ࠥࠦᾭ"))
    zip_path = os.path.join(bstack1111l1111l1_opy_, bstack1l1lll1_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᾮ"))
    bstack11lll11ll11_opy_ = bstack1l1lll1_opy_ (u"ࠬ࠭ᾯ")
    with requests.get(bstack11111llll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1lll1_opy_ (u"ࠨࡷࡣࠤᾰ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1lll1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᾱ"))
    with zipfile.ZipFile(zip_path, bstack1l1lll1_opy_ (u"ࠨࡴࠪᾲ")) as zip_ref:
        bstack1111lll11ll_opy_ = zip_ref.namelist()
        if len(bstack1111lll11ll_opy_) > 0:
            bstack11lll11ll11_opy_ = bstack1111lll11ll_opy_[0] # bstack11111lll1ll_opy_ bstack111l1llllll_opy_ will be bstack1111l1l11l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111l1111l1_opy_)
        logger.debug(bstack1l1lll1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᾳ") + str(bstack1111l1111l1_opy_) + bstack1l1lll1_opy_ (u"ࠥࠫࠧᾴ"))
    os.remove(zip_path)
    return bstack11lll11ll11_opy_
def get_cli_dir():
    bstack1111ll1ll1l_opy_ = bstack1l1ll1lll11_opy_()
    if bstack1111ll1ll1l_opy_:
        bstack1lll1lll111_opy_ = os.path.join(bstack1111ll1ll1l_opy_, bstack1l1lll1_opy_ (u"ࠦࡨࡲࡩࠣ᾵"))
        if not os.path.exists(bstack1lll1lll111_opy_):
            os.makedirs(bstack1lll1lll111_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1lll111_opy_
    else:
        raise FileNotFoundError(bstack1l1lll1_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᾶ"))
def bstack1ll1lll11l1_opy_(bstack1lll1lll111_opy_):
    bstack1l1lll1_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᾷ")
    bstack1111l11ll11_opy_ = [
        os.path.join(bstack1lll1lll111_opy_, f)
        for f in os.listdir(bstack1lll1lll111_opy_)
        if os.path.isfile(os.path.join(bstack1lll1lll111_opy_, f)) and f.startswith(bstack1l1lll1_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᾸ"))
    ]
    if len(bstack1111l11ll11_opy_) > 0:
        return max(bstack1111l11ll11_opy_, key=os.path.getmtime) # get bstack11llll1111l_opy_ binary
    return bstack1l1lll1_opy_ (u"ࠣࠤᾹ")
def bstack111lll1l111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11llll11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11llll11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d