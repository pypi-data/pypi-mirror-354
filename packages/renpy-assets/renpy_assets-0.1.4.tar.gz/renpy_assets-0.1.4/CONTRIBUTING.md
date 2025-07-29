# Contributing to renpy-assets

Thanks for your interest in contributing!
This project aims to provide Ren'Py developers with powerful CLI tooling for working with assets.

---

## How to Contribute

1. **Fork this repository**

2. **Clone your fork**

   ```bash
   git clone https://github.com/jeje1197/renpy-assets
   cd renpy-assets
   ```

3. **Install dependencies**

   ```bash
   pip install -e .[dev]
   ```

4. **Make your changes**
   Add new features or bug fixes in `renpy_assets`.

5. **Write tests**
   Add test cases under `tests/` for any new behavior.

6. **Run tests**

   ```bash
   pytest
   ```

7. **Submit a pull request**

---

## Code Structure

* `cli.py` – Typer app entry point
* `commands/` – Individual command logic (e.g. `scan`, `generate`)
* `utils/` – File pattern matching, reusable helpers
* `tests/` – Unit tests

---

## Code Style

* Use `black` for formatting
* Use `pytest` for all testing
* Keep CLI output clean and informative

---

## Ideas to Contribute

* Add support for other Ren'Py assets (movies, live2D, etc)
* Autogenerate label or character definitions
* Export declarations to `.rpy` files directly
* VS Code extension integration
