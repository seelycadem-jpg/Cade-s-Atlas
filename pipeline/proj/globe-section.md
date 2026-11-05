## The globe (rebuilt on the graphics card, 2026-10-29)

The atlas globe is drawn by MapLibre GL (loaded from jsDelivr, version 5.6.0) in globe projection, with a flat web-map view as the alternative. Land, states, borders, coastal lines, relief and rivers are GPU layers; names, cities, event markers and arc threads are drawn on a light canvas above it from projected points. Changing the year only changes layer filters and feature colours, so it is instant; dragging and zooming never redraw on the CPU. Story-page medal globes still use the older canvas globe.

Borders 1400-1885: Cliopatria, the polity borders dataset of the Seshat Global History Databank (CC BY 4.0, credited on the About page as the licence requires). Base polities are the territories drawn; unions (Holy Roman Empire, Kingdom of France, Spanish Empire and the like) are drawn as a broader outer border and named at low zoom; members and vassals take the overlord's colour in a lighter shade. Each record is clipped only where it runs far out to sea. Where no state is recorded, land is shaded faintly as the peoples of its region (from the older survey maps). Data in maps/g/c{start}.json, twenty-year chunks; pipeline g3/clio.py then g3/build.py.

Borders from 1886: CShapes 2.0 (maps/cs.json), evaluated at mid-year, plus land the record leaves empty (maps/csgaps.json). The ledger lists dated changes; survey notes were removed.

Hand-drawn patches and survey-based dating were retired from the atlas globe on 2026-10-29: the user judged them awkward and under-researched. Do not reintroduce hand-drawn polygons; correct borders by reporting them against the reference record.
