# trmnl-baby-growth-plugin

Show the size of a baby each day as a plugin for [TRMNL](https://trmnl.com) devices.

Enter your due date (`DD/MM/YYYY`) and the screen shows, every day until the baby is born:

- a countdown of days (and weeks + days) until the due date
- the current pregnancy week, day and trimester
- an everyday object the baby is about the size of (poppy seed → pumpkin)
- a high-contrast illustration of that object, linked to its image
- the baby's approximate length and weight
- a pregnancy progress bar

After the due date it switches to an "overdue" count for two weeks, then to a "Baby has arrived!" message.
All four TRMNL layouts are supported (full, half horizontal, half vertical, quadrant).

All calculations happen in Liquid (`src/shared.liquid`) using a 280-day (40-week) pregnancy ending on the due date,
so no server or API is needed — the plugin uses the `static` strategy and refreshes hourly so it rolls over each day
in your TRMNL account's time zone. Sizes are typical averages and are for fun, not medical advice.

## Project structure

```
.trmnlp.yml               # local preview config (sample due date)
src/settings.yml          # plugin definition, including the "Due date" custom field
src/shared.liquid         # date parsing, countdown and week-by-week size table
images/                   # monochrome SVG illustrations for the size table
src/full.liquid           # full-screen layout
src/half_horizontal.liquid
src/half_vertical.liquid
src/quadrant.liquid
```

## Develop locally

Uses [trmnlp](https://github.com/usetrmnl/trmnlp) (gem or Docker; `bin/trmnlp` picks whichever is available).

```sh
bin/trmnlp serve   # preview at http://localhost:4567
bin/trmnlp lint    # check against TRMNL best practices
```

Change the sample due date in `.trmnlp.yml` (`custom_fields.due_date`) to preview other stages.

## Install on your TRMNL

```sh
bin/trmnlp login   # paste your TRMNL API key
bin/trmnlp push    # creates the private plugin
```

Then open the plugin in TRMNL, set **Due date** (e.g. `15/03/2027`) and add it to your playlist.
After the first push, run `bin/trmnlp pull` so `src/settings.yml` records the plugin `id` and later pushes update it
instead of creating a new plugin.

The illustrations are loaded from this repository's `main` branch using raw GitHub URLs, so the repository must be
public for TRMNL to fetch them. Each displayed illustration also links directly to its SVG file.

Alternatively, create a Private Plugin in the TRMNL web UI and paste the contents of `src/shared.liquid` into the
Shared markup tab, each layout file into its tab, and import the custom field from `src/settings.yml`.
