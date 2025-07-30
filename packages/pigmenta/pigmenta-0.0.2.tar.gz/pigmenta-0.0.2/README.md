### 📘 pigmenta

- **Version**: `0.0.2`
- **License**: [`MIT`](/LICENSE)
- **Author**: `Crispen Gari`
- **Python Compatibility**: Python `3.9+`

<p align="center">
  <img src="/images/logo.png" alt="logo" width="200">
</p>

<p align="center">
  <a href="https://pypi.python.org/pypi/pigmenta"><img src="https://badge.fury.io/py/pigmenta.svg"></a>
  <a href="https://github.com/crispengari/pigmenta/actions/workflows/ci.yml"><img src="https://github.com/crispengari/pigmenta/actions/workflows/ci.yml/badge.svg"></a>
  <a href="/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="https://pypi.python.org/pypi/pigmenta"><img src="https://img.shields.io/pypi/pyversions/pigmenta.svg"></a>
</p>

### Table of Contents

- [📘 pigmenta](#-pigmenta)
- [Table of Contents](#table-of-contents)
- [🌈 Overview](#-overview)
- [🚀 Features](#-features)
- [📦 Installation](#-installation)
- [🧪 Usage](#-usage)
  - [Example with Matplotlib](#example-with-matplotlib)
  - [🎨 Available Palettes](#-available-palettes)
- [🛠️ Custom Palettes](#️-custom-palettes)
- [💡 Use Cases](#-use-cases)
- [🧩 Future Plans](#-future-plans)
- [📬 Contributing](#-contributing)
- [📝 License](#-license)

### 🌈 Overview

`pigmenta` is a lightweight Python package that provides easy access to a curated collection of beautiful color palettes. It is designed for developers, designers, data scientists, and artists who want to use harmonious and theme-based color palettes in visualizations, UI design, machine learning plots, or generative art.

### 🚀 Features

- Access over 30 named color palettes.
- Themes include: `pastel`, `vintage`, `neon`, `sunset`, `earth`, `skin`, `space`, and more.
- Easy integration with libraries like Matplotlib, Seaborn, Plotly, or your own app.
- Simple API via a class or dictionary.
- Extensible and open-source.

### 📦 Installation

```bash
pip install pigmenta
```

> _Note: You can install it directly from a GitHub repo:_

```bash
pip install git+https://github.com/yourusername/pigmenta.git
```

### 🧪 Usage

First you need to start by importing the package.

```python
from pigmenta import PALETTES
```

You can access the color pallets as follows:

```python
# Get a pastel palette
colors = PALETTES.pastel
print(colors)
```

#### Example with Matplotlib

```python
import matplotlib.pyplot as plt
from pigmenta import PALETTES

colors = PALETTES.sunset

plt.bar([1, 2, 3], [3, 5, 2], color=colors[:3])
plt.title("Bar chart using pigmenta")
plt.show()
```

#### 🎨 Available Palettes

Here are the palette names you can access via `PALETTES.<name>`:

```
pastel, vintage, retro, neon, gold, light, dark, warm, cold,
summer, fall, winter, spring, happy, nature, earth, night, space,
rainbow, gradient, sunset, sky, sea, kids, skin, food, cream,
coffee, wedding, christmas, halloween
```

Access any of them like:

```python
PALETTES.sky
PALETTES.christmas
```

### 🛠️ Custom Palettes

You can also register or override palettes by modifying the `COLORS` dictionary directly if allowed by your API:

```python
from pigmenta.core import COLORS

COLORS['custom'] = ['#111111', '#222222', '#333333']
```

### 💡 Use Cases

- Visualizing data in elegant color themes.
- Designing dashboards or GUIs.
- Generative art and graphics programming.
- Branding and UI prototyping.

### 🧩 Future Plans

- Add support for gradient generation.
- Integration with design tools or Jupyter extensions.

### 📬 Contributing

Contributions, bug reports, and palette suggestions are welcome! Please open an issue or pull request on the [GitHub repository](https://github.com/crispengari/pigmenta).

### 📝 License

This project is licensed under the MIT License — see the [`LICENSE`](/LICENSE) file for details.
