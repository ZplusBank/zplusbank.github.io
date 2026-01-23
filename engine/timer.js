/**
 * timer.js
 * Handles the exam countdown timer.
 */

let timerInterval = null;
let remainingTime = 0;

export function startTimer(durationSeconds, onTick, onComplete) {
    if (timerInterval) clearInterval(timerInterval);

    remainingTime = durationSeconds;

    // Initial tick
    onTick(formatTime(remainingTime));

    timerInterval = setInterval(() => {
        remainingTime--;

        if (remainingTime <= 0) {
            stopTimer();
            onTick(formatTime(0));
            if (onComplete) onComplete();
        } else {
            onTick(formatTime(remainingTime));
        }
    }, 1000);
}

export function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

export function getRemainingTime() {
    return remainingTime;
}

function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}
