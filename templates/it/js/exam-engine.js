// ===== Global State =====
let sections = [];
let currentSection = null;
let currentChapter = null;
let currentQuestionIndex = 0;
let userAnswers = {};
let examStartTime = null;
let timerInterval = null;
let currentFilter = 'all';
let searchQuery = '';

// ===== Initialize App =====
document.addEventListener('DOMContentLoaded', () => {
    loadSections();
    setupEventListeners();
    hljs.highlightAll();
});

// ===== Event Listeners =====
function setupEventListeners() {
    // Search
    document.getElementById('searchInput').addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        filterSections();
    });

    // Filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');
            currentFilter = e.currentTarget.dataset.filter;
            filterSections();
        });
    });
}

// ===== Load Sections =====
async function loadSections() {
    try {
        // In a real implementation, this would scan the data directory
        // For now, we'll manually define sections
        sections = [
            {
                id: 'java2',
                title: 'Java 2',
                icon: '🎯',
                folder: 'java2',
                chapters: [
                    { id: 'chapter9', title: 'Chapter 9 Objects and Classes', file: 'chapter9.json', questions: 4 }
                ],
                totalQuestions: 4,
                status: 'not-started'
            }
        ];

        renderSections();
        updateFilterCounts();
    } catch (error) {
        console.error('Error loading sections:', error);
    }
}

// ===== Render Sections =====
function renderSections() {
    const grid = document.getElementById('sectionsGrid');
    const noResults = document.getElementById('noResults');

    const filteredSections = sections.filter(section => {
        const matchesSearch = section.title.toLowerCase().includes(searchQuery);
        const matchesFilter = currentFilter === 'all' || section.status === currentFilter;
        return matchesSearch && matchesFilter;
    });

    if (filteredSections.length === 0) {
        grid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }

    grid.style.display = 'grid';
    noResults.style.display = 'none';

    grid.innerHTML = filteredSections.map(section => `
        <div class="section-card" onclick="openSection('${section.id}')">
            <span class="section-icon">${section.icon}</span>
            <h3 class="section-title">${section.title}</h3>
            <div class="section-meta">
                <div class="meta-item">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                    ${section.chapters.length} Chapter${section.chapters.length !== 1 ? 's' : ''}
                </div>
                <div class="meta-item">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                        <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg>
                    ${section.totalQuestions} Question${section.totalQuestions !== 1 ? 's' : ''}
                </div>
            </div>
            <span class="section-status status-${section.status}">
                ${section.status.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </span>
        </div>
    `).join('');
}

// ===== Filter Sections =====
function filterSections() {
    renderSections();
}

// ===== Update Filter Counts =====
function updateFilterCounts() {
    document.getElementById('countAll').textContent = sections.length;
    document.getElementById('countCompleted').textContent = sections.filter(s => s.status === 'completed').length;
    document.getElementById('countInProgress').textContent = sections.filter(s => s.status === 'in-progress').length;
    document.getElementById('countNotStarted').textContent = sections.filter(s => s.status === 'not-started').length;
}

// ===== Open Section =====
function openSection(sectionId) {
    currentSection = sections.find(s => s.id === sectionId);
    if (!currentSection) return;

    const modal = document.getElementById('chapterModal');
    const modalTitle = document.getElementById('modalTitle');
    const chaptersList = document.getElementById('chaptersList');

    modalTitle.textContent = `${currentSection.title} - Select Chapter`;

    chaptersList.innerHTML = currentSection.chapters.map(chapter => `
        <div class="chapter-item" onclick="startChapter('${chapter.id}')">
            <div class="chapter-info">
                <h3>${chapter.title}</h3>
                <p>${chapter.questions} questions</p>
            </div>
            <div class="chapter-arrow">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
            </div>
        </div>
    `).join('');

    modal.classList.add('active');
}

// ===== Close Chapter Modal =====
function closeChapterModal() {
    document.getElementById('chapterModal').classList.remove('active');
}

// ===== Start Chapter =====
async function startChapter(chapterId) {
    const chapter = currentSection.chapters.find(c => c.id === chapterId);
    if (!chapter) return;

    try {
        const response = await fetch(`data/${currentSection.folder}/${chapter.file}`);
        const data = await response.json();

        currentChapter = data[0];
        currentQuestionIndex = 0;
        userAnswers = {};
        examStartTime = Date.now();

        closeChapterModal();
        showPage('examPage');
        startTimer();
        renderQuestion();
    } catch (error) {
        console.error('Error loading chapter:', error);
        alert('Failed to load chapter. Please try again.');
    }
}

