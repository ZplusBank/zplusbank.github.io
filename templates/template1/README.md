# Exam Platform - Template 1

A modern, fully-featured exam platform template with support for MCQ and multiple selection questions, code syntax highlighting, search/filter functionality, and comprehensive results tracking.

## 🎯 Features

### Core Functionality
- ✅ **Multiple Question Types**: Support for both radio (MCQ) and checkbox (multiple selection) questions
- ✅ **Code Syntax Highlighting**: Beautiful code rendering using Highlight.js with Atom One Dark theme
- ✅ **Section-Based Organization**: Organize exams by sections and chapters
- ✅ **Search & Filters**: Real-time search and filter by completion status
- ✅ **Progress Tracking**: Visual progress bar and question counter
- ✅ **Timer**: Built-in exam timer with elapsed time tracking
- ✅ **Results Dashboard**: Comprehensive results with score percentage, correct/incorrect counts, and time spent
- ✅ **Review Mode**: Review all answers with correct/incorrect highlighting after submission

### UI/UX
- 🎨 **Modern Dark Theme**: Premium dark mode with glassmorphism effects
- 🌈 **Gradient Accents**: Beautiful gradient colors using HSL for vibrant visuals
- ✨ **Smooth Animations**: Micro-animations and transitions for enhanced user experience
- 📱 **Responsive Design**: Fully responsive layout that works on all devices
- 🎯 **Accessible**: Semantic HTML and proper ARIA labels

## 📁 Directory Structure

```
template1/
├── index.html              # Main application file
├── css/
│   └── styles.css         # Comprehensive styling
├── js/
│   └── exam-engine.js     # Exam logic and functionality
└── data/
    └── [Section_Name]/    # Each section has its own folder
        ├── chapter1.json  # Chapter data files
        ├── chapter2.json
        └── ...
```

## 🚀 Getting Started

### 1. Setup

Simply open `index.html` in a modern web browser. No build process or server required!

### 2. Adding Sections

Create a new folder in the `data/` directory for each section:

```
data/
├── Objects_and_Classes/
├── Data_Structures/
└── Algorithms/
```

### 3. Creating Chapter Files

Each chapter is a JSON file with the following structure:

```json
[
  {
    "id": "task-0",
    "label": "chapter=9, username=liang12e",
    "params": {
      "chapter": "9",
      "username": "liang12e"
    },
    "title": "Chapter 9 Objects and Classes",
    "questions": [
      {
        "id": "9.1",
        "number": "9.1",
        "text": "Question text here with <strong>HTML</strong> support",
        "choices": [
          {
            "value": "A",
            "label": "A",
            "text": "First choice"
          },
          {
            "value": "B",
            "label": "B",
            "text": "Second choice"
          }
        ],
        "inputName": "Q0",
        "inputType": "radio",
        "correctAnswer": "B"
      }
    ],
    "status": "completed",
    "totalQuestions": 52
  }
]
```

### 4. Registering Sections

In `js/exam-engine.js`, update the `loadSections()` function:

```javascript
sections = [
    {
        id: 'objects-and-classes',
        title: 'Objects and Classes',
        icon: '🎯',
        folder: 'Objects_and_Classes',
        chapters: [
            { 
                id: 'chapter9', 
                title: 'Chapter 9 Objects and Classes', 
                file: 'chapter9.json', 
                questions: 52 
            }
        ],
        totalQuestions: 52,
        status: 'not-started'
    },
    // Add more sections here...
];
```

## 📝 Question Types

### Radio (MCQ) - Single Selection

```json
{
  "id": "9.1",
  "number": "9.1",
  "text": "Question text",
  "choices": [...],
  "inputName": "Q0",
  "inputType": "radio",
  "correctAnswer": "B"
}
```

### Checkbox - Multiple Selection

```json
{
  "id": "9.7",
  "number": "9.7",
  "text": "Select all that apply",
  "choices": [...],
  "inputName": "QD6",
  "inputType": "checkbox",
  "correctAnswer": "ABCD"
}
```

For multiple selection, the `correctAnswer` is a string of all correct choice values concatenated (e.g., "ABCD" means A, B, C, and D are all correct).

## 💻 Code Highlighting

The template supports code blocks with syntax highlighting. Use HTML with proper class names:

```html
<span style="font-family:monospace; font-size: 109%;">
  <span class="keyword">public</span> 
  <span class="keyword">class</span> 
  Test {
    <span class="keyword">int</span> x = 
    <span class="constant">5</span>;
  }
</span>
```

Supported classes:
- `.keyword` - Programming keywords (purple)
- `.constant` - Numbers and constants (orange)
- `.literal` - String literals (green)

## 🎨 Customization

### Colors

Edit CSS variables in `css/styles.css`:

```css
:root {
    --primary: hsl(250, 84%, 54%);
    --secondary: hsl(199, 89%, 48%);
    --success: hsl(142, 71%, 45%);
    --danger: hsl(0, 84%, 60%);
    /* ... more colors */
}
```

### Icons

Section icons use emojis. Change them in the sections array:

```javascript
icon: '🎯',  // Change to any emoji
```

### Fonts

The template uses Inter font from Google Fonts. To change:

1. Update the `<link>` in `index.html`
2. Update `font-family` in CSS

## 🔧 Advanced Features

### Status Tracking

The system automatically tracks section status:
- **Not Started**: No chapters attempted
- **In Progress**: Score < 80%
- **Completed**: Score ≥ 80%

### Local Storage

Currently, the template doesn't persist data. To add persistence:

```javascript
// Save answers
localStorage.setItem('exam-answers', JSON.stringify(userAnswers));

// Load answers
const saved = localStorage.getItem('exam-answers');
if (saved) userAnswers = JSON.parse(saved);
```

## 📱 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ⚠️ IE11 (not supported)

## 🤝 Contributing

To add new features:

1. **New Question Types**: Extend the `renderQuestion()` function
2. **Analytics**: Add tracking in `submitExam()`
3. **Export Results**: Add export functionality in results page

## 📄 License

This template is free to use for educational purposes.

## 🎓 Example Usage

1. **Educational Institutions**: Create course exams
2. **Self-Study**: Build practice quizzes
3. **Certification Prep**: Organize study materials
4. **Code Challenges**: Technical interview preparation

## 🐛 Troubleshooting

### Questions not loading
- Check JSON syntax in chapter files
- Verify file paths in `loadSections()`
- Check browser console for errors

### Code not highlighting
- Ensure Highlight.js CDN is accessible
- Verify code block HTML structure
- Check CSS class names

### Styles not applying
- Clear browser cache
- Check CSS file path
- Verify CSS variable names

## 📞 Support

For issues or questions, please check:
1. JSON structure matches the example
2. File paths are correct
3. Browser console for errors

---

**Built with ❤️ for developers and learners**
