import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default [
  {
    ignores: ['.astro/**', 'out/**', 'node_modules/**'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{js,mjs,ts}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',
        document: 'readonly',
        IntersectionObserver: 'readonly',
        process: 'readonly',
        setTimeout: 'readonly',
        window: 'readonly',
      },
    },
  },
];
