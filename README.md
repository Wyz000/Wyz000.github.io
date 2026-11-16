# Yuze Wu's academic website

Personal academic homepage at https://wyz000.github.io/.

The design takes inspiration from al-folio while retaining this repository's static HTML deployment. Existing GIFs, contact files and research-note URLs are preserved.

## Update content

- `data/profile.json`: name, role, affiliation, contact, honors and site metadata.
- `data/news.json`: monthly news, ordered newest first; the first eight items appear by default.
- `data/publications.json`: publication records, links, author roles and source evidence.
- `scripts/build.py`: page copy, page structure and publication rendering.
- `assets/css/site.css`: responsive layout and light/dark themes.
- `assets/js/site.js`: publication search, filters, theme switching, navigation and on-demand demos.

Run `python3 scripts/build.py` after editing content. Commit the generated HTML pages together with source changes. GitHub Pages serves the files at the repository root; no Ruby or Node build is needed.

For local preview, run `python3 -m http.server 8000` at the repository root.

Publication entries distinguish preprints from accepted or published papers. Add a paper only after checking its title, author list, venue, year and public links. Use `co_first_authors` and `corresponding_authors` to record author roles; author names in these arrays must match the full author list. Control each role independently: show all co-first authors with `*` only when Yuze Wu is co-first; show all corresponding authors with `#` only when Yuze Wu is corresponding. Show both groups only when Yuze Wu has both roles. An empty array means no marker is declared; `null` means the source did not establish the role. Sources are retained in the JSON for future updates. News dates must come from an announcement or publication record; do not use conference dates as acceptance dates. Do not place private CVs, student information without permission, or credentials in this repository.

## Design credits

- [al-folio](https://github.com/alshedivat/al-folio): visual inspiration.
- [Jon Barron](https://jonbarron.info/): the previous site's original layout inspiration.
