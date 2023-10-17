import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';

const config: UserConfig = {
	server: {
		proxy: {
			"/api": {
				target: "http://localhost:5000",
				changeOrigin: true,
			}
		},
	},
	plugins: [sveltekit()]
};

export default config;