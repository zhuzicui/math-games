# math-games · Feed the Monster

Learn to add with Momo the unicorn. Works on phones and iPads, in English, Français and 中文.

## What's in this folder

| File | What it's for |
|---|---|
| `index.html` | The whole app |
| `animals/`, `stars/` | Character and star artwork |
| `icons/apple-touch-icon.png` | iPhone / iPad home-screen icon (180×180) |
| `icons/icon-192.png`, `icons/icon-512.png` | Android / Chrome home-screen icons |
| `icons/icon-maskable-192.png`, `icons/icon-maskable-512.png` | Android adaptive icons (any shape mask) |
| `icons/icon-1024.png` | Master icon (App Store size, or for any other use) |
| `icons/favicon-16/32/48/96.png`, `favicon.ico` | Browser-tab icons |
| `manifest.webmanifest` | Tells phones the app's name, colours and icons |
| `og-image.png` | Preview picture when the link is shared (1200×630) |

## Put it online (any static host works)

1. This repo deploys straight from `main` on Vercel (no build step). Or upload the folder to any static host — e.g. **Netlify Drop** (drag the folder onto app.netlify.com/drop), **GitHub Pages**, **Cloudflare Pages** or **Vercel**.
2. Open the address on the phone or iPad.
3. **iPhone / iPad (Safari):** Share button → **Add to Home Screen**.
   **Android (Chrome):** ⋮ menu → **Add to Home screen** / **Install app**.

The icon shows Momo, the home-screen name is **Feed Momo**, and the app opens full-screen without browser bars.

## One small thing for link previews

`og:image` in `index.html` points to `og-image.png` with a relative path. Some apps (iMessage, WhatsApp, Slack) need a full address — once you know your site's URL, change it to e.g.
`<meta property="og:image" content="https://your-site.netlify.app/og-image.png">`.

## Notes

- Progress is saved in the browser on each device.
- Spoken instructions use the device's built-in voices. On iPad: Settings → Accessibility → Spoken Content → Voices to download "Enhanced" or "Premium" voices.
