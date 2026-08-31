/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: '1.25rem',
        sm: '2rem',
        lg: '2.5rem',
      },
      screens: {
        '2xl': '1200px',
      },
    },
    extend: {
      colors: {
        // Claude.com Signature Canvas & Surface Tokens
        canvas: '#faf9f5',
        'surface-soft': '#f5f0e8',
        'surface-card': '#efe9de',
        'surface-cream-strong': '#e8e0d2',
        'surface-dark': '#181715',
        'surface-dark-elevated': '#252320',
        'surface-dark-soft': '#1f1e1b',
        hairline: '#e6dfd8',
        'hairline-soft': '#ebe6df',

        // Brand Coral Tokens
        primary: {
          DEFAULT: '#cc785c',
          active: '#a9583e',
          disabled: '#e6dfd8',
        },
        coral: {
          DEFAULT: '#cc785c',
          active: '#a9583e',
          disabled: '#e6dfd8',
        },

        // Secondary Accents
        'accent-teal': '#5db8a6',
        'accent-amber': '#e8a55a',

        // Text Hierarchy
        ink: '#141413',
        'body-strong': '#252523',
        body: '#3d3d3a',
        muted: '#6c6a64',
        'muted-soft': '#8e8b82',
        'on-primary': '#ffffff',
        'on-dark': '#faf9f5',
        'on-dark-soft': '#a09d96',

        // Semantic
        success: '#5db872',
        warning: '#d4a017',
        error: '#c64545',
      },
      fontFamily: {
        serif: [
          'Cormorant Garamond',
          'EB Garamond',
          'Tiempos Headline',
          'Copernicus',
          'Garamond',
          'Georgia',
          'serif',
        ],
        sans: [
          'Inter',
          'StyreneB',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace',
        ],
      },
      borderRadius: {
        xs: '4px',
        sm: '6px',
        md: '8px',
        lg: '12px',
        xl: '16px',
        pill: '9999px',
      },
      spacing: {
        section: '96px',
      },
      letterSpacing: {
        'display-xl': '-1.5px',
        'display-lg': '-1px',
        'display-md': '-0.5px',
        'display-sm': '-0.3px',
        'caption-upper': '1.5px',
      },
      lineHeight: {
        'display-xl': '1.05',
        'display-lg': '1.1',
        'display-md': '1.15',
        'display-sm': '1.2',
      },
      boxShadow: {
        subtle: '0 1px 3px rgba(20, 20, 19, 0.08)',
        dark: '0 4px 20px rgba(0, 0, 0, 0.35)',
      },
    },
  },
  plugins: [],
}
