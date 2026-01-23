# How to Add Subjects to Your Online Exam Platform

## Overview
Each subject card on the home page now redirects to a separate HTML repository/page. This allows you to organize your exams independently and host them anywhere.

## Adding a New Subject

### Step 1: Edit `engine/renderer.js`

Open `engine/renderer.js` and locate the `EXAM_DATA` object (around line 10). Add your subject following this structure:

```javascript
const EXAM_DATA = {
    math: {
        id: "math",
        name: "Mathematics",
        description: "Algebra, Calculus, and Geometry exams",
        externalLink: "https://your-username.github.io/math-exams/index.html"
    },
    physics: {
        id: "physics",
        name: "Physics",
        description: "Mechanics, Thermodynamics, and Electromagnetism",
        externalLink: "https://your-username.github.io/physics-exams/index.html"
    },
    chemistry: {
        id: "chemistry",
        name: "Chemistry",
        description: "Organic, Inorganic, and Physical Chemistry",
        externalLink: "./local-exams/chemistry.html"  // Can also use relative paths
    }
};
```

### Step 2: Create Your External Exam Repository

Each subject should have its own HTML page or repository. You can:

1. **Use GitHub Pages**: Create a separate repository for each subject
2. **Use Local Files**: Store HTML files in a subdirectory
3. **Use Any Web Host**: Host your exam pages anywhere

### Example Subject Structure

```
your-math-exams-repo/
├── index.html          (Main exam page)
├── assets/
│   ├── style.css
│   └── questions.json
└── engine/
    └── exam-logic.js
```

### Step 3: Link Format

- **Absolute URL**: `https://your-domain.com/exam.html`
- **Relative Path**: `./exams/math.html` (relative to your main index.html)
- **GitHub Pages**: `https://username.github.io/repo-name/index.html`

## Subject Properties

| Property | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Unique identifier (lowercase, no spaces) |
| `name` | Yes | Display name shown on the card |
| `description` | Yes | Brief description of the subject |
| `externalLink` | Yes | URL or path to the exam HTML page |

## Tips

1. **Keep it organized**: One repository per subject makes maintenance easier
2. **Use GitHub Pages**: Free hosting for your exam repositories
3. **Test links**: Make sure all external links work before deploying
4. **Consistent design**: Use similar styling across all exam pages for better UX

## Example: Adding a Programming Subject

```javascript
const EXAM_DATA = {
    programming: {
        id: "programming",
        name: "Programming",
        description: "C++, Python, JavaScript, and Algorithms",
        externalLink: "https://yourusername.github.io/programming-exams/"
    }
};
```

When users click the "Programming" card, they'll be redirected to your programming exams repository.
