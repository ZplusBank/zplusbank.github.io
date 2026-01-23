/**
 * evaluator.js
 * Handles checking answers and calculating scores.
 */

export function checkAnswer(question, selectedIndex) {
    // For MCQ, answer is the index of the correct option
    return question.answer === selectedIndex;
}

export function calculateScore(questions, userAnswers) {
    let correctCount = 0;

    questions.forEach((q, index) => {
        // userAnswers is a map or array where index corresponds to question index
        // or key is question id.
        // Let's assume userAnswers is an object { [questionIndex]: selectedOptionIndex }

        const selected = userAnswers[index];
        if (selected !== undefined && selected !== null) {
            if (checkAnswer(q, selected)) {
                correctCount++;
            }
        }
    });

    const percentage = (correctCount / questions.length) * 100;

    return {
        correct: correctCount,
        total: questions.length,
        percentage: Math.round(percentage)
    };
}
