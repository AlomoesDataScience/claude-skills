# Sprite Studio for Windows (demo)

A local sprite editor for Dominions 6 mods. Build a unit from simple 3D shapes, pose it,
recolour it, and render it straight to a Dominions-ready TGA: black is transparent,
magenta is the shadow, the unit faces left, and there are two free rows under the feet.
You can also import an existing sprite and edit it in 2D, or turn it into a posable 3D
model.

This is a **demo release**. Expect rough edges, and keep backups of sprites you care
about.

## What you need

- **Windows 10 or 11, 64-bit.**
- A web browser. The editor runs on your own computer and needs no internet.
- Nothing to install: Python and Pillow come inside the `python` folder.

## Start

1. Unzip the whole folder. The best place is **inside your Dominions mods folder**,
   because **Export** copies sprites into folders next to Sprite Studio's own folder.
   Don't run it from inside the zip.
2. Double-click **`Sprite Studio.bat`**. A black window flashes for a moment, then the editor
   opens in your browser.

**Quit** (top right) stops it. It also stops by itself about 3 minutes after you close
the tab.

Your projects are saved in `models\` and your renders in `output\`, both in this folder.
The demo starts with one example model, the killbot.

If Windows SmartScreen warns about the file, choose **More info → Run anyway**. The demo
is not signed.

## What you can do

- **3D models:** add and reshape parts, pose them with handles, and recolour them. There
  are three looks: shiny metal, cel-shaded paint, and pixel wireframe.
- **Frames:** an idle and an attack frame, rendered as `<name>1.tga` and `<name>2.tga`.
- **Import** a TGA or PNG sprite:
  - edit it in 2D: cut it into pieces, pose them, paint pixels, and use layers;
  - or convert it to 3D blocks that you can turn and pose.
- **Canvas sizes** that Dominions accepts (8 to 128 px; 64 for humans, 128 for big units),
  with the shadow and ground row handled for you.
- **Export** copies the finished TGAs into your mod's folder.

The full manual is in **MANUAL.md**.

## Known limits of the demo

- Rendering runs on your CPU. A 64×64 unit takes a few seconds; a big converted sprite
  can take 15 to 30 seconds per frame.
- Sprites are not checked inside the game. Look at them in Dominions before you ship a mod.
- If something goes wrong, details are written to `sprite-studio.log` in this folder.
