# Installation

You can install `AIToolkit Base` and its dependencies using `pip`. We recommend using a virtual environment.

## Base Installation

For the core functionalities (excluding OCR and training-specific features), you can install the package directly from the root of the project directory:

```bash
# Navigate to the project root directory first
pip install .
```

This will install the base package with minimal dependencies, perfect for running most of the landmarking and detection examples.

## Optional Dependencies

The toolkit is designed to be modular, and some features require extra dependencies. You can install these "extras" as needed.

### Installing All Features

To install all features including OCR, deep learning models, and development tools, use the `[all,dev]` extra. This is the recommended way for developers.

```bash
# From the project root
pip install .[all,dev]
```

### Specific Features

If you only need specific functionalities, you can install them individually to keep your environment lean.

- **OCR and License Plate Recognition**: Requires `cnocr` and `torch`.
  ```bash
  pip install .[ocr]
  ```

- **Training & Advanced Models**: Requires `torch` and its ecosystem.
  ```bash
  pip install .[training]
  ```

- **For Generating Documentation**: If you want to build or serve the documentation locally, install the `doc` dependencies.
  ```bash
  pip install .[doc]
  ```

## Installing from GitHub (Future)

Once the project is hosted on GitHub, you will be able to install it directly from the repository.

```bash
# Example (once repository is public)
pip install git+https://github.com/your-username/aitoolkit_base.git
```

By following these instructions, you can set up an environment that is perfectly tailored to your needs. 