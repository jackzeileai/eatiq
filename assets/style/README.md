# Meal Pic style pack — "Mono"

One stylesheet for every Meal Pic web page: `assets/style/mono.css`.
The thesis: **black and white. The pictures are the colour.**

References: shopify.design (giant black grotesk, white space, mono labels, image masonry) and the "ripped off by filthy marketing scum bags" memoji ad (huge heavy headline, one grey wedge, colour only from the memoji).

## The rules

1. **Page is white. Type is black.** Secondary text is one grey (`--sub`). No coloured headings, numbers, icons, badges, links or buttons.
2. **Colour comes only from pictures**: food photos, app screenshots, UI mockups, memoji, video. If something needs colour, make it a picture.
3. **One grey, one job.** `--stage` (#f2f2f2) is a stage behind pictures and UI mockups. Never put a block of text on it.
4. **One button.** Black pill, white text (`.btn`). Secondary is the same pill in white with a hairline (`.btn.ghost`). Big page-wide CTA is `.btn.bar`.
5. **One typeface, used big.** Inter. Headlines are heavy (800) and tight (-.04em to -.05em), and bigger than feels safe. Body is 17px medium.
6. **Mono labels for structure.** Tiny uppercase monospace labels with a hairline rule (`.rule` + `.label`) replace coloured eyebrows, pills and icons.
7. **Hairlines, not shadows.** Cards get a 1px hairline (`.card`). Only UI mockups sitting on a stage get a soft shadow (`.ui`).
8. **No gradients, no washes, no glows, no emoji in UI.**
9. **Short copy.** One line per section subhead, one sentence per card.
10. **Don't add page CSS to change the look.** Change the pack. Page CSS is for layout only.

## Primitives

| Class | What |
|---|---|
| `.wrap` | centred column, 1200px, 24px gutters (16px on phones) |
| `.sec` | section spacing (112px top, 72px on phones) |
| `.grid.c2` / `.grid.c3` | 16px-gap grids, stack under 980px |
| `.split` | headline left, lede right |
| `.h-hero` `.h1` `.h2` `.h3` | heavy black headlines, fluid sizes |
| `.lede` `.p` `.small` | body sizes |
| `.label` (+`.dim`, `.dot`) and `.rule` | mono labels and the hairline rule line |
| `.btn` `.btn.ghost` `.btn.small` `.btn.circle` `.btn.bar` | the button |
| `.stage` | grey stage for a picture or mockup |
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
