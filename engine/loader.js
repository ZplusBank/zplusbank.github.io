/**
 * loader.js
 * Handles fetching of data from remote (or local) JSON files.
 */

// Function to fetch the list of subjects
export async function fetchSubjects() {
    try {
        const response = await fetch('config/subjects.json');
        if (!response.ok) {
            throw new Error(`Failed to load subjects: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching subjects:", error);
        return [];
    }
}

// Function to fetch a specific exam file
// url could be relative or absolute
export async function fetchExam(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to load exam: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching exam:", error);
        throw error;
    }
}
