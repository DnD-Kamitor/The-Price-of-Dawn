const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// API routes
app.get('/api/puzzles', (req, res) => {
  // In a real app, this would come from a database
  res.json([
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
  ]);
});

// Serve the main game page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`D&D Puzzle Game server running on http://localhost:${PORT}`);
});