# Farmer's Pickup

A two-seat farm truck for [Vanilla Wheels](https://github.com/the-rusty-shackleford/minecraft-vanilla-wheels)
on NeoForge 1.21.1, built by nfx: a red single-cab pickup with a working tailgate, two
chests in the bed, a dash with a speedometer and a fuel gauge, headlights, a horn, a radio and a
hitch for a [trailer](https://github.com/the-rusty-shackleford/minecraft-trailer). There is
no Java in it: the truck is a vehicle profile and two Blockbench meshes, and the protocol
does the rest, so driving, fuel, storage, towing and the lift are documented there.

## Getting one

- **Chassis**: eight iron blocks round a hay bale.
- **Build**: the chassis, four wheels and an engine in a Mechanic Lift, and Build. Paint it
  there with a dye; it is red to begin with, and a dye replaces the red, the tailgate's
  panels included.
- **Pick up**: punch it six times in a row and it packs into your inventory as it is, cargo,
  fuel and wear included; a truck paired to a key packs only for its owner (Vanilla Wheels 1.10.0, its D-0025).
- **Repair by hand**: right-click it damaged and it is repaired 2.5% a click for hunger, no
  materials; a full rebuild from a wreck costs 4.5 food points (2¼ drumsticks). Whole, the click does what it
  always did (D-0025).
- **Durability 8** (Vanilla Wheels 1.14.0, its D-0034): a blow wears the truck an eighth of what it
  wears a boat; seven pistol rounds, four rifle rounds, two shotgun shells or two rockets wreck it.
  Needs Vanilla Wheels 1.14.0, which it nests.

## Driving it

Right-click to board (the driver's seat first); movement keys drive, jump held in a turn
drifts, Left Control honks, H cycles the headlights. Look down from the driver's seat and
the two dials on the dash read your speed and your tank. Crouch and right-click the
tailgate, empty-handed, anywhere on it, to drop or raise it.
Right-click either of the two chests in the bed to open it, or press the inventory key
while riding for the left one.
Crouch and right-click with a music disc to play it; crouch and right-click the dash
empty-handed to eject it. Hold a trailer and right-click the truck to hitch it behind, or
back the rear hitch onto a loose trailer's tongue.

Numbers: the Trailblazer's -- top speed 0.9 blocks a tick, mass 1.45, climb 1 block, 32
degrees of lock; six and a half blocks long, two and a half wide, three high.

## How it is made

`devtools/art/preview/pickup.bbmodel` is an approved cosmetic derivative of nfx's
Blockbench project. The original is preserved in `devtools/art/reference/`, with its
attribution and checksums. Shaped bonnet and roof corners, continuous painted arch shells with dark trim, recessed rims, lamp bezels, a layered grille and tucked bumpers.

Edit the Blockbench source, then run `devtools/art/build.py --appearance-only`.
It exports only the body and wheel meshes, supports cube and polygon faces, and refuses
to run if the vehicle profile differs from the frozen released contract. It does not
derive gameplay from the reshaped art or rewrite the profile, recipes or language files.
The importer retains the existing paint wrappers, greys the paint swatches, separates shared tailgate UVs, centres the gauges and lifts the fuel needle onto its original pivot.

See D-0002 for the art direction and gameplay boundary. The cosmetic changes in 1.3.0 do not change the driving, interactions or construction described above.

## Verifying it

```
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 PATH="$JAVA_HOME/bin:$PATH"
uv run --no-project python devtools/art/build.py --appearance-only
uv run --no-project --with pillow python -m unittest discover -s devtools/art -p "test_appearance.py"
./gradlew check                                       # gametests and the photo booth (needs a display)
```

Seven gametests on a headless server: the profile is registered as described (two seats,
a tailgate, two chests of six rows, four wheels, two gauges, a hitch, a radio, headlights); the truck
reaches speed and climbs a one-block step, and a two-block ledge holds it level; runs a
cow over for the damage its mass and speed say; takes the gas can; crafts its chassis; takes and
ejects a disc. The booth photographs the truck's side red and painted light blue, the
tailgate dropped, the view from the driver's seat ahead and down at the dash at speed on
half a tank, the third-person views, and the lamps at night; its `booth: PASS/FAIL` lines
are the assertion. For server-only checks, run
`./gradlew --no-watch-fs check -PskipBooth`. For the shader booth, use a native GPU display
with Iris, Sodium and Complementary in `run/booth/`. Verify host clients and Xephyr first,
reuse the existing display, and run only one rendering client. The booth mutes itself and exits.

The paint check includes shaded red under Complementary, using the light-blue repaint
as its negative control; dashboard needles retain a separate brightness check.

## Release 1.3.0

The approved cosmetic derivative ships with Vanilla Wheels 1.7.0 and Luminance 1.1.0. Vehicle gameplay data and original supplied-model references are preserved. Update every client and the server together for network protocol 4.

## Licence

AGPL-3.0-or-later. Copyright 2026 Rusty Shackleford and nfx.

## Shared materials dependency

Version 1.3.1 bundles Vanilla Wheels 1.7.2, which requires Metals and Materials
as a separately installed mod on both client and server. Mod Hub includes it
in our pack. Vehicle profiles, models, recipes and handling are unchanged.

## Repairs and recovery (1.4.0)

Broken vehicles become packed items at zero condition, preserving cargo, paint,
fuel and radio discs. Packing it up with punches also preserves cargo and wear; a punch is a knock, not wear.
Repair it by hand (above), or place a damaged vehicle on the Mechanic Lift to reveal Repair; a full repair costs **18 iron
ingots**, with cheaper proportional repairs rounded up. Creative needs no materials.

Use a Vehicle Key Fob on a motor vehicle to pair it. Hold use in air to preview the
fuel bill and recall it together with its currently hitched trailer. The farther
it is, the higher the bill (5% of a full tank at 1,000 blocks; 20% at 2,000).
Missing fuel becomes half as much condition loss. Cargo stays intact even if recall
returns a wreck. Unload passengers and animals, close vehicle chests, and leave room
in inventory. One key per vehicle, named for it and banded in its paint, and a paired key
never leaves its owner (Vanilla Wheels D-0026); a blank key used in the air replaces one
that is gone, and the lost one stops working.
The fob can recover a paired physical wreck, including from an unloaded chunk, but
cannot duplicate an item someone already collected. A trailer detached by breaking
or packing up is a separate vehicle.

Requires matching Vanilla Wheels 1.8.0 / protocol 5 on client and server.
Update the full pack on both sides before connecting.