// ===== Show Page =====
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

// ===== Start Timer =====
function startTimer() {
    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        const elapsed = Date.now() - examStartTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        document.getElementById('timerText').textContent =
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

// ===== Render Question =====
function renderQuestion() {
    const question = currentChapter.questions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');

    document.getElementById('examTitle').textContent = currentChapter.title;
    document.getElementById('progressText').textContent =
        `${currentQuestionIndex + 1}/${currentChapter.questions.length}`;

    const progress = ((currentQuestionIndex + 1) / currentChapter.questions.length) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;

    const isMultipleChoice = question.inputType === 'checkbox';
    const savedAnswer = userAnswers[question.id] || (isMultipleChoice ? [] : '');

    container.innerHTML = `
        <div class="question-number">Question ${currentQuestionIndex + 1} of ${currentChapter.questions.length}</div>
        <div class="question-text">${question.text}</div>
        <div class="choices">
            ${question.choices.map(choice => {
        const isChecked = isMultipleChoice
            ? savedAnswer.includes(choice.value)
            : savedAnswer === choice.value;

        return `
                    <label class="choice ${isChecked ? 'selected' : ''}" for="choice-${choice.value}">
                        <input 
                            type="${question.inputType}" 
                            id="choice-${choice.value}"
                            name="${question.inputName}" 
                            value="${choice.value}"
                            ${isChecked ? 'checked' : ''}
                            onchange="handleAnswerChange('${question.id}', '${choice.value}', ${isMultipleChoice})"
                        />
                        <span class="choice-label">
                            <strong>${choice.label}.</strong> ${choice.text}
                        </span>
                    </label>
                `;
    }).join('')}
        </div>
    `;

    // Highlight code blocks
    container.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    // Update navigation buttons
    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;

    const isLastQuestion = currentQuestionIndex === currentChapter.questions.length - 1;
    document.getElementById('nextBtn').style.display = isLastQuestion ? 'none' : 'flex';
    document.getElementById('submitBtn').style.display = isLastQuestion ? 'flex' : 'none';
}

// ===== Handle Answer Change =====
function handleAnswerChange(questionId, value, isMultiple) {
    if (isMultiple) {
        if (!userAnswers[questionId]) {
            userAnswers[questionId] = [];
        }

        const index = userAnswers[questionId].indexOf(value);
        if (index > -1) {
            userAnswers[questionId].splice(index, 1);
        } else {
            userAnswers[questionId].push(value);
        }

        // Sort to match answer format
        userAnswers[questionId].sort();
    } else {
        userAnswers[questionId] = value;
    }

    // Update UI
    const choices = document.querySelectorAll('.choice');
    choices.forEach(choice => {
        const input = choice.querySelector('input');
        if (input.checked) {
            choice.classList.add('selected');
        } else {
            choice.classList.remove('selected');
        }
    });
}

// ===== Navigation =====
function nextQuestion() {
    if (currentQuestionIndex < currentChapter.questions.length - 1) {
        currentQuestionIndex++;
        renderQuestion();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion();
    }
}

// ===== Exit Exam =====
function exitExam() {
    if (confirm('Are you sure you want to exit? Your progress will be lost.')) {
        if (timerInterval) clearInterval(timerInterval);
        showPage('mainPage');
    }
}

// ===== Submit Exam =====
function submitExam() {
    if (timerInterval) clearInterval(timerInterval);

    const totalTime = Date.now() - examStartTime;
    let correct = 0;
    let incorrect = 0;

    currentChapter.questions.forEach(question => {
        const userAnswer = userAnswers[question.id];
        const correctAnswer = question.correctAnswer;

        let isCorrect = false;
        if (question.inputType === 'checkbox') {
            const userAnswerStr = (userAnswer || []).sort().join('');
            isCorrect = userAnswerStr === correctAnswer;
        } else {
            isCorrect = userAnswer === correctAnswer;
        }

        if (isCorrect) {
            correct++;
        } else {
            incorrect++;
        }
    });

    const total = currentChapter.questions.length;
    const percentage = Math.round((correct / total) * 100);

    // Update results page
    document.getElementById('scorePercentage').textContent = `${percentage}%`;
    document.getElementById('correctCount').textContent = correct;
    document.getElementById('incorrectCount').textContent = incorrect;
    document.getElementById('totalCount').textContent = total;

    const minutes = Math.floor(totalTime / 60000);
    const seconds = Math.floor((totalTime % 60000) / 1000);
    document.getElementById('timeSpent').textContent =
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Animate score ring
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (percentage / 100) * circumference;

    // Add SVG gradient
    const svg = document.querySelector('.score-ring');
    if (!svg.querySelector('defs')) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'scoreGradient');
        gradient.innerHTML = `
            <stop offset="0%" stop-color="hsl(250, 84%, 64%)" />
            <stop offset="100%" stop-color="hsl(199, 89%, 48%)" />
        `;
        defs.appendChild(gradient);
        svg.appendChild(defs);
    }

    setTimeout(() => {
        document.getElementById('scoreRing').style.strokeDashoffset = offset;
    }, 300);

    // Update section status
    if (percentage >= 80) {
        currentSection.status = 'completed';
    } else {
        currentSection.status = 'in-progress';
    }
    updateFilterCounts();

    showPage('resultsPage');
}

// ===== Review Answers =====
function reviewAnswers() {
    currentQuestionIndex = 0;
    showPage('examPage');
    renderReviewQuestion();
}

function renderReviewQuestion() {
    const question = currentChapter.questions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');

    const isMultipleChoice = question.inputType === 'checkbox';
    const userAnswer = userAnswers[question.id] || (isMultipleChoice ? [] : '');
    const correctAnswer = question.correctAnswer;

    let isCorrect = false;
    if (isMultipleChoice) {
        const userAnswerStr = (userAnswer || []).sort().join('');
        isCorrect = userAnswerStr === correctAnswer;
    } else {
        isCorrect = userAnswer === correctAnswer;
    }

    container.innerHTML = `
        <div class="question-number">Question ${currentQuestionIndex + 1} of ${currentChapter.questions.length}</div>
        <div class="question-text">${question.text}</div>
        <div class="choices">
            ${question.choices.map(choice => {
        const isUserChoice = isMultipleChoice
            ? userAnswer.includes(choice.value)
            : userAnswer === choice.value;

        const isCorrectChoice = correctAnswer.includes(choice.value);

        let choiceClass = '';
        if (isCorrectChoice) {
            choiceClass = 'correct';
        } else if (isUserChoice && !isCorrectChoice) {
            choiceClass = 'incorrect';
        }

        return `
                    <label class="choice ${choiceClass}" for="choice-${choice.value}">
                        <input 
                            type="${question.inputType}" 
                            id="choice-${choice.value}"
                            name="${question.inputName}" 
                            value="${choice.value}"
                            ${isUserChoice ? 'checked' : ''}
                            disabled
                        />
                        <span class="choice-label">
                            <strong>${choice.label}.</strong> ${choice.text}
                        </span>
                    </label>
                `;
    }).join('')}
        </div>
        <div style="margin-top: 2rem; padding: 1rem; background: var(--bg-tertiary); border-radius: var(--radius); border-left: 4px solid ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
            <strong style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
                ${isCorrect ? '✓ Correct' : '✗ Incorrect'}
            </strong>
        </div>
    `;

    // Highlight code blocks
    container.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    // Update navigation
    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;
    document.getElementById('prevBtn').onclick = () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            renderReviewQuestion();
        }
    };

    const isLastQuestion = currentQuestionIndex === currentChapter.questions.length - 1;
    document.getElementById('nextBtn').style.display = isLastQuestion ? 'none' : 'flex';
    document.getElementById('nextBtn').onclick = () => {
        if (currentQuestionIndex < currentChapter.questions.length - 1) {
            currentQuestionIndex++;
            renderReviewQuestion();
        }
    };

    document.getElementById('submitBtn').style.display = 'none';
}

// ===== Back to Home =====
function backToHome() {
    // Reset navigation functions
    document.getElementById('prevBtn').onclick = previousQuestion;
    document.getElementById('nextBtn').onclick = nextQuestion;

    showPage('mainPage');
    renderSections();
}
