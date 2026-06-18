# ZPlus Global Redirect 🌐

This repository catches all legacy incoming traffic and consolidates it down to the new root website homepage.

## 🚀 Mapping Strategy
* `https://zplusbank.github.io/` ➡️ `https://zplus.codes`
* `https://zplusbank.github.io/anything` ➡️ `https://zplus.codes`
* `https://github.io` ➡️ `https://zplus.codes`

* [zplus.codes](https://zplus.codes)


---

## 🛠️ How It Works
1. **`index.html`**: Immediately routes root domain visitors via standard meta headers and Javascript fallback.
2. **`404.html`**: Serves as a global catch-all router. If a user visits an outdated sub-path, GitHub Pages triggers this custom 404 layout, which instantly forces the browser window straight to the primary home address instead of displaying an error.
