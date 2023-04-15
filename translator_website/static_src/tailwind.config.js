module.exports = {
  content: ['../templates/**/*.html'],
  separator: ':',
  corePlugins: {},
  plugins: [],
  theme: {
    extend: {
      colors: {
        brand: {
          white: '#f8f1e6',
          brown: '#c4a691',
          main: '#f1b989',
          grey: '#aa9894',
          dark: '#9d7476'
        }
      },
      fontFamily: {
        'brand': ['Hahmlet']
      }
    }
  }
}