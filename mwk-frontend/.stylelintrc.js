module.exports = {
  extends: ['stylelint-config-prettier', 'stylelint-config-recess-order', 'stylelint-config-standard-scss'],
  rules: {
    'value-keyword-case': null,
    indentation: 2,
    'string-quotes': 'single',
    'selector-class-pattern': '^[a-z][a-zA-Z0-9]+$'
  },
  ignoreFiles: [
    'src/styles/**/*.scss'
  ]
}
