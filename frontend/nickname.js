// nickname.js

function generateNickname() {
  const emojis = ['🌿', '🫧', '🌸', '🕊️', '🌙', '💮', '🦋', '🍃', '✨', '🌻'];
  const adjectives = ['Quiet', 'Gentle', 'Calm', 'Warm', 'Soft', 'Kind', 'Brave', 'Shy', 'Still', 'Tender'];
  const nouns = ['River', 'Voice', 'Cloud', 'Fox', 'Flame', 'Petal', 'Wind', 'Whisper', 'Rain', 'Echo'];

  const emoji = emojis[Math.floor(Math.random() * emojis.length)];
  const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
  const noun = nouns[Math.floor(Math.random() * nouns.length)];

  return `${emoji} ${adjective}${noun}`;
}

// Auto-generate on load
window.addEventListener('DOMContentLoaded', () => {
  const output = document.getElementById('nickname');
  if (output) output.textContent = generateNickname();
});