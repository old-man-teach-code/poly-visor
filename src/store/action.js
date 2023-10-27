import {
	Chart,
	LineElement,
	PointElement,
	LineController,
	CategoryScale,
	LinearScale,
	Filler,
	Legend,
	Title,
	Tooltip
} from 'chart.js';
import { currentPid, loading } from './supstore.js';
import { get } from 'svelte/store';

Chart.register(
	LineElement,
	PointElement,
	LineController,
	CategoryScale,
	LinearScale,
	Filler,
	Legend,
	Title,
	Tooltip
);

let chart;

export function chartJS(node, config) {
	const ctx = node.getContext('2d');
	chart = new Chart(ctx, config);
	return {
		update(newConfig) {
			chart.data = newConfig.data;
			Object.assign(chart.options, newConfig.options);
			chart.update();
		},
		destroy() {
			chart.destroy();
		}
	};
}

export function destroyChart() {
	chart.destroy();
}

async function makeApiRequest(url, method, body) {
	if (get(loading)) return;
	loading.set(true);
	try {
		const response = await fetch(url, {
			method: method,
			body: body
		});

		const data = await response.json();

		if (data.status === 401) {
			window.location.href = '/login';
			alert('Unauthorized');
		}

		return data;
	} catch (error) {
		console.error(error);
	} finally {
		loading.set(false);
	}
}

export async function startProcess(formData) {
	return makeApiRequest('/api/processes/start', 'POST', formData);
}

export async function stopProcess(formData) {
	return makeApiRequest('/api/processes/stop', 'POST', formData);
}

export async function startAllProcess(supervisor) {
	return makeApiRequest(`/api/processes/startAll/${supervisor}`);
}

export async function stopAllProcess(supervisor) {
	return makeApiRequest(`/api/processes/stopAll/${supervisor}`);
}

export async function addNewProcessConf(conf) {
	return makeApiRequest('/api/config/create', 'POST', JSON.stringify(conf));
}

export async function renderProcessConf(name) {
	return makeApiRequest(`/api/config/render/${get(currentPid)}/${name}`);
}

export async function Taskset(pid, index) {
	return makeApiRequest(`/api/cpu/set_affinity/${pid}/${index}`);
}

export async function getAllSupervisors() {
	return makeApiRequest('/api/supervisors');
}

export async function login(formdata) {
	return makeApiRequest('/api/login', 'POST', formdata);
}

export async function logout() {
	return makeApiRequest('/api/logout', 'POST');
}
