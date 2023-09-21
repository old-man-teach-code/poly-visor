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
import { loading } from './supstore.js';
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
export async function startProcess(name) {
	//if loading is true, return
	if (get(loading)) return;
	loading.set(true);
	return fetch(`/api/process/start/${name}`)
		.then((response) => response.json())
		.then((data) => {
			return data;
		})
		.catch((error) => {
			console.error(error);
		})
		.finally(() => loading.set(false));
}
export async function stopProcess(name) {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/process/stop/${name}`)
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
	return res;
}

export async function startAllProcess() {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/processes/start`)
		.then((message) => message.json())
		.catch((err) => console.log(err))
		.finally(() => loading.set(false));
	return res;
}

export async function stopAllProcess() {
	if (get(loading)) return;
	loading.set(true);
	const res = fetch(`/api/processes/stop`)
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
	return fetch(`/api/config/render/${name}`)
		.then((response) => response.json())
		.then((data) => {
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
