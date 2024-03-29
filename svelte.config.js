import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';


/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: [
		preprocess({
		  postcss: true,
		}),
	  ],
	kit: {
		adapter: adapter({
			pages: 'polyvisor/build',
			assets: 'polyvisor/build',
			fallback: null,
			precompress: false,
			strict: true
		})
	}
};

export default config;
