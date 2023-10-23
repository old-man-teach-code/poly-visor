import { get, writable } from 'svelte/store';

//writables for fetching api
export const system = writable([]);
export const loading = writable(false);
export const processes = writable([]);
export const count = writable(0);
export const cpuCount = writable(0);
export const cpuChart = writable(Array(31));
export const ramChart = writable(Array(31));

let systemInterval;
let processesInterval;

export const dashboardEnabled = writable(localStorage.dashboardEnabled || true);
dashboardEnabled.subscribe((value) => {
	localStorage.dashboardEnabled = value;
});

export const isAuthenticated = writable(localStorage.isAuthenticated || false);
isAuthenticated.subscribe((value) => {
	localStorage.isAuthenticated = value;
});

export const currentSupervisor = writable(localStorage.currentSupervisor || '');
currentSupervisor.subscribe((value) => {
	localStorage.currentSupervisor = value;
});

//fetch api
const fetchSystem = async () => {
	if (get(isAuthenticated) == 'true') {
		try {
			// fetching system data
			const resSystem = await fetch('/api/system');
			const dataSystem = await resSystem.json();
			let cpus = dataSystem.machineSpec.CPUs;
			cpuCount.set(cpus);
			system.set(dataSystem);
			cpuChart.update((items) => {
				items.shift();
				items.push(dataSystem.cpu);
				return items;
			});
			ramChart.update((items) => {
				items.shift();
				items.push(dataSystem.memory);
				return items;
			});
		} catch (err) {
			console.log(err);
		}
	}
};

async function fetchProcesses() {
	// fetching processes data
	try {

		const supervisorName = get(currentSupervisor);
		const resProcesses = await fetch(`/api/supervisor/${supervisorName}/processes`);
		const data = await resProcesses.json();
		//mapd data.processes to array
		const dataProcesses = Object.values(data.processes);
		const loadedProcesses = dataProcesses.map((data) => ({
			description: data.description,
			exitstatus: data.exitstatus,
			group: data.group,
			logfile: data.logfile,
			name: data.name,
			pid: data.pid,
			spawnerr: data.spawnerr,
			start: data.start,
			state: data.state,
			statename: data.statename,
			stderr_logfile: data.stderr_logfile,
			stdout_logfile: data.stdout_logfile,
			stop: data.stop,
			stateColor:
				data.statename == 'RUNNING' || data.statename == 'STARTING'
					? 'bg-green-300'
					: data.statname == 'BACKOFF'
					? 'bg-yellow-300'
					: 'bg-red-300',
			core_index: data.core_index
		}));
		processes.set(loadedProcesses);

		count.set(0);
		for (let process of dataProcesses) {
			if (process.state == 20) {
				count.update((n) => n + 1);
			}
		}
	} catch (err) {
		console.log(err);
	}
}

export function toggleSystemInterval() {
	if (get(dashboardEnabled) == 'true') {
		systemInterval = setInterval(async () => {
			fetchSystem();
		}, 2000);
	} else {
		clearInterval(systemInterval);
	}
}

export function toggleProcessesInterval() {
	fetchProcesses();
	if (get(isAuthenticated) == 'true') {
		processesInterval = setInterval(async () => {
			fetchProcesses();
		}, 2000);
	} else {
		clearInterval(processesInterval);
	}
}
