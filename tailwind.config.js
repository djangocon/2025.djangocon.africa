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


//

const darkPrimary = "#0F103F"
const lightPrimary = "#2B1392"

const accentPurple = "#2C05F2"
const accentYellow = "#FFCD29"
const accentPink = "#FF93DD"

const accentGreen = "#048041"

const deepTeal = '#004B65'

module.exports = {
  content: ["./**/*.html", '!./dev_db',
  ],
  theme: {
    extend: {
      fontFamily: {
        bebasneue: ['BebasNeue', 'sans-serif'],
        chivomono: ['Chivomono', 'sans-serif'],
        archivo: ['Archivo', 'sans-serif']
      },
      colors: {
        // tz_flag_green,
        // tz_flag_yellow,
        // tz_flag_blue
        darkPrimary,
        lightPrimary,
        accentPurple,
        accentYellow,
        accentGreen,
        accentPink,
        deepTeal
      },
      backgroundImage: {
        'dotted-world-map': "url('/static/images/dotted-world-map.svg')",
    },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}

