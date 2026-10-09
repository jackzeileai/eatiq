# Meal Pic style pack — "Mono"

One stylesheet for every Meal Pic web page: `assets/style/mono.css`.
The thesis: **black and white. The pictures are the colour.**

## Hallmarks (Jack's words)

- A white or black background.
- Bold text, very Apple-like. **Text is often too thin — err heavier.**
- Incredibly concise and simple.
- Bold pictures do the talking, with colour.
- Liquid glass as much as possible. It's iOS-based, Apple-based.

References: shopify.design (giant black grotesk, white space, mono labels, image masonry); the "ripped off by filthy marketing scum bags" memoji ad (huge heavy headline, one grey wedge, colour only from the memoji); Apple product pages — iPhone Duo on white, iPhone 17 Pro and Watch Ultra on black (centred words, two pills, one giant 3D object does the talking); Partiful and Corner (black UI, chrome 3D logo, memoji and emoji as the colour); X Money, Slash, Serus (plain type, one product shot); UglyCash (giant condensed black headline, white page, phone + sticker pile as the colour, three light tiles with a bold caption under each); Shopify's giant "26" with 3D objects floating around the numeral, and its huge type with tiny mono place labels.

## The rules

1. **Page is white or black. Type is the opposite.** Secondary text is one grey (`--sub`). No coloured headings, numbers, icons, badges, links or buttons. Dark is the same pack inverted: `data-theme="dark"` on `<html>` or `.dark` on a section.
2. **Colour comes only from pictures**: food photos, app screenshots, UI mockups, 3D renders, memoji, big emoji, video. If something needs colour, make it a picture.
3. **One picture does the talking.** The hero is words, two pills, then one big object (`.hero-apple`). Not a collage, not a wall.
4. **No grey fills.** Tiles and stages are white with a hairline (or pure black on dark). Jack: "I hate the grey fill." Grey exists only as secondary text.
5. **One button, Apple's.** 56px pill, 18px medium text, roomy padding. Black on white, white on black (`.btn`). Secondary is the same pill outlined 1.5px with no fill (`.btn.ghost`). Big page-wide CTA is `.btn.bar`.
6. **One typeface, used big and heavy.** Inter. Headlines 800 and tight (-.04em to -.05em), bigger than feels safe. Body is 17px semibold (600). If it looks thin, it is thin: go up a weight.
7. **Small bold labels for structure.** Tiny uppercase Inter labels (800, letter-spaced) with a hairline rule (`.rule` + `.label`) replace coloured eyebrows, pills and icons. Not monospace — Jack said it felt off-brand.
8. **Hairlines, not shadows.** Cards get a 1px hairline (`.card`). Only UI mockups and 3D objects get a soft shadow (`.ui`, `.object3d`).
8b. **Liquid glass for anything that floats**: the nav, sticky bars, chips sitting on pictures, sheets (`.glass`). Translucent, blurred, bright inner edge.
9. **No gradients, no washes, no glows.** Emoji and memoji are welcome, but only big, as the picture (`.emoji`), never as bullet decoration next to text.
10. **Short copy.** One line per section subhead, one sentence per card.
11. **Don't add page CSS to change the look.** Change the pack. Page CSS is for layout only.

## Primitives

| Class | What |
|---|---|
| `.wrap` | centred column, 1200px, 24px gutters (16px on phones) |
| `.sec` | section spacing (112px top, 72px on phones) |
| `.grid.c2` / `.grid.c3` | 16px-gap grids, stack under 980px |
| `.split` | headline left, lede right |
| `.h-hero` `.h1` `.h2` `.h3` | heavy black headlines, fluid sizes |
| `.lede` `.p` `.small` `.meta` | body sizes; `.meta` is the small fact line under a hero |
| `.hero-apple` + `.object` | centred words, two pills, one big picture |
| `.emoji` (+`.xl`), `.object3d` | big emoji / memoji / 3D render used as the picture |
| `[data-theme="dark"]` / `.dark` | the inverted pack |
| `.glass` (+`.card`), `.btn.glass`, `.nav.float` | liquid glass surfaces, floating glass nav pill |
| `.label` (+`.dim`, `.dot`) and `.rule` | mono labels and the hairline rule line |
| `.btn` `.btn.ghost` `.btn.small` `.btn.circle` `.btn.bar` | the button |
| `.stage` (+`.dark`) | white hairline tile for a picture; `.dark` for a black one |
| `.pic` | rounded image |
| `.card` | hairline card (white) |
| `.ui` | white UI mockup with soft shadow, for use on a stage |
| `.nav` `.brand` `.links` | sticky white nav |
| `.faq` | hairline accordion |
| `footer.site` | hairline footer |

## Using it

```html
<link rel="stylesheet" href="/assets/style/mono.css">
```

Pages that use it: `/join` (creator landing). Next: `/dashboard`, `/home`, `/c/`.

## Before every edit (read this, then edit)

1. Re-read the rules above. An edit never lowers a weight, adds a colour, or adds a second grey.
2. Pictures: one render per spot, never the same render twice on one screen.
3. Floating objects live in the margins, outside the text column, never over words or buttons.
4. Keep the layout Jack approved (hero: words left, one-slider calculator right, three tiles under). Change the content, not the structure, unless he asks.
5. Screenshot desktop and phone after every change and look at it before pushing.

## The house moves (Jack-approved, 2026-10-09)

- **Giant headline with 3D objects floating around the edges** and a floating glass nav pill (lab C hero). Objects sit in the margins, never over the words.
- **Three white tiles, one 3D object each**, bold caption, grey one-liner (lab B tiles).
- **3D clay illustration style** for objects: soft matte, saturated props, white or black background, generated per section (never reuse one render twice on a page).
- **People are Apple Memoji, not Bitmoji.** Jack: "I like memojis, not bitmojis." Memoji = Apple's Animoji look: oversized head, smooth glossy skin, simple dot-like features, little or no body. Not the Pixar / Snapchat Bitmoji cartoon kid with a full body and detailed clothes. Exception: Jack prefers the original blue-hoodie ring-light guy (`memoji_ringlight_white_t.png`) over the Memoji redo, so keep him.

- **Headline is all black.** Jack hated the grey second line ("I hate this gray"). Each sentence on its own line, sized so it fits; don't make it wall-sized. Grey never goes in headlines.
- **Nav type:** wordmark 800 with "Creators" the same weight in grey; links 600 solid black (hover goes grey); Join 600.

## Render prompt (Jack's winner)

`Pure white background. 3D render in the style of Apple's mobile phone emoji: <THING>. Soft shadow below. No text.` — Higgsfield GPT Image 2.5, 1:1. Then Higgsfield remove_background for the cutout. Winners: `cash100_t.png`, `iphone_color_t.png`.

## Moves worth stealing

- A giant number or word as the graphic, with a few 3D objects / emoji floating around it (Shopify "26").
- Three white hairline tiles in a row, each holding one 3D object, bold caption and two short lines under each (UglyCash, our `.tile`).
- Tiny bold labels hanging off huge type (Shopify "Toronto — ONTARIO, CANADA").
- Words, two pills, one object (Apple).

## Logo

Use the line mark (`assets/mark-black.png`, `mark-white.png` on dark) next to the wordmark in navs. Not the rounded app-icon square. Jack: "I like this logo way more."
