# Z+ Exam Platform

A fully static, client-side exam portal. It acts as a central hub linking to subject-specific repositories.

## 🛠️ Developer Overview

- **Tech**: HTML5, Vanilla JavaScript (ES6 Modules), CSS3.
- **Architecture**: Modular SPA. Data is separated from logic for cleaner edits.
- **Data Source**: `engine/sections.js` (Centralized `EXAM_DATA`).
- **Localization**: Native English/Arabic support via `index.html`.

## 📂 Project Structure

- **index.html**: App entry point. Handles layout and localization.
- **engine/**:
  - `renderer.js`: UI Controller. Manages view switching and subject rendering.
  - `sections.js`: **Data Store**. Contains all subject metadata and links.
- **Editor/**:
  - `Renderer.py`: Python GUI tool to edit `sections.js` without touching code.

## ➕ How to Add a Section

### Option A: GUI Editor (Recommended)
1.  Run: `python3 Editor/Renderer.py`
2.  Open `engine/sections.js`.
3.  Add/Edit subjects and click **"Save to sections.js"**.

### Option B: Manual Edit
1.  Open `engine/sections.js`.
2.  Add a new entry to the `EXAM_DATA` object:
    ```javascript
    subject_id: {
        id: "subject_id",
        name: "Subject Title",
        description: "Short description",
        externalLink: "https://your-github-io-link.com/"
    },
    ```
3.  Save the file.
