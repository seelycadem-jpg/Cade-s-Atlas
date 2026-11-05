"""Where the pipeline reads and writes, in one place.

Every script takes its folders from here, so the pipeline runs from any checkout of the
repo. Prototype 1 ran in a chat workspace; its old folders map as follows:
  /home/claude            -> ROOT     pipeline/ (code and research inputs)
  /home/claude/site       -> SITE     site/ (built data the app reads)
  /home/claude/atlas/maps -> MAPS     site/maps/ (built map data)
  /home/claude/atlas      -> ATLAS    pipeline/atlas/ (Prototype 1 front-end source)
  /mnt/user-data/uploads  -> UPLOADS  pipeline/uploads/ (the original timeline script)
  /tmp                    -> WORK     work/ (scratch and large intermediates; git-ignored)
Set ATLAS_WORK to put scratch somewhere else, and ATLAS_SITE to build into a test folder
instead of site/ (site/ is Prototype 1 and is never edited by hand).
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SITE = os.environ.get("ATLAS_SITE") or os.path.join(REPO, "site")
MAPS = os.path.join(SITE, "maps")
ATLAS = os.path.join(ROOT, "atlas")
UPLOADS = os.path.join(ROOT, "uploads")
WORK = os.environ.get("ATLAS_WORK") or os.path.join(REPO, "work")
os.makedirs(WORK, exist_ok=True)
