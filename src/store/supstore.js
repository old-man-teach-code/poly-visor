import { writable,derived } from "svelte/store";

export const allProcessInfo = writable([]);

// export const fetchState = async() =>{
//     const url = 'http://127.0.0.1:5000/api/state';
//     const res = await fetch(url);
//     const data = await res.json();
//     console.log(data);
//     state.set(data);
// };

export const fetchAllProcessInfo = async() =>{
    const url = 'http://127.0.0.1:5000/api/allProcessInfo';
    const res = await fetch(url);
    const data = await res.json();
    const loaded = data.map((data) =>{
        return{
            name: data.name,
            description: data.description,
            exitstatus: data.exitstatus,
            group: data.group,
            logfile: data.logfile,
            now: data.now,
            pid: data.pid,
            spawnerr: data.spawnerr,
            start: data.start,
            state: data.state,
            statename: data.statename,
            stderr_logfile: data.stderr_logfile,
            stdout_logfile: data.stdout_logfile,
            stop: data.stop
        };
    });
    allProcessInfo.set(loaded);
}
setInterval(fetchAllProcessInfo, 1000);



// export const fetchNames = async(name) =>{
//     const url = `http://127.0.0.0:5000/api/processInfo/${name}`;
//     const res = await fetch(url);
//     const data = await res.json();
//     console.log(data);
//     processName.set(data);
// }

// fetchState();

// fetchNames();
