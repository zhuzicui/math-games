# Dark mode: design and build spec

Status: design prototype. The switch, the boot code and the dark colours for the shared chrome, the home screens,
Feed the Unicorn, Hungry Crocodile, the reward screens, the rainbow screen and the grown-ups area are in `index.html`
on this branch. The other games are only partly covered (they inherit the tokens) and are the build work listed in section 7.

Sample screens: `/mnt/project-files/dark-mode/dark-mode-light-vs-dark.png`.

## 1. Principles

1. **Light mode is not touched.** No existing CSS rule is edited for dark mode. Everything dark lives in one block at the
   end of `<style>`, under `html[data-theme="dark"]`. Light screenshots must stay pixel-identical (checked for the home
   screens with `cmp`).
2. **Chrome goes cocoa, scenes go dusk.** Page, cards, bubbles, text and buttons turn warm dark brown with cream text.
   Game scenes (water, sky, garden, rails) keep their own hue and go to a mid-dark "dusk" value, never near-black.
3. **Dark mode is never blue-violet.** That colour belongs to the lock screen ("time is up"). A child must be able to tell
   "the app is dark" from "the app is asleep".
4. **Artwork is not redrawn and not filtered as a whole.** No `invert`, no global `brightness`. Art keeps its pastel fills,
   which read well on dark. Where a thin brown outline or a dark object would vanish, fix the surface behind it or add a
   thin light rim (section 5).
5. **Anything a child has to count must stay as visible as in light mode.** This outranks looks.
6. **JS never bakes a theme colour into markup.** Colours that change with the theme come from CSS, so a live switch needs
   no re-render.

## 2. Palette

| Token | Light | Dark | Use |
|---|---|---|---|
| `--paper` | `#F7F1EA` | `#2B201C` | page |
| `--card` | `#FFFCF7` | `#3A2D27` | cards, bubbles, round buttons |
| `--lift` (new) | n/a | `#46372F` | a surface one step above a card |
| `--well` (new) | n/a | `#221915` | text inputs |
| `--edge` | `#E6D5C4` | `#5A463C` | borders and the 3D lip under buttons |
| `--ink` | `#5A3E33` | `#F7F1EA` | text |
| `--ink2` | `#7A5A4A` | `#CFBBAD` | secondary text |
| `--line` | `#6B4A3A` | `#EADBCD` | icon strokes |
| `--on-ink` (new) | `#fff` | `#2B201C` | text on a pill filled with `--ink` |
| `--coral` / `-d` | `#E9917A` / `#C46F58` | `#DE8A73` / `#A85C48` | main buttons |
| `--sage` / `-d` | `#A9C99F` / `#7FA474` | `#9CBD92` / `#6A8D61` | Done button |
| `--butter` | `#F7D98C` | `#E6C97F` | "learning" cells |
| `--cta` / `-d` | `#9DCBEC` / `#6EA6D1` | `#8FC0E3` / `#5A8FB8` | blue buttons |
| `--red-ink` | `#B5604A` | `#F4AE9F` | the "already there" number |
| `--blue-ink` | `#3B78A0` | `#A7D0E8` | the "added" number |
| `--red-bg` / `-ring` / `-edge` | `#FCE8E2` / `#F8D6CC` / `#E2A898` | `#4A2F29` / `#5A3830` / `#8A5547` | red surfaces |
| `--blue-bg` / `-edge` / `-slot` | `#E2EEF6` / `#8DB6D0` / `#A6C6DA` | `#263B4B` / `#4C7590` / `#4C7590` | blue surfaces |

Notes
- Cookies (`#A7D0E8` blue, `#F4AE9F` red), beads, blocks, eggs, stars and all image files keep their colours.
  In dark mode the two numbers in a sum take exactly the cookie colours.
- Coloured buttons keep dark brown text (`#2B1D17`) in both modes.
- Text contrast: cream on cocoa is about 14:1; `--ink2` on `--paper` is about 9:1.

Tiles (home and game lists): same hue as light, deep instead of pale. Rule used to derive them from the light
border colour: keep the hue, cap saturation at 0.34, lightness 0.22 for the fill and 0.36 for the border and lip.

