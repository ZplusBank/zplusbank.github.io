# 📚 Online Exam Platform

A fully static, serverless online exam platform. No backend, no database, no login required.

## ✨ Features

- 🚀 **100% Static** - Runs entirely in the browser
- 📝 **Multiple Question Types** - MCQ, Code Output, True/False
- ⏱️ **Timed Exams** - Countdown timer with auto-submit
- 🎨 **Modern UI** - Clean, responsive design
- 📊 **Instant Results** - Score calculation and feedback

## 🎯 Live Demo

[View Live Demo](https://your-username.github.io/online-exam/)

## 🚀 Quick Start

1. Clone this repository
2. Open `online-exam/index.html` in your browser
3. Start taking exams!

## 📁 Project Structure

```
online-exam/
├── index.html          # Main entry point
├── assets/
│   └── style.css      # Styling
└── engine/
    ├── renderer.js    # UI & exam data (embedded)
    ├── timer.js       # Countdown timer
    └── evaluator.js   # Answer checking
```

## 🛠️ Adding Subjects

Each subject redirects to a separate HTML repository. This allows you to organize exams independently.

**See [HOW_TO_ADD_SUBJECTS.md](HOW_TO_ADD_SUBJECTS.md) for detailed instructions.**

Quick example - edit `engine/renderer.js`:

```javascript
const EXAM_DATA = {
    math: {
        id: "math",
        name: "Mathematics",
        description: "Algebra, Calculus, and Geometry",
        externalLink: "https://your-username.github.io/math-exams/"
    },
    physics: {
        id: "physics",
        name: "Physics",
        description: "Mechanics and Thermodynamics",
        externalLink: "./exams/physics.html"  // or use relative paths
    }
};
```

Each subject card will redirect users to the specified URL when clicked.

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Fork, create a branch, and submit a PR.
