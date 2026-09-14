# Trip Guide — build pipeline

Builds `여행_맛집_지도.html`: 283 restaurants across Barcelona, Lisbon and Porto
as one self-contained file. No server, no build step, no dependencies.

Project note: [`wiki/projects/Trip Guide - Shareable Restaurant Map.md`](../../wiki/projects/Trip%20Guide%20-%20Shareable%20Restaurant%20Map.md)

## Inputs

| File | Rows | Role |
| :--- | ---: | :--- |
| `raw/extracts/all-cities-full.csv` | 81 | Michelin + Repsol layer. Has address, phone, cuisine, 1-person price, description. |
| `raw/extracts/bcbm-lisboa-porto.csv` | 165 | Boa Cama Boa Mesa layer. **Name and Google URL only** — no address; `Main_Menu` is cuisine genre, not dishes. |
| `page.py` (`BCN`/`LIS`/`POR`) | 45 | The personal saves, hand-written after filtering a 658-row Google Takeout export. |
| `enrich.json` | 251 | Everything looked up from Google Places, keyed `"{Name}\|{도시}"`. |

Dedupe is by ASCII-normalised name + city. The three layers do not overlap at all.

## Files

| File | What it holds |
| :--- | :--- |
| `build2.py` | The builder. Merges the three layers, renders the HTML, writes the combined CSV. |
| `page.py` | The 45 personal saves + `gurl()`, the Google Maps deep-link builder. |
| `enrich.json` | Places lookups: address, lat/lng, rating, review count, price level, closing day, place ID, dish, note. |
| `mine_coords.json` | Coordinates for the 45 personal saves. |
| `spots.py` | 119 hand-written landmarks with KR/ES/PT/EN search aliases. |
| `syn.py` | Search synonym table (see the docstring — this is the 빠에야 fix). |
| `ko.py` | English → Korean cuisine labels. |
| `notes_guide.py` | Korean one-line characteristics for 65 Michelin/Repsol venues, written from the source descriptions. |
| `mine_dish.py` | Up to 3 dishes for each of the 45 personal saves. |
| `add2.py` | stdin helper: merges `{"Name\|도시": {"dish":…, "note":…}}` into `enrich.json`. |

## Run

```bash
cd scripts/trip_guide
python3 build2.py          # writes the HTML + combined CSV
```

## Design constraints (do not "fix" these)

**Deep links must use the official Maps URL API.** The legacy
`/maps/place/?q=place_id:{pid}` form does not open reliably. Use
`/maps/search/?api=1&query={name}&query_place_id={pid}` — the place ID wins and
the name is the fallback.

**Location input is typed, not GPS.** Browser geolocation is blocked on
`file://`, and the whole point is that this file works when emailed. The
gazetteer (119 landmarks + 283 venue names + ~180 street names derived by
averaging the coordinates of every restaurant on that street) resolves offline;
Nominatim, bounded to an Iberian viewbox, is the fallback only.

**Blank fields are deliberate.** 113 local-guide venues have no dish because no
source has one — `Main_Menu` turned out to hold cuisine genres. Someone will
order from this; a plausible invented dish is worse than an empty line. Same for
Marlene, where Google returns her Time Out stall rather than the flagship.

**Prices are marked.** `€45` came from the source CSV. `~€35` was derived from
Google's 1–4 price level (€12 / €22 / €35 / €60). The tilde is the only thing
distinguishing them — keep it.

## Open

- 113 local-guide dishes and 134 characteristics still unfilled (~22 more
  Places lookup rounds at 6 venues each).
- **Pisca** (Porto): guide address + phone match a listing now named
  *Restaurante Paco*. Probably rebranded, unverified.
- **Jardín del Alma** (Barcelona): Google lists it as *Jardí de l'Ànima*.
- Dessert layer scoped but not built — *O Melhor Pastel de Nata* finalists
  (Lisbon) and *Mejor Croissant Artesano* winners (Barcelona), already
  documented as guides #12/#13 in `selected-restaurants.md`.
