# Cosmetic reference inputs

The original source is nfx's Blockbench project from `v1.2.0`, preserved byte for byte.
Copyright 2026 Rusty Shackleford and nfx; AGPL-3.0-or-later.

- `pickup-before-cosmetics.bbmodel` SHA-256: `746bc70a9bcf43b2adcd03acb3dee71be59004afd191aa45a4836629b0f8cd2c`
- `released-profile.json` SHA-256: `7a5e16a636c7ec00a430584fe2cdb077343da1b9bddad6440865733beb698efb`

`../preview/pickup.bbmodel` is the intentional cosmetic derivative approved by Rusty
on 2026-09-16. It is not a verbatim collaborator delivery. See D-0002.
Automobility 0.5.0.h's steel motorcar supplied a finish reference; none of its geometry
or textures are included in this derivative.

The profile is a frozen comparison input. The importer checks it before exporting
meshes and never rewrites gameplay data. Review a future gameplay change separately;
do not regenerate or refresh this reference merely to bypass that guard.
