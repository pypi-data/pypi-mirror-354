# doc-utils

This repository contains modular Python utilities and CLI scripts to help technical writers with documentation tasks.

**Purpose:**
Each script is now a thin CLI wrapper that delegates to reusable modules in the `doc_utils` package. For details on how to use a script, see the initial docstring, comments, or the corresponding Markdown help file.

## Current Scripts

- **check_scannability.py**  
  Checks the scannability of AsciiDoc (`.adoc`) files in the current directory. Reports sentences that are too long and paragraphs that contain too many sentences, based on configurable limits. See [check_scannability.md](check_scannability.md) for usage and examples.

- **archive_unused_files.py**  
  Scans `./modules` and `./assemblies` for AsciiDoc files not referenced by any other AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_files.md](archive_unused_files.md) for usage and examples.

- **archive_unused_images.py**  
  Scans all directories for image files (e.g., `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`) not referenced by any AsciiDoc file in the project. Optionally archives and deletes them. See [archive_unused_images.md](archive_unused_images.md) for usage and examples.

- **find_unused_attributes.py**  
  Scans a user-specified attributes file (e.g., `attributes.adoc`) for attribute definitions (e.g., `:version:`) and recursively scans all `.adoc` files in the current directory for usages (e.g., `{version}`). Reports any attribute that is defined but not used in any `.adoc` file as **NOT USED** in both the command line output and a timestamped output file. See [find_unused_attributes.md](find_unused_attributes.md) for usage and examples.

## Modular Python Package

The core logic for all scripts is implemented in the `doc_utils/` package. You can import and reuse these utilities in your own scripts or tests:

- `doc_utils.file_utils` — file collection, manifest, and archiving utilities
- `doc_utils.unused_images` — logic for finding and archiving unused images
- `doc_utils.unused_adoc` — logic for finding and archiving unused AsciiDoc files
- `doc_utils.scannability` — logic for checking AsciiDoc scannability
- `doc_utils.unused_attributes` — logic for finding unused AsciiDoc attributes

## How to Use

1. Open the script you are interested in (for example, `check_scannability.py` or `find_unused_attributes.py`).
2. Read the top of the script or the corresponding `.md` file for instructions, options, and examples.
3. Run the script from your terminal as described in the usage section.

## Running Tests

To run all tests, install the development requirements and run pytest from the project root:

```sh
pip install -r requirements-dev.txt
pytest
```

All tests and fixtures are located in the `tests/` directory. See `tests/README.md` for details.

---

*For licensing information, see [LICENSE](LICENSE).*
