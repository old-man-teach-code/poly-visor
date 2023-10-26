//ChartJS import
// import chartjs from 'chart.js';
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
// import chartjs from 'chart.js/auto';
// const { Chart, LineElement, PointElement, LineController, CategoryScale, LinearScale, Filler, Legend, Title, Tooltip } = chartjs;

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
//ChartJS function for creating, updating. Delete chart when there's no param
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

//call start process api
export async function startProcess(formData) {
	//if loading is true, return
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/processes/start`, {
		method: 'POST',
		body: formData
	})
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
}
export async function stopProcess(formData) {
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/processes/stop`, {
		method: 'POST',
		body: formData
	})
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
}
export async function startAllProcess(supervisor) {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/processes/startAll/${supervisor}`)
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
	return res;
}

export async function stopAllProcess(supervisor) {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/processes/stopAll/${supervisor}`)
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
	return res;
}

export async function addNewProcessConf(conf) {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/config/create`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(conf)
	})
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
	return res;
}

export async function renderProcessConf(name) {
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/config/render/${get(currentPid)}/${name}`)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			return data;
		})
		.catch((error) => {
			console.error(error);
		})
		.finally(() => loading.set(false));
}

export async function Taskset(pid, index) {
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/cpu/set_affinity/${pid}/${index}`)
		.then((response) => response.json())
		.then((data) => {
			return data;
		})
		.catch((error) => {
			console.error(error);
		})
		.finally(() => loading.set(false));
}

export async function getAllSupervisors() {
	loading.set(true);
	return fetch(`/api/supervisors`)
		.then((response) => response.json())
		.then((data) => {
			return data;
		})
		.catch((error) => {
			console.error(error);
		})
		.finally(() => loading.set(false));
}

export async function login(formdata) {
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/login`, {
		method: 'POST',
		body: formdata
	})
		.then((message) => message.json())
		.then((data) => {
			return data;
		})
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
}

export async function logout() {
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/logout`, {
		method: 'POST'
	})
		.then((message) => message.json())
		.then((data) => {
			console.log(data);
			return data;
		})
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
}
