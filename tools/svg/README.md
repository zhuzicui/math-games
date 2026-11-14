# Splitting an SVG sheet into one SVG per drawing

How the game art (birds, fish, balloons, market food, cookies, beads, train, night sky, crocodile) was cut out of the original artwork sheets. Run from a scratch folder that holds `src/<sheet>.svg`; Node needs Playwright (preinstalled in Claude's cloud machines) and Python needs lxml, Pillow, numpy and scipy.

1. `python3 tag.py src tag` gives every drawable in each sheet a `data-k` number.
2. `node bbox.js tag bb` measures each one's box in sheet units (clip paths included).
3. `python3 hide.py <sheet>` lists background shapes (anything over 20% of the sheet), `node samples.js <sheet>` renders the sheet without them, and `python3 comp.py 3 <sheet>` groups shapes into drawings by which blob of the render they fall in (`cl/<sheet>.json`, with a numbered preview in `cl/<sheet>.png`).
   Drawings that touch (beads on a string, penguins in their train cars) are picked by hand instead: `node zoom.js` draws a grid in sheet units and `pick.py` takes every shape fully inside a box.
4. `python3 export.py <sheet>` writes one SVG per group; `node rbox.js 128 elr el/<sheet>/*.svg` renders them and `python3 match.py <sheet> <folder>` finds which drawing each existing picture is.
5. `python3 flatten.py raw flat` bakes every transform into the path data, scales each drawing to 1000 units and rounds to whole units (≈0.3 px on an iPad), drops metadata and default styles; `node tight.js flat/**/*.svg` crops the viewBox to the ink.

Each finished SVG keeps `width`/`height` equal to the PNG it replaced, so layout is unchanged.
The cookies are the orange cookie sheet recoloured with a colour mapping fitted to the earlier red and blue cookies.
