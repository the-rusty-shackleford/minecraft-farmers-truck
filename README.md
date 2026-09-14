# Farmer's Pickup

A two-seat farm truck for [Vanilla Wheels](https://github.com/the-rusty-shackleford/minecraft-vanilla-wheels)
on NeoForge 1.21.1, built by nfx: a red single-cab pickup with a working tailgate, a chest
in the bed, a dash with a speedometer and a fuel gauge, headlights, a horn, a radio and a
hitch for a [trailer](https://github.com/the-rusty-shackleford/minecraft-trailer). There is
no Java in it: the truck is a vehicle profile and two Blockbench meshes, and the protocol
does the rest, so driving, fuel, storage, towing and the lift are documented there.

## Getting one

- **Chassis**: eight iron blocks round a hay bale.
- **Build**: the chassis, four wheels and an engine in a Mechanic Lift, and Build. Paint it
  there with a dye; it is red to begin with, and a dye replaces the red -- except on the
  tailgate, which keeps it.
- **Pick up**: crouch and right-click with the wrench.

## Driving it

Right-click to board (the driver's seat first); movement keys drive, jump held in a turn
drifts, Left Control honks, H cycles the headlights. Look down from the driver's seat and
the two dials on the dash read your speed and your tank. Crouch and right-click the
tailgate, empty-handed, within a block and a half of its hinge to drop or raise it.
Right-click the bed for the chest (crouching), or press the inventory key while riding.
Crouch and right-click with a music disc to play it; crouch and right-click the dash
empty-handed to eject it. Hold a trailer and right-click the truck to hitch it behind, or
back the rear hitch onto a loose trailer's tongue.

Numbers: the Trailblazer's -- top speed 0.9 blocks a tick, mass 1.45, climb 1 block, 32
degrees of lock; six and a half blocks long, two and a half wide, three high.

## How it is made

The truck is nfx's Blockbench project, `devtools/art/preview/pickup.bbmodel`, as saved;
`devtools/art/build.py` (his build, ported) turns it into what the protocol reads. The
model was rigged with its own folder names, so the build wraps cubes into the folders the
profile's selectors name: `lenses` for the headlights, `glass` for the windshield and the
cab's rear pane, and a `paint` folder inside the bed, cab, doors, windshield and front
holding every red panel. Paint in Vanilla Wheels is a vertex-colour multiply, and this
model bakes its red in, so the build greys the red texels of the painted faces to the same
brightness and the profile's `factory` colour (the model's own red) restores the look; a
dye then replaces the red instead of multiplying with it. The tailgate is a door and door
meshes are drawn untinted, so it keeps its baked red; its atlas patches, shared with the
bed's sides and rails, are duplicated first so the greying does not reach it. The fuel
needle is raised so its base sits on the dial's centre, the gauge's pivot. The profile is
measured off the cubes the way the Trailblazer's is: the seats four tenths of a unit over
the cushion, the wheels off `wheel_0_left`'s axle, the hit boxes fender-wide at each axle,
the body cab-wide and bumper to hitch, the lamps half a unit ahead of the lenses, the
hitch ball's rear face, the bed's front wall for the chest region, the tailgate's hinge
off its folder's pivot with a quarter turn about +X. Units are sixteenths of a block.

## Verifying it

```
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 PATH="$JAVA_HOME/bin:$PATH"
uv run --no-project python devtools/art/build.py     # split the project and write the profile
./gradlew check                                       # gametests and the photo booth (needs a display)
```

Seven gametests on a headless server: the profile is registered as described (two seats,
a tailgate, six rows, four wheels, two gauges, a hitch, a radio, headlights); the truck
reaches speed and climbs a one-block step, and a two-block ledge holds it level; runs a
cow over for the damage its mass and speed say; takes coal; crafts its chassis; takes and
ejects a disc. The booth photographs the truck's side red and painted light blue, the
tailgate dropped, the view from the driver's seat ahead and down at the dash at speed on
half a tank, the third-person views, and the lamps at night; its `booth: PASS/FAIL` lines
are the assertion. Headless: `Xephyr :7 -screen 1280x720 -ac -br -noreset`, then
`DISPLAY=:7 __GLX_VENDOR_LIBRARY_NAME=mesa LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe
MESA_GL_VERSION_OVERRIDE=4.6 MESA_GLSL_VERSION_OVERRIDE=460 ./gradlew check`.

## Licence

AGPL-3.0-or-later. Copyright 2026 Rusty Shackleford and nfx.
