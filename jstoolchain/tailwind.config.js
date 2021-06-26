module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    screens: {
      'sm': '640px',
      'md': '848px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
		cursor: {
			auto: 'auto',
			default: 'default',
			pointer: 'pointer',
			wait: 'wait',
			text: 'text',
			move: 'move', 
			'not-allowed': 'not-allowed',
			crosshair: 'crosshair', 
			'zoom-in': 'zoom-in',
			'zoom-out': 'zoom-out',
		},
		extend: {
			inset: {
				'screen': '100vh',
				'-screen': '-100vh',
			},
			transformOrigin: {
				'0': '0%',
			},
			zIndex: {
				'-1': '-1',
			},
      spacing: {
				4.5: '1.125rem',
      },
      padding: {
				4.5: '1.125rem',
      },
      maxHeight: {
				'500': '500rem',
      },
			colors: {
				primary: {
					'50': '#FDF2F8',
					'100': '#FCE7F3',
					'200': '#FBCFE8',
					'300': '#F472B6',
					'400': '#F472B6',
					'500': '#EC4899',
					'600': '#DB2777',
					'700': '#BE185D',
					'800': '#9D174D',
					'900': '#831843',
				}
			},
      borderWidth: {
				'3': '3px',
			}
		},
	},
	variants: {
		extend: {
			borderWidth: ['hover', ],
			padding: ['hover', 'focus'],
			animation: ['hover', 'focus'],
		}
	},
	plugins: [],
	purge: {
    enabled: true,
    content: [
			'../account/templates/**/*.html',
			'../blog/templates/**/*.html',
			'../cart/templates/**/*.html',
			'../contact/templates/**/*.html',
			'../coupon/templates/**/*.html',
			'../home/templates/**/*.html',
			'../newsletter/templates/**/*.html',
			'../order/templates/**/*.html',
			'../shop/templates/**/*.html',
			'../streams/templates/**/*.html',
			'../webshop/templates/**/*.html',
			'../winwheel/templates/**/*.html',
			'../account/static/**/*.js',
			'../blog/static/**/*.js',
			'../cart/static/**/*.js',
			'../contact/static/**/*.js',
			'../coupon/static/**/*.js',
			'../home/static/**/*.js',
			'../newsletter/static/**/*.js',
			'../order/static/**/*.js',
			'../shop/static/**/*.js',
			'../streams/static/**/*.js',
			'../webshop/static/**/*.js',
			'../winwheel/static/**/*.js',
		],
  },
}
