# Mewbile Tech

This repository contains a simplified phone management system used for an
educational assignment.  It simulates customers, phone lines and contracts and
provides a small visual interface for exploring call data.

## Project Structure

* `application.py` – loads call data, creates customers and starts the
  `Visualizer` interface.
* `bill.py`, `contract.py`, `phoneline.py`, `customer.py` – core logic for
  billing phone calls and tracking customer data.
* `call.py`, `callhistory.py` – represent individual calls and their histories.
* `filter.py` – classes used by the interface to filter calls by different
  criteria.
* `visualizer.py` – Pygame based tool for displaying calls on a map of Toronto.
* `sample_tests.py` – small test suite for selected functionality (requires
  `pytest` and the `pygame` package).

See [`ASSETS.md`](ASSETS.md) for details on the dataset and image files used by
this application.

## Running

1. Install the project dependencies, notably `pygame` and `pytest` for the test
   suite.
2. Run `python application.py` to launch the visual interface.
3. Sample tests can be executed with `pytest sample_tests.py`.