| Tile | Dark fill | Dark border |
|---|---|---|
| feed, group-add | `#4B3325` / `#4B3225` | `#7D523B` |
| ten | `#4B4225` | `#7D6D3B` |
| bus, upt | `#253C4B` | `#3B627D` |
| frogt | `#324B25` | `#527A3D` |
| towert | `#4B3825` | `#7D5C3B` |
| writet | `#36254B` | `#573B7D` |
| group-kinder, croct | `#354B25` | `#567D3B` |
| traint | `#26444A` | `#3E7079` |
| beadt | `#4B2530` | `#7D3B4D` |
| birdt | `#253A4B` | `#3B607D` |
| markett | `#4B3B25` | `#7D613B` |
| garden | `#27484A` | `#3F7578` |

Scenes

| Scene | Light | Dark |
|---|---|---|
| Crocodile water | `#D6ECF5 → #BFE0EE → #A9D3E6` | `#34637E → #2B5670 → #234A63`, ripples at 14% opacity |
| Rainbow garden | `#DAECEC` | `#1D3236` |
| Sticker book | `#F3E9DC` | `#30251F` |
| Birds sky | `#D9ECF6 → #E8F3F3 → #F3F1E6` | `#22384C → #2B3F4A → #3A382E` |
| Up and Away sky | `#9FD3F2 → #C7E6F8 → #E6F4FB` | `#1F4463 → #2C5878 → #3B6C8A` |
| Number Train | `train/bg.jpg` | the same picture under a 62% `rgb(22,26,46)` scrim (no new image) |
| Lock screen | night sky | unchanged |

## 3. The switch

- Place: grown-ups area, Settings tab, a new card "Appearance" between "Spoken instructions" and "Progress".
  It uses the existing `.seg` control with three choices. It is behind the maths gate on purpose: the kids' screens stay
  uncluttered and a child cannot flip it mid-game.
- States: **Auto** (default, follows the device), **Light**, **Dark**. A one-line tip under the control explains Auto.
- Storage: `S.theme` = `'auto' | 'light' | 'dark'`, at the top level of the saved state. It is not in `KID_FIELDS`:
  it belongs to the device, not to a child, and "Reset progress" does not change it.
- Strings (keys `theme`, `th_auto`, `th_light`, `th_dark`, `themeTip`), already added in all 7 languages:

| | Label | Auto | Light | Dark | Tip |
|---|---|---|---|---|---|
| en | Appearance | Auto | Light | Dark | Auto follows this device’s setting. |
| fr | Apparence | Auto | Clair | Sombre | Auto suit le réglage de cet appareil. |
| es | Apariencia | Auto | Claro | Oscuro | Auto sigue el ajuste de este dispositivo. |
| zh | 外观 | 自动 | 浅色 | 深色 | “自动”会跟随这台设备的设置。 |
| ja | 外観 | 自動 | ライト | ダーク | 「自動」はこの端末の設定に合わせます。 |
| yue | 外觀 | 自動 | 淺色 | 深色 | 「自動」會跟隨呢部機嘅設定。 |
| ko | 화면 모드 | 자동 | 라이트 | 다크 | 자동은 이 기기의 설정을 따라가요. |

  Every character above was checked against the subset fonts in `fonts/` with fontTools: none missing.
  The zh, ja, yue and ko wording has not been read by a native speaker.

## 4. How it is wired

- `<head>`: a one-line inline script before the stylesheet reads `S.theme` from `localStorage` and the device setting,
  then sets `<html data-theme="light|dark">`. This prevents a flash of light colours on launch.
  **The offline thread also edits `<head>`; keep this script first, before any stylesheet.**
- JS, right after `var S = load()`: `isDark()`, `applyTheme()` and `TOP_COL`.
  `applyTheme()` sets `data-theme`, the `theme-color` meta and the `<html>` background (the strip behind the clock on
  iPhone and iPad). `render()` calls it; so do the switch and the `prefers-color-scheme` change listener, which makes
  Auto follow the device live, even in the middle of a round, without re-rendering.
- `TOP_COL.dark` needs one entry per screen that has its own top colour (currently `up`, `locked`, `garden`, `book`).
  Add `croc`, `train`, `birds` if their top strip should match the scene.
- CSS: `html[data-theme="dark"]{ color-scheme:dark; ...tokens... }` then overrides grouped by screen.
- Offline: a service worker must cache nothing extra for dark mode. There are no new files.

## 5. Artwork rules

