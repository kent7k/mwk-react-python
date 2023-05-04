const path = require('path')

const rootDir = __dirname

const OFF = 0
const WARNING = 1
const ERROR = 2

module.exports = {
  env: {
    browser: true,
    jest: true,
  },
  extends: [
    'airbnb',
    'airbnb-typescript',
    'airbnb/hooks',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:import/typescript',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    tsconfigRootDir: rootDir,
    project: 'tsconfig.json',
  },

  plugins: ['import', '@typescript-eslint', 'react-hooks', 'sort-export-all'],
  rules: {
    "@typescript-eslint/naming-convention": "off", // FIXME
    '@typescript-eslint/no-explicit-any': 'off', // FIXME
    '@typescript-eslint/explicit-function-return-type': OFF,
    '@typescript-eslint/explicit-module-boundary-types': OFF,
    '@typescript-eslint/prefer-interface': OFF,
    '@typescript-eslint/no-unused-vars': [
      ERROR,
      {
        argsIgnorePattern: '^_',
      },
    ],
    '@typescript-eslint/comma-dangle': [
      ERROR,
      {
        arrays: 'always-multiline',
        objects: 'always-multiline',
        imports: 'always-multiline',
        exports: 'always-multiline',
        enums: 'always-multiline',
        functions: 'never',
      },
    ],
    'no-return-assign': OFF,
    'no-console': OFF,
    'import/no-extraneous-dependencies': [
      'error',
      {
        devDependencies: [
          '**/*.setup.{js,ts}',
          '**/*.config.{js,ts}',
          '**/*.spec.{ts,tsx}',
          '**/*.stories.{ts,tsx}',
          '**/__fixtures__/**/*.{ts,tsx}',
          '**/mocks/**/*.{ts,tsx}',
        ],
        peerDependencies: false,
      },
    ],
    'import/order': [
      ERROR,
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          "type",
          'index',
        ],
        pathGroups: [
          {
            pattern: 'react*',
            group: 'builtin',
            position: 'before',
          },
          {
            pattern: '{@mui/**, @reduxjs/**, formik, moment, yup}',
            group: 'external',
            position: 'before',
          },
          // {
          //   pattern: 'redux-thunk',
          //   group: 'external',
          //   position: 'after',
          // },
        ],
        pathGroupsExcludedImportTypes: ['react'],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],
    'sort-imports': ['error', { ignoreDeclarationSort: true }],
    'sort-export-all/sort-export-all': 'warn',
    'import/no-named-export': OFF,
    'import/no-relative-packages': OFF,
    'import/newline-after-import': ERROR,
    'import/named': OFF, // ref: https://github.com/benmosher/eslint-plugin-import/issues/1282
    'import/prefer-default-export': OFF,
    'jsx-a11y/anchor-is-valid': OFF,
    'react/display-name': OFF,
    'react-hooks/rules-of-hooks': 'error',
    'react/jsx-filename-extension': [WARNING, { extensions: ['.tsx'] }],
    'react/jsx-fragments': [ERROR, 'element'],
    'react/jsx-props-no-spreading': OFF,
    'react/prop-types': OFF,
    'react/require-default-props': OFF,
    'react/function-component-definition': [
      ERROR,
      {
        namedComponents: ['arrow-function'],
        unnamedComponents: ['arrow-function'],
      },
    ],
    semi: ['error', 'never', { beforeStatementContinuationChars: 'never' }],
    'semi-spacing': ['error', { after: true, before: false }],
    'semi-style': ['error', 'first'],
    'no-extra-semi': 'error',
    'no-unexpected-multiline': ERROR,
    'no-unreachable': ERROR,
    '@typescript-eslint/semi': OFF,
    // 'react/no-unstable-nested-components': OFF,
    'react/react-in-jsx-scope': OFF,
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
}
