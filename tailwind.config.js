/** @type {import('tailwindcss').Config} */

/*
Tanzania flag colors generated using:
- https://www.flagcolorcodes.com/tanzania
- https://uicolors.app/create 
*/

// tz_flag_green = {
//   '50': '#f0fdf2',
//   '100': '#dcfce1',
//   '200': '#bbf7c5',
//   '300': '#85f098',
//   '400': '#49df65',
//   '500': '#1eb53a', //main 
//   '600': '#15a430',
//   '700': '#148129',
//   '800': '#156625',
//   '900': '#145321',
//   '950': '#052e0f',
// }

// tz_flag_yellow = {
//   '50': '#fefce8',
//   '100': '#fffac2',
//   '200': '#fff389',
//   '300': '#ffe445',
//   '400': '#fcd116', //main
//   '500': '#ecb706',
//   '600': '#cc8e02',
//   '700': '#a26406',
//   '800': '#864f0d',
//   '900': '#724011',
//   '950': '#432105',
// }

// tz_flag_blue = {
//   '50': '#f0faff',
//   '100': '#e0f4fe',
//   '200': '#b9ebfe',
//   '300': '#7cddfd',
//   '400': '#36cdfa',
//   '500': '#0cb7eb',
//   '600': '#00a3dd', // main
//   '700': '#0176a3',
//   '800': '#066386',
//   '900': '#0b526f',
//   '950': '#07344a',
// }


const darkPrimary = "#2B1392"
const lightPrimary = "#004AAD"

const accentPurple = "#2C05F2"
const accentYellow = "#FFCD29"

const accentGreen = "#048041"

module.exports = {
  content: ["./**/*.html", '!./dev_db',
  ],
  theme: {
    extend: {
      colors: {
        // tz_flag_green,
        // tz_flag_yellow,
        // tz_flag_blue
        darkPrimary,
        lightPrimary,
        accentPurple,
        accentYellow,
        accentGreen
      },
    },
  },
  plugins: [],
}

