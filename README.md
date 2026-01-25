# Z+ Exam Platform

A fully static, client-side exam portal. It serves as a central hub that links to specific subject repositories.

## 🛠️ Developer Overview

- **Tech**: HTML5, Vanilla JavaScript (ES6 Modules), CSS3.
- **Architecture**: Single Page Application (SPA) feel without a framework.
- **Data Source**: Embedded `EXAM_DATA` object in `renderer.js` (No backend database).
- **Localization**: Native bilingual support (English/Arabic) via `index.html`.

## 📂 Project Structure

- **index.html**: The main entry point. Handles routing (Home/Sections/Exam), Localization, and UI layout.
- **engine/**:
  - `renderer.js`: Main controller. Manages Views, Subject Rendering, and Search.
  - `evaluator.js`: Scoring logic.
  - `timer.js`: Countdown logic.
- **Editor/**:
  - `Renderer.py`: A Python GUI tool to safely edit `renderer.js` without touching code.

## ➕ How to Add a Section

You have two ways to add a new exam section:

### Option A: Using the GUI Editor (Recommended)
1.  Run the Python script:
    ```bash
    python3 Editor/Renderer.py
    ```
2.  Click **"Open renderer.js"** and select `engine/renderer.js`.
3.  Click **"Add Subject"**.
4.  Fill in the details:
    - **ID**: Unique key (e.g., `python101`).
    - **Name**: Display title (e.g., `Python Basics`).
    - **Description**: Short subtitle.
    - **External Link**: The URL to the deployed exam repo (e.g., `https://your-user.github.io/python-exam/`).
5.  Click **"Save Changes"** -> **"Save to renderer.js"**.

### Option B: Manual Code Edit
1.  Open `engine/renderer.js`.
2.  Locate the `EXAM_DATA` object.
3.  Add a new entry:
    ```javascript
    new_subject: {
        id: "new_subject",
        name: "New Subject Title",
        description: "Brief description",
        externalLink: "https://link-to-exam-repo.com/"
    },
    ```
4.  Save the file.
