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
with the protocol nested inside. The body is his project `devtools/art/preview/pickup.bbmodel`;
everything shipped is written from it by `devtools/art/build.py`, his build ported. The
repo is `minecraft-farmers-truck`, Rusty's name for it.

## Shape

No Java in the mod. `gametest` is a mod of its own: seven gametests and a photo booth,
the Trailblazer's adapted. The pipeline wraps cubes into the profile's folders, greys the
painted texels so the factory red is the profile's and a dye replaces it, duplicates the
tailgate's shared atlas patches first (door meshes are drawn untinted), raises the fuel
needle onto its pivot, and measures the profile off the cubes.

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
