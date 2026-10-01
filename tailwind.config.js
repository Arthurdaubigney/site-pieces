/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './assets/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: '#161b22', 900: '#0f1318', 700: '#2a313b', 500: '#5b6573', 300: '#a5adb9' },
        gold: { DEFAULT: '#a6823c', 600: '#8a6a2b', 400: '#c9a965', 100: '#f3ead6' },
        paper: { DEFAULT: '#faf8f4', 2: '#f2eee6' },
        line: '#e6e0d3',
      },
      fontFamily: {
        sans: ['Geist', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'serif'],
      },
      boxShadow: {
        soft: '0 1px 2px rgb(22 27 34 / .04), 0 12px 32px -12px rgb(22 27 34 / .14)',
      },
    },
  },
  plugins: [],
};