1. Image files (`animals/`, `fish/`, `avatars/`, `stars/`, `cookies/`, and the rest) are used as they are.
2. Buddy avatars stay on a light medallion (`#F3EADF`, a little dimmer than white). Their line art needs it.
3. Icons built in JS with a hardcoded brown stroke are recoloured in the dark block with attribute selectors, for example
   `html[data-theme="dark"] svg [stroke="#6B4A3A"]{stroke:var(--line)}`. This is how the prototype does it and it is
   safe. Cleaner, optional: change those strokes to `currentColor` in the JS.
4. The empty rainbow colour `#F3F9F9` is written by JS as an SVG attribute; the dark block overrides it the same way.
5. Counting objects on dark scenes get a thin light rim: `filter:drop-shadow(0 0 1.5px rgba(255,255,255,.8))`.
   Apply it once per loose object and once per group of 10 (the `.school`), never to each object inside a group.
   Done for fish. Likely needed for: birds and the wire, sheep strings, bead string, tower flag.
6. Existing brown drop shadows (`rgba(90,62,51,…)`, `rgba(71,28,14,…)`) are invisible on dark. Replace with
   `rgba(0,0,0,.35–.45)` only where the shadow carries meaning (a dragged object lifting). Otherwise leave them.
7. White sticker outlines (`.stk`, `.sticker-zoom .zoomed`) stay white: they are part of the sticker look.

## 6. Traps found in the code

- `--ink` is used as a **fill** for selected pills (`.seg`, `.tabs`, `.kpill.on`) with `color:#fff`. In dark mode the
  fill becomes cream, so the text must become `var(--on-ink)`. Search for `background:var(--ink)` before finishing.
- Literal `#fff` / `#FFFCF7` backgrounds (inputs, gate answers, number cards, train cards, write pad, bus signs) do not
  follow `--card`. Each needs a dark override. The full list of colour-bearing rules is about 245; most are covered by
  tokens, about 90 need a line in the dark block.
- `.count-tag` is brown with white text; in dark it flips to cream with dark text.
- The Write It canvas draws with `x.strokeStyle = '#5A3E33'`. On a dark pad this is invisible. Either keep the write pad
  light in dark mode (recommended: it is "paper", and the digit reader was trained on dark strokes on light) or read the
  ink colour from CSS. Do not change what the reader sees.
- The bus is drawn in CSS with `#5A3E33` outlines on a pale road. Keep the bus colours; darken only the road and sky.

## 7. Build tasks (each is independent unless noted)

Acceptance for every task: light mode pixel-identical; no page errors; text and countable objects clearly visible;
checked at 1180×820, 820×1180, 844×390 and 390×844 in dark mode; a full round played.

| # | Task | Notes | Model |
|---|---|---|---|
| 1 | Ten (chick): carton, eggs, tray, answer cards | egg number has a white text glow; keep | Haiku |
| 2 | Bus: road, stop sign, window numbers, rider chips | keep bus body colours | Haiku |
| 3 | Frog: pond, pads, arcs | pads keep their colours; pond goes dusk | Haiku |
| 4 | Tower: shelf, ruler, ghost block | ruler lines and marks | Haiku |
| 5 | Write It | keep pad light; see section 6 | Sonnet |
| 6 | Number Train | scrim is in; cards, slots, track | Haiku |
| 7 | Bead Necklace: tray, empty slots, string | string needs a lighter stroke | Haiku |
| 8 | Bird on a Wire | sky is in; wire `#4A4038` and poles need lightening; rim on birds | Sonnet |
| 9 | Market Day: labels, bins, selection glow | | Haiku |
| 10 | Up and Away | sky is in; clouds dimmer, hill darker, strings lighter | Sonnet |
| 11 | Start screen, name entry, buddy picker, add-a-child dialog, sticker book, sticker zoom, timer screen, update pill, rotate hints | sweep | Sonnet |
| 12 | Crocodile with 50 and 100 (schools, number cards, wrong-answer hint) | base is in | Haiku |
| 13 | Feed the Unicorn with 50 and 100 (boxes of 10, dashed ring) | base is in | Haiku |
| 14 | Final review on the real iPad at night; fish rim performance with 9 schools | after 1 to 13 | Fable |

Tasks 1 to 13 touch only the dark block, each in its own labelled section, so they can run in parallel and merge
without conflicts if each adds its section at the end of the block.
