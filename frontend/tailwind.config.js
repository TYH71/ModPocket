/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
        "./public/index.html",
    ],
    theme: {
        extend: {
            colors: {
                // NUS Brand Colors
                'nus-orange': '#EF7C00',
                'nus-blue': '#003D7C',
                'nus-dark': '#1a1a2e',
                'nus-darker': '#16162a',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'spin-slow': 'spin 2s linear infinite',
            },
        },
    },
    plugins: [],
}
