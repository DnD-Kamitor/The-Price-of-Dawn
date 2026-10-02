// Puzzle Game JavaScript

let currentPuzzleIndex = 0;
let score = 0;
let timerInterval;
let timeElapsed = 0;

// Puzzle data (in a real app, this would come from the API)
const puzzles = [
  {
    id: 1,
    title: "The Riddle of the Sphinx",
    description: "What walks on four legs in the morning, two legs at noon, and three legs in the evening?",
    answer: "human",
    difficulty: "easy",
    hint: "Think about the stages of human life"
  },
  {
    id: 2,
    title: "The Dungeon Door",
    description: "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
    answer: "echo",
    difficulty: "medium",
    hint: "It's a sound phenomenon"
  },
  {
    id: 3,
    title: "The Wizard's Tower",
    description: "The more you take, the more you leave behind. What am I?",
    answer: "footsteps",
    difficulty: "hard",
    hint: "Think about walking"
  }
];

// DOM elements
const puzzleTitle = document.getElementById('puzzle-title');
const puzzleDescription = document.getElementById('puzzle-description');
const answerInput = document.getElementById('answer-input');
const submitBtn = document.getElementById('submit-btn');
const showHintBtn = document.getElementById('show-hint');
const hintText = document.getElementById('hint-text');
const resultMessage = document.getElementById('result-message');
const correctAnswer = document.getElementById('correct-answer');
const difficultyLevel = document.getElementById('difficulty-level');
const scoreElement = document.getElementById('score');
const timerElement = document.getElementById('timer');

// Initialize the game
function initGame() {
  loadPuzzle(currentPuzzleIndex);
  startTimer();
  setupEventListeners();
}

// Load a puzzle
function loadPuzzle(index) {
  const puzzle = puzzles[index];
  puzzleTitle.textContent = puzzle.title;
  puzzleDescription.textContent = puzzle.description;
  difficultyLevel.textContent = puzzle.difficulty.charAt(0).toUpperCase() + puzzle.difficulty.slice(1);
  hintText.textContent = puzzle.hint;
  
  // Reset UI
  answerInput.value = '';
  resultMessage.textContent = '';
  correctAnswer.classList.add('hidden');
  answerInput.focus();
}

// Start the timer
function startTimer() {
  timerInterval = setInterval(() => {
    timeElapsed++;
    const minutes = Math.floor(timeElapsed / 60);
    const seconds = timeElapsed % 60;
    timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }, 1000);
}

// Stop the timer
function stopTimer() {
  clearInterval(timerInterval);
}

// Check the answer
function checkAnswer() {
  const userAnswer = answerInput.value.trim().toLowerCase();
  const correctAnswerText = puzzles[currentPuzzleIndex].answer.toLowerCase();
  
  if (userAnswer === correctAnswerText) {
    resultMessage.textContent = 'Correct! Well done!';
    resultMessage.style.color = '#27ae60';
    correctAnswer.textContent = `The answer was: ${puzzles[currentPuzzleIndex].answer}`;
    correctAnswer.classList.remove('hidden');
    score += 10;
    scoreElement.textContent = score;
    
    // Disable input after correct answer
    answerInput.disabled = true;
    submitBtn.disabled = true;
    
    // Move to next puzzle after a delay
    setTimeout(() => {
      if (currentPuzzleIndex < puzzles.length - 1) {
        currentPuzzleIndex++;
        loadPuzzle(currentPuzzleIndex);
        answerInput.disabled = false;
        submitBtn.disabled = false;
      } else {
        resultMessage.textContent = 'Congratulations! You solved all puzzles!';
        resultMessage.style.color = '#27ae60';
        stopTimer();
      }
    }, 1500);
  } else {
    resultMessage.textContent = 'Incorrect. Try again!';
    resultMessage.style.color = '#e74c3c';
    answerInput.value = '';
    answerInput.focus();
  }
}

// Show hint
function showHint() {
  hintText.classList.toggle('hidden');
  showHintBtn.textContent = hintText.classList.contains('hidden') ? 'Show Hint' : 'Hide Hint';
}

// Setup event listeners
function setupEventListeners() {
  submitBtn.addEventListener('click', checkAnswer);
  
  answerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      checkAnswer();
    }
  });
  
  showHintBtn.addEventListener('click', showHint);
}

// Start the game when the page loads
document.addEventListener('DOMContentLoaded', initGame);