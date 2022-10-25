/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
          colors: {
      'text-logo': '#A4A6B3',
      'sidebar':  '#363740'
    }
    }

  },
  plugins: []
};