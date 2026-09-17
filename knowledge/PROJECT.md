---
title: Farmer's Pickup — project
type: overview
layer: store
tags: [overview]
---

# Farmer's Pickup

## What this is

The third vehicle for Vanilla Wheels: nfx's two-seat farm truck, a data-only NeoForge
1.21.1 mod (`lowcodefml`, mod id `farmpickup`, vehicle `farmpickup:pickup`, the ids his
instance already runs) holding a profile, two Blockbench meshes, a recipe and a lang file,
with the protocol nested inside. The body is a deliberate derivative of his project `devtools/art/preview/pickup.bbmodel`;
the two meshes are exported from it by `devtools/art/build.py`, his build ported. The
repo is `minecraft-farmers-truck`, Rusty's name for it.

## Shape

No Java in the shipped mod. The separate gametest source set contains the real-server
checks and client booth. `build.py --appearance-only` splits the Blockbench source,
preserves selector/animation structure and uses the frozen released gameplay profile.
It does not write gameplay or language data. Original source and profile references,
with attribution, are kept under `devtools/art/reference/` (D-0002).

## How it is verified

`./gradlew check`: seven gametests (profile, the one-block step and the two-block wall,
running a cow over, the gas can, the chassis recipe, the radio) and the booth (side red and
dyed blue, the tailgate dropped, the dash from the seat at speed, the quarters, the lamps
at night).

## Decisions

D-0001: the truck is nfx's project under his ids; the build is his, ported.

## Next

1.1.0 (2026-09-13): the first release from this repo, past the 1.0.x nfx shipped to his
instance, on Vanilla Wheels 1.5.0, with the gauges moved to the centre of the console (the
wheel's rim hid them; Rusty) and the tailgate's panels painted, since the protocol now dyes
a door's painted part. Then into the pack.


## Release approval - 2026-09-16

Rusty approved the final review, completing their earlier conditional release go.
Version 1.2.0 was published on 2026-09-16 and deployed in pack 1.35.1
after the clean release build and asset verification. The deployed server matched
the published pack and ran at 20 TPS. This supersedes the earlier release holds
and pending presentation/listening review recorded above.

## Cosmetic work — held, 2026-09-17

D-0002 records Rusty's approved art direction and intentionally edited derivative.
Shaped bonnet and roof corners, continuous painted arch shells with dark trim, recessed rims, lamp bezels, a layered grille and tucked bumpers. Gameplay remains frozen to v1.2.0. New releases remain HELD.
Independent driver/observer multiplayer checks, the historical movement-warning route,
and representative 4–8-player capacity, distant tracking and DH load remain open;
local booths and isolated frame timings do not close them.

## Release authorization — 2026-09-17

Rusty approved the final vehicle cosmetics, then explicitly requested the release.
Version 1.3.0 is the coordinated release version, superseding the prior hold.
The release set is Luminance 1.1.0, Vanilla Wheels 1.7.0 (network protocol 4),
Trailblazer 1.7.0, Farmer's Pickup 1.3.0 and Trailer 2.3.0, targeting pack 1.36.0.
All peers must update together. Vehicle artwork changes leave the existing gameplay
profiles, recipes, seats and interaction anchors unchanged; the separately approved
collision and moving-light changes ship in the shared libraries.

Independent driver/observer multiplayer, the historical live movement-warning route,
and representative 4–8-player tracking/DH capacity remain open follow-ups. Local tests
do not establish those results. Release authorization does not claim those checks passed.
