# Momo Math

A gentle addition app for 4–6 year olds. Kids feed cookies to Momo the unicorn, fill an egg carton to make 10, and count snails on a bus. Mistakes aren't failures: Momo just counts with you, out loud.

**Try it:** https://math-games-neon.vercel.app (free, no account; add it to your home screen for a full-screen app)

<p align="center"><img src="docs/screenshots/hero.png" width="760" alt="Momo Math on iPad and iPhone"></p>

## What's inside

- **Three games**, each teaching a different addition idea
  - **Feed the Unicorn**: drag blue cookies onto a plate that already has red ones (adding two groups)
  - **Ten Frame**: fill the egg carton, then say how many eggs you added (making 10)
  - **Bus Stop**: some snails were on the bus, more got on; how many now? (counting on)
- **Colour coding everywhere**: red = what was already there, blue = what you add, matching the numbers in the sum
- **Kind feedback**: a wrong answer triggers counting together, never a buzzer
- **Rewards**: stars colour in rainbows; finished rainbows become stickers in a sticker book
- **Buddies**: kids pick one of 25 animal avatars
- **Voice in 6 languages**: English, Français, 普通话, 廣東話, 日本語, 한국어 (device voices, female or male)
- **For grown-ups** (behind a simple maths gate): a progress grid of every fact, a "try at home" tip, sums up to 5, 10, 15 or 20

## iPad

| Home | Feed the Unicorn | You did it! |
|---|---|---|
| <img src="docs/screenshots/ipad-03-home.png" width="270" alt="Home"> | <img src="docs/screenshots/ipad-04-feed.png" width="270" alt="Feed the Unicorn"> | <img src="docs/screenshots/ipad-05-bravo.png" width="270" alt="You did it!"> |

| Ten Frame | Bus Stop | Your rainbow |
|---|---|---|
| <img src="docs/screenshots/ipad-06-tenframe.png" width="270" alt="Ten Frame"> | <img src="docs/screenshots/ipad-07-bus.png" width="270" alt="Bus Stop"> | <img src="docs/screenshots/ipad-08-rainbow.png" width="270" alt="Your rainbow"> |

| Sticker book | Pick your buddy | For grown-ups |
|---|---|---|
| <img src="docs/screenshots/ipad-09-stickers.png" width="270" alt="Sticker book"> | <img src="docs/screenshots/ipad-02-buddy.png" width="270" alt="Pick your buddy"> | <img src="docs/screenshots/ipad-10-grownups.png" width="270" alt="For grown-ups"> |

## iPhone

| Name | Pick a buddy | Home | Feed the Unicorn | You did it! |
|---|---|---|---|---|
| <img src="docs/screenshots/phone-01-name.png" width="150" alt="Name"> | <img src="docs/screenshots/phone-02-buddy.png" width="150" alt="Pick a buddy"> | <img src="docs/screenshots/phone-03-home.png" width="150" alt="Home"> | <img src="docs/screenshots/phone-04-feed.png" width="150" alt="Feed the Unicorn"> | <img src="docs/screenshots/phone-05-bravo.png" width="150" alt="You did it!"> |

| Ten Frame | Bus Stop | Your rainbow | Sticker book | For grown-ups |
|---|---|---|---|---|
| <img src="docs/screenshots/phone-06-tenframe.png" width="150" alt="Ten Frame"> | <img src="docs/screenshots/phone-07-bus.png" width="150" alt="Bus Stop"> | <img src="docs/screenshots/phone-08-rainbow.png" width="150" alt="Your rainbow"> | <img src="docs/screenshots/phone-09-stickers.png" width="150" alt="Sticker book"> | <img src="docs/screenshots/phone-10-grownups.png" width="150" alt="For grown-ups"> |

## How it's built

A single `index.html` (plain HTML, CSS and JavaScript, no framework, no build step) plus artwork folders. Progress is saved in the browser's local storage on each device; nothing is sent anywhere.

| Path | What it's for |
|---|---|
| `index.html` | The whole app |
| `animals/`, `avatars/`, `stars/`, `cookies/`, `eggs/` | Characters, buddy faces, stars, cookies and eggs |
| `rainbows.js` | Rainbow stickers |
| `fonts/` | Fonts for Chinese, Cantonese, Japanese and Korean (only downloaded when used) |
| `icons/`, `favicon.ico`, `manifest.webmanifest` | Home-screen and browser icons, app name |
| `og-image.png` | Preview picture when the link is shared (1200×630) |
| `docs/screenshots/` | The pictures in this README |

## Put it online (any static host works)

1. This repo deploys straight from `main` on Vercel (no build step). Or upload the folder to any static host — e.g. **Netlify Drop** (drag the folder onto app.netlify.com/drop), **GitHub Pages**, **Cloudflare Pages** or **Vercel**.
2. Open the address on the phone or iPad.
3. **iPhone / iPad (Safari):** Share button → **Add to Home Screen**.
   **Android (Chrome):** ⋮ menu → **Add to Home screen** / **Install app**.

The icon shows Momo, the home-screen name is **Momo Math**, and the app opens full-screen without browser bars.

## Link previews

`og:image` points to `https://math-games-neon.vercel.app/og-image.png`. After changing the picture, bump the `?v=` number in `index.html` and re-scrape the link in Facebook's Sharing Debugger and LinkedIn's Post Inspector.

## Notes

- Progress is saved in the browser on each device.
- Spoken instructions use the device's built-in voices. On iPad: Settings → Accessibility → Spoken Content → Voices to download "Enhanced" or "Premium" voices.
