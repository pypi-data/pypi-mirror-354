
# mhmixtools

`mhmixtools` is a Python utility package providing automation tools for developers and web maintainers. It includes features like HTML template syncing, image utilities, site crawling/reporting, folder structure generation, and helpful decorators.

---

## 📦 Installation

```bash
pip install mhmixtools
````

---

## ✨ Features

* **template\_sync**: Automate updating HTML files with a shared layout.
* **image\_utils**: Download and manage image files efficiently.
* **webcrawler**: Crawl websites, collect links, and generate reports.
* **folder\_structure\_generator**: Generate project folder structures quickly.
* **decorators**: Simple decorators to track function execution time.

---

## 🧩 Module Guide

### 1. `template_sync`

Update multiple HTML files with a shared template layout, preserving dynamic sections.

#### 🔹 `list_html`

```python
list_html(exclude_dirs: list, show: bool = True) -> list
```

* **Parameters**:

  * `exclude_dirs`: Directories to ignore.
  * `show`: Print file paths if True (default); return list if False.

#### 🔹 `render_templates`

```python
render_templates(template_url: str, target_files: list, content_id: str, indent: int = 4)
```

* **Updates** HTML files by replacing layout while keeping content inside an element with `id=content_id`.

---

### 2. `image_utils`

Tools for working with images from the web and image converters.

#### 🔹 `get_next_filename`

```python
get_next_filename(base_path: str, filename: str) -> str
```

* Returns a unique filename to avoid overwriting existing files in a directory.

#### 🔹 `download_image`

```python
download_image(url: str, save_dir: str, filename: str = None)
```

* Downloads an image from a URL and saves it, generating a unique name if needed.

---

### 3. `webcrawler`

Analyze websites and generate a report of all internal, external, image links, and broken pages.

#### 🔹 `get_internal_links`, `get_external_links`, `get_image_links`

* Extracts respective link types from a BeautifulSoup-parsed page and base URL.

#### 🔹 `crawl_site`

```python
crawl_site(start_url: str, max_pages: int = 100)
```

* Crawls a website and gathers data from pages.

#### 🔹 `check_broken_pages`

Checks for broken links (HTTP errors or unreachable pages).

#### 🔹 `generate_site_report`

Returns a structured dictionary summarizing internal, external, image links, and broken pages.

#### 🔹 `print_site_report` and `save_site_report`

* Display or save the crawl results.

---

### 4. `folder_structure_generator`

Quickly create nested folder structures for projects.

#### 🔹 `list_files`

```python
list_files(base_dir: str, depth: int = 1, prefix: str = "")
```

* Prints or returns folder structure recursively to a specified depth.

---

### 5. `decorators`

Helper decorator for monitoring performance.

#### 🔹 `execution_time`

```python
@execution_time
def your_function():
    ...
```

* Prints how long a function takes to execute.

---

## 🧪 Example Usage

### Template Sync

```python
from mhmixtools.template_sync import list_html, render_templates

files = list_html(exclude_dirs=['env'], show=False)
render_templates(template_url="base.html", target_files=files, content_id="content")
```

### Download Image

```python
from mhmixtools.image_utils import download_image

download_image("https://example.com/image.jpg", save_dir="images")
```

### Crawl Site

```python
from mhmixtools.webcrawler import crawl_site, print_site_report

report = crawl_site("https://example.com", max_pages=50)
print_site_report(report)
```

---

## 📌 Notes

* Designed for developers working with static HTML sites, scraping, or automating small tasks.
* Contributions and suggestions are welcome via GitHub issues.

---

## 🛠️ License

MIT License

---

## 🤝 Contribute

If you have ideas, improvements, or new tools to add, feel free to open an [issue](https://github.com/mahamudh472/mhmixtools/issues) or submit a pull request!

