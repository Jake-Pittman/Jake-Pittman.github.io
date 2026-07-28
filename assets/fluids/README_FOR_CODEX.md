# Fluids website asset kit

## Core brand
- **Positioning:** Lab-informed whole-food drink mix
- **Primary line:** Nutrition, calibrated.
- **Secondary line:** Your labs. Your blend.
- **Blend:** Raspberry Lemonade
- **Ingredients:** Raspberry, carrot, lemon, coconut water, and lime

## Start with these files
1. `fluids_logo_primary_transparent.png` — light backgrounds.
2. `fluids_logo_reverse_transparent.png` — dark backgrounds.
3. `fluids_box_3d_transparent.png` — product detail and purchase sections.
4. `fluids_stick_pack_transparent.png` — product cards and mobile layouts.
5. `fluids_product_family_transparent.png` — transparent hero composition.
6. `fluids_product_hero_porcelain.png` — complete no-text hero background.
7. `fluids_pouch_pouring_into_water_4x5.png` — product-use/lifestyle section.
8. `fluids_nutrient_matrix_orb_transparent.png` — science and personalization sections.
9. `fluids_nutrient_profile.json` — structured nutrient data for live UI.
10. `fluids_brand_tokens.css` — initial CSS variables.

## Implementation notes for Codex
- Keep headlines and body copy as live HTML. Do not rely on text embedded in reference/mockup images.
- Transparent product files are high-resolution PNGs and can be positioned with CSS over Porcelain (`#F8F4ED`) or white.
- Use the product-family PNG with `object-fit: contain`; avoid cropping the package edges.
- Use the 4:5 lifestyle files inside portrait cards or editorial sections.
- Render the nutrient profile dynamically from `fluids_nutrient_profile.json`; the chart PNG is a visual reference.
- Use the matrix orb as a reusable accent behind cards, between sections, or as a subtle parallax element.
- Suggested display font: Didot/Bodoni-style high-contrast serif.
- Suggested body font: Inter.
- The packaging and UI images are concept assets. Final commercial packaging copy, supplement facts, regulatory language, and weights should be reviewed before production.

## Suggested responsive image widths
- Logo: 240–520 CSS px
- Box: 420–760 CSS px
- Stick pack: 150–320 CSS px
- Product family: 760–1280 CSS px
- Matrix orb: 260–620 CSS px
- Lifestyle portrait: 420–700 CSS px
