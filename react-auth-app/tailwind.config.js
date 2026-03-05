/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-out': 'slideOut 0.4s ease-in forwards',
        'bounce-in': 'bounceIn 0.6s ease-out',
        'pulse-ring': 'pulse 2s infinite',
        'spin-slow': 'spin 1s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideOut: {
          '0%': { opacity: '1', transform: 'translateX(0)' },
          '100%': { opacity: '0', transform: 'translateX(-100px)' },
        },
        bounceIn: {
          '0%': { opacity: '0', transform: 'scale(0.3)' },
          '50%': { opacity: '1', transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        pulse: {
          '0%': { boxShadow: '0 0 0 0 rgba(99, 102, 241, 0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(99, 102, 241, 0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(99, 102, 241, 0)' },
        },
      },
    },
  },
  plugins: [],
}