/**
 * renderer.js
 * Main UI Controller. Renders views and manages app flow.
 * Redirects to external HTML repositories based on section data.
 */

import { EXAM_DATA } from './sections.js';

// State
let allSubjects = []; // Store for filtering

// DOM Elements
const views = {
    home: document.getElementById('home-view'),
    sections: document.getElementById('sections-view')
};

const dom = {
    subjectsGrids: document.querySelectorAll('.subjects-grid'),
    btnHome: document.getElementById('btn-home'),
    navHome: document.getElementById('nav-home'),
    navSubjects: document.getElementById('nav-subjects'),
    btnExplore: document.getElementById('btn-explore'),
    sectionSearch: document.getElementById('section-search'),
    appLoader: document.getElementById('app-loader')
};

export function initApp() {
    // Render subjects from externalized data
    allSubjects = Object.values(EXAM_DATA);
    renderSubjects(allSubjects);

    // Hide loader
    if (dom.appLoader) {
        dom.appLoader.classList.add('hidden');
    }

    // Event Listeners
    setupEventListeners();
}

function setupEventListeners() {
    if (dom.btnHome) dom.btnHome.addEventListener('click', showHome);
    if (dom.navHome) dom.navHome.addEventListener('click', showHome);
    if (dom.navSubjects) dom.navSubjects.addEventListener('click', showSectionsView);
    if (dom.btnExplore) dom.btnExplore.addEventListener('click', showSectionsView);

    // Search Filter
    if (dom.sectionSearch) {
        dom.sectionSearch.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = allSubjects.filter(s =>
                s.name.toLowerCase().includes(term) ||
                s.description.toLowerCase().includes(term)
            );
            renderSubjects(filtered);
        });
    }
}

function renderSubjects(subjects) {
    if (!dom.subjectsGrids || dom.subjectsGrids.length === 0) return;

    dom.subjectsGrids.forEach(grid => {
        grid.innerHTML = '';

        if (subjects.length === 0) {
            grid.innerHTML = '<p style="text-align:center; grid-column: 1 / -1; width:100%;">No sections found.</p>';
            return;
        }

        subjects.forEach(subject => {
            const card = document.createElement('div');
            card.className = 'subject-card';
            card.innerHTML = `
                <h3><i class="fas fa-book"></i> ${escapeHtml(subject.name)}</h3>
                <p>${escapeHtml(subject.description)}</p>
            `;

            card.addEventListener('click', () => {
                if (subject.externalLink) {
                    window.location.href = subject.externalLink;
                } else {
                    alert('No exam link configured for this subject.');
                }
            });

            grid.appendChild(card);
        });
    });
}

function switchView(viewName) {
    Object.values(views).forEach(el => {
        if (el) el.classList.add('hidden');
    });
    if (views[viewName]) views[viewName].classList.remove('hidden');

    // Update Active Nav
    if (dom.navHome) dom.navHome.classList.toggle('active', viewName === 'home');
    if (dom.navSubjects) dom.navSubjects.classList.toggle('active', viewName === 'sections');
}

function showHome() {
    switchView('home');
}

function showSectionsView() {
    switchView('sections');
    if (dom.sectionSearch) {
        dom.sectionSearch.value = ''; // Reset search
        dom.sectionSearch.focus();
    }
    renderSubjects(allSubjects); // Show all
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



