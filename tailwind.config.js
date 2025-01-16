/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/component/**/*.html', // HTML components (dashboard.html, index.html, onboarding.html)
    './src/**/*.py',             // Python files (app.py, process_audio.py, etc.)
    './src/static/css/**/*.css', // CSS files (static.css)
	],
  theme: {
    extend: {},
  },
  plugins: [],
}
