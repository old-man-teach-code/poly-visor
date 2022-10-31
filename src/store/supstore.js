import { writable } from "svelte/store";

//writables for fetching api
export const system = writable([]);
export const processes = writable([]);
export const count = writable(0);

//fetch api
const fetchAll = async () => {
    // fetching system data
    const resSystem = await fetch('http://127.0.0.1:5000/api/system');
    const dataSystem = await resSystem.json();
    system.set(dataSystem);
    // fetching processes data
    const resProcesses = await fetch('http://127.0.0.1:5000/api/processes');
    const dataProcesses = await resProcesses.json();
    processes.set(dataProcesses);

    count.set(0);
    for (let process of dataProcesses) {
        if (process.state == 20) {
            count.update(n => n + 1);
        }
    }
}
//fetch api every 2 seconds
setInterval(fetchAll, 2000);
