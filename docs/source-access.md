# Source access: where the agents read (draft, 2026-11-16)

The verification loop (agents.md, Source verification) only works where a session can
fetch the source. Today the environment allows three hosts (developers.cloudflare.com,
commons.wikimedia.org, upload.wikimedia.org), so almost every source below is blocked.
Each host is added to the environment with Cade's approval; a key is entered by Cade in a
secure form and never pasted into a chat.

## 1. Free and open, no key (add first)

| Host | What it gives | Used for |
| --- | --- | --- |
| doi.org, api.crossref.org | The record of every article with a DOI | The resolver script: does this article exist, with this author, title and year |
| openlibrary.org | Book records by ISBN | The resolver script for books |
| archive.org, web.archive.org, scholar.archive.org | Scanned books, saved web pages, open papers | Reading passages; the saved copy of every cited page |
| api.openalex.org | An open index of scholarly work | Finding scholarship and checking authors |
| avalon.law.yale.edu | Texts of treaties, laws and diplomatic papers | Primary texts (Versailles among them) |
| sourcebooks.fordham.edu | Primary texts by era, ancient to modern | Primary texts |
| www.loc.gov | The Library of Congress: catalogue and digitised collections | Records, primary sources, pictures |
| catalog.archives.gov | The US National Archives | Primary records and pictures |
| discovery.nationalarchives.gov.uk | The UK National Archives catalogue | Primary records |
| gallica.bnf.fr | The French national library's scans | Primary texts and maps |
| babel.hathitrust.org | Scanned library books; public-domain books in full | Reading passages in older books |
| www.gutenberg.org | Public-domain books | Primary texts and older accounts |
| www.perseus.tufts.edu | Greek and Latin texts | The ancient world |
| ctext.org | Chinese texts | The Chinese record |
| www.britannica.com, en.wikipedia.org | The two exits | Checking each page's exits |

## 2. Free with a key (Cade signs up; the key goes in through the secure form)

| Service | Used for |
| --- | --- |
| Semantic Scholar | Finding scholarship and its open copies |
| CORE | Open-access copies of papers |
| Europeana | European archives and museums |
| DPLA (Digital Public Library of America) | American archives and libraries |
| Google Books | Previews, so a passage in a paywalled book can be read |

## 3. What only Cade can open

- **A library card.** Many public libraries give their members free access to scholarly
  databases (which ones varies by library). Worth asking his library what it offers.
- **University or alumni access**, if he has any: JSTOR runs an alumni programme with many
  universities, and JSTOR holds most of the history journals.
- **The audit.** Cade's hand check of one source in five, then one in twenty, can use any
  book he can borrow, including the Internet Archive's lending library with his own free
  account. Agents never use his login to borrow books.

## Rules

- A source behind a paywall that no agent can read is left out. A better book that cannot
  be read loses to a good one that can.
- Agents respect each site's terms: no mass downloading, and a pause between requests.
- Requests identify the atlas generically, never with Cade's name or email.
