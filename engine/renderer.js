/**
 * renderer.js
 * Main UI Controller. Renders views and manages app flow.
 * FULLY SELF-CONTAINED - No external data fetching required
 */

import { startTimer, stopTimer } from './timer.js';
import { calculateScore } from './evaluator.js';

// Subject data - each subject redirects to a separate HTML repository
// Add your subjects here with their external links
const EXAM_DATA = {

    java: {
        "id": "java",
        "name": "OOP2",
        "description": "Chapter 17 questions",
        "externalLink": "https://ibdx.github.io/javaOOP17/"
    },
    it: {
        "id": "it",
        "name": "Information Technology",
        "description": "IT Subjects",
        "externalLink": "https://zplusbank.github.io/it/"
    }


};

// State
let currentExam = null;
let currentQuestionIndex = 0;
let userAnswers = {}; // { questionIndex: selectedOptionIndex }
let allSubjects = []; // Store for filtering

// DOM Elements
const views = {
    home: document.getElementById('home-view'),
    sections: document.getElementById('sections-view'),
    exam: document.getElementById('exam-view'),
    results: document.getElementById('results-view')
};

const dom = {
    subjectsGrid: document.getElementById('subjects-grid'),
    examTitle: document.getElementById('exam-title'),
    questionContainer: document.getElementById('question-container'),
    btnPrev: document.getElementById('btn-prev'),
    btnNext: document.getElementById('btn-next'),
    btnSubmit: document.getElementById('btn-submit'),
    timerDisplay: document.getElementById('exam-timer'),
    progressFill: document.getElementById('progress-fill'),
    scoreText: document.getElementById('score-text'),
    scoreCircle: document.getElementById('score-circle-path'),
    resultMessage: document.getElementById('result-message'),
    btnRetry: document.getElementById('btn-retry'),
    btnHome: document.getElementById('btn-home'),
    navHome: document.getElementById('nav-home'),
    navSubjects: document.getElementById('nav-subjects'), // New
    btnExplore: document.getElementById('btn-explore'),   // New
    sectionSearch: document.getElementById('section-search'), // New
    appLoader: document.getElementById('app-loader')
};

export function initApp() {
    // Render subjects from embedded data
    allSubjects = Object.values(EXAM_DATA);
    renderSubjects(allSubjects);

    // Hide loader
    dom.appLoader.classList.add('hidden');

    // Event Listeners
    setupEventListeners();
}

function setupEventListeners() {
    dom.btnNext.addEventListener('click', () => {
        if (currentQuestionIndex < currentExam.questions.length - 1) {
            currentQuestionIndex++;
            renderQuestion();
        }
    });

    dom.btnPrev.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            renderQuestion();
        }
    });

    dom.btnSubmit.addEventListener('click', finishExam);
    dom.btnRetry.addEventListener('click', () => startExam(currentExam)); // Restart same exam
    dom.btnHome.addEventListener('click', showHome);
    dom.navHome.addEventListener('click', showHome);

    // New Navigation
    dom.navSubjects.addEventListener('click', showSectionsView);
    dom.btnExplore.addEventListener('click', showSectionsView);

    // Search Filter
    dom.sectionSearch.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allSubjects.filter(s =>
            s.name.toLowerCase().includes(term) ||
            s.description.toLowerCase().includes(term)
        );
        renderSubjects(filtered);
    });
}

function renderSubjects(subjects) {
    dom.subjectsGrid.innerHTML = '';

    if (subjects.length === 0) {
        dom.subjectsGrid.innerHTML = '<p style="text-align:center; col-span:3; width:100%;">No sections found.</p>';
        return;
    }

    subjects.forEach(subject => {
        const card = document.createElement('div');
        card.className = 'subject-card';
        card.innerHTML = `
            <h3><i class="fas fa-book"></i> ${subject.name}</h3>
            <p>${subject.description}</p>
        `;

        card.addEventListener('click', () => {
            // Redirect to external HTML repository
            if (subject.externalLink) {
                window.location.href = subject.externalLink;
            } else {
                alert('No exam link configured for this subject.');
            }
        });

        dom.subjectsGrid.appendChild(card);
    });
}

