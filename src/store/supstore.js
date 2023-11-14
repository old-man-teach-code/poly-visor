import { get, writable } from 'svelte/store';

//writables for fetching api
export const system = writable([]);
export const loading = writable(false);
export const processes = writable([]);
export const count = writable(0);
export const cpuCount = writable(0);

let systemInterval;
let processesInterval;

export const chartInstances = writable(localStorage.chartInstances || 30);
chartInstances.subscribe((value) => {
	localStorage.chartInstances = value;
});

export const cpuChart = writable(Array(Number(localStorage.chartInstances)));
export const ramChart = writable(Array(Number(localStorage.chartInstances)));

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

export const currentPid = writable(localStorage.currentPid || -1);
currentPid.subscribe((value) => {
	localStorage.currentPid = value;
});

//fetch api
export const fetchSystem = async () => {
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

export async function fetchProcesses() {
	// fetching processes data
	try {
		const supervisorName = get(currentSupervisor);
		const resProcesses = await fetch(`/api/supervisor/${supervisorName}/processes`);
		const data = await resProcesses.json();
		if (get(currentPid) == -1 && get(currentPid) != data.pid) {
			currentPid.set(data.pid);
		}
		//map data.processes to array
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
			network_io_counters: [
				{
					key: 'read counter',
					value: data?.network_io_counters[0] || 'Unavailable'
				},
				{
					key: 'write counter',
					value: data?.network_io_counters[1] || 'Unavailable'
				},
				{
					key: 'read bytes',
					value: data?.network_io_counters[2] || 'Unavailable'
				},
				{
					key: 'write bytes',
					value: data?.network_io_counters[3] || 'Unavailable'
				},
				{
					key: 'read chars',
					value: data?.network_io_counters[4] || 'Unavailable'
				},
				{
					key: 'write chars',
					value: data?.network_io_counters[5] || 'Unavailable'
				}
			],
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
