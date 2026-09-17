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
- **Pick up**: crouch and right-click with the wrench.

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
