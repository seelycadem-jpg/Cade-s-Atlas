# Pipeline scripts: not yet recovered

This folder is reserved for the Python build pipeline and `build.sh`. The published
atlas holds only built output, so these scripts are absent from this first commit.

Scripts to recover from the workspace of the main atlas chat:

- Core build: `build.sh`, `make_json.py`, `arcs_build.py`, `refine.py`, `tiers.py`,
  `deepen.py`, `links.py`, `map_rules.py`, `polities.py`, `analysis.py`,
  `briefcheck.py`, `graph_build.py`, `graph/`
- Content sources: `arc_*.py`, `details*.py`, `deepen*.py`, `an*.py`, `refine*.py`,
  `arcs_all*.py`
- Borders: `g3/` (`clio.py`, `prep.py`, `landgl.py`, `snap.py`, `chunk.py`) and `g4/`
  (`prov.py`, `prov_rivers.py`, `topo.py`, `owners.py`, `owners_anc.py`, `estimate.py`,
  `audit.py`)
- Review material: `review/` (`gaz`, `cp`, `fix/*.json`, `writing/EVENT_PAGE_BRIEF.md`,
  `ANC_BRIEF.md`, `BLANK_BRIEF.md`, `events_anc/arcs`)

This list comes from the project docs and chat history, and it may be incomplete.
Delete this file once the scripts are in place.