function switchView(viewName) {
    Object.values(views).forEach(el => el.classList.add('hidden'));
    views[viewName].classList.remove('hidden');

    // Update Active Nav
    dom.navHome.classList.toggle('active', viewName === 'home');
    dom.navSubjects.classList.toggle('active', viewName === 'sections');
}

function showHome() {
    stopTimer();
    switchView('home');
    currentExam = null;
}

function showSectionsView() {
    stopTimer();
    switchView('sections');
    currentExam = null;
    dom.sectionSearch.value = ''; // Reset search
    renderSubjects(allSubjects); // Show all
    dom.sectionSearch.focus();
}

function startExam(examData) {
    currentExam = examData;
    currentQuestionIndex = 0;
    userAnswers = {};

    dom.examTitle.textContent = examData.title;
    switchView('exam');

    renderQuestion();

    startTimer(examData.duration, (timeStr) => {
        dom.timerDisplay.textContent = timeStr;
    }, () => {
        alert("Time's up!");
        finishExam();
    });
}

function renderQuestion() {
    const q = currentExam.questions[currentQuestionIndex];
    if (!q) return;

    // Update Progress
    const progress = ((currentQuestionIndex + 1) / currentExam.questions.length) * 100;
    dom.progressFill.style.width = `${progress}%`;

    // Controls State
    dom.btnPrev.disabled = currentQuestionIndex === 0;
    if (currentQuestionIndex === currentExam.questions.length - 1) {
        dom.btnNext.classList.add('hidden');
        dom.btnSubmit.classList.remove('hidden');
    } else {
        dom.btnNext.classList.remove('hidden');
        dom.btnSubmit.classList.add('hidden');
    }

    // Render Logic
    let html = `<div class="question-text">${currentQuestionIndex + 1}. ${q.question}</div>`;

    if (q.codeSnippet) {
        html += `<pre class="code-block"><code>${escapeHtml(q.codeSnippet)}</code></pre>`;
    }

    html += `<div class="options-grid">`;
    q.options.forEach((opt, idx) => {
        const isSelected = userAnswers[currentQuestionIndex] === idx;
        html += `
            <div class="option-card ${isSelected ? 'selected' : ''}" onclick="window.selectOption(${idx})">
                <div class="option-marker"></div>
                <div class="option-content">${escapeHtml(opt)}</div>
            </div>
        `;
    });
    html += `</div>`;

    dom.questionContainer.innerHTML = html;
}

// Global helper for inline onclick (module scope workaround)
window.selectOption = (idx) => {
    userAnswers[currentQuestionIndex] = idx;
    renderQuestion(); // Re-render to update UI
};

function finishExam() {
    stopTimer();
    const result = calculateScore(currentExam.questions, userAnswers);
    showResults(result);
}

function showResults(result) {
    switchView('results');

    dom.scoreText.textContent = `${result.percentage}%`;
    const circumference = 100; // from stroke-dasharray
    const offset = circumference - (result.percentage / 100) * circumference;
    dom.scoreCircle.style.strokeDasharray = `${result.percentage}, 100`;

    // Color based on score
    if (result.percentage >= 80) {
        dom.scoreCircle.style.stroke = 'var(--success-color)';
        dom.resultMessage.textContent = "Excellent Work!";
    } else if (result.percentage >= 50) {
        dom.scoreCircle.style.stroke = 'var(--accent-color)';
        dom.resultMessage.textContent = "Good job, but room for improvement.";
    } else {
        dom.scoreCircle.style.stroke = 'var(--danger-color)';
        dom.resultMessage.textContent = "Keep practicing!";
    }
}

function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}



