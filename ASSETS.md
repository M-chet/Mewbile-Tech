# Data and Image Assets

This project expects several external files located inside the `data/` directory.

## Dataset

- `dataset.json` – the main data set used by `application.py`. It contains
  customer information and a chronological list of call and SMS events. The file
  is large and stored as a single JSON object.

## Images

The visualizer relies on a few PNG images to render calls on the map:

- `call-start.png` and `call-start-2.png` – icons for the origin of a call.
- `call-end.png` and `call-end-2.png` – icons for the destination of a call.
- `toronto_map.png` – background map used by the visualizer.

Make sure these files remain in the `data/` folder so that the paths inside the
source code resolve correctly.
