import { browser } from "$app/environment";
import { writable } from "svelte/store";

//writables for fetching api
export const system = writable([]);
export const processes = writable([]);
export const count = writable(0);
export const cpuCount = writable(0);
export const cpuChart = writable(Array(31));
export const ramChart = writable(Array(31));

//fetch api
const fetchAll = async () => {
    try {
        // fetching system data
        const resSystem = await fetch('http://127.0.0.1:5000/api/system');
        const dataSystem = await resSystem.json();
        let cpus = dataSystem.machineSpec.CPUs;
        cpuCount.set(cpus);
        system.set(dataSystem);
        cpuChart.update(items => {
            items.shift();
            items.push(dataSystem.cpu);
            return items
        })
        ramChart.update(items => {
            items.shift();
            items.push(dataSystem.memory);
            return items
        })
        // fetching processes data
        const resProcesses = await fetch('http://127.0.0.1:5000/api/processes');
        const dataProcesses = await resProcesses.json();
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
            stateColor: (((data.statename == "RUNNING") || (data.statename == "STARTING")) ? ('bg-green-300') : (data.statname == "BACKOFF") ? ('bg-yellow-300') : ('bg-red-300')),
            core_index: data.core_index
        }));
        processes.set(loadedProcesses);

        count.set(0);
        for (let process of dataProcesses) {
            if (process.state == 20) {
                count.update(n => n + 1);
            }
        }

    } catch (err) {
        console.log(err);
    }
}
// //First time calling api when the page loads
fetchAll();
// //fetch api every 2 seconds
setInterval(fetchAll, 1000);
