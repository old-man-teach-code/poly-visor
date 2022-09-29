import { writable } from "svelte/store";

export const supervisor = writable([]);

const fetchSupervisor = async () =>{
    const url = 'http://127.0.0.1:5000/api/state';
    console.log('fetching supervisor');
    const response = await fetch(url);
    console.log('fetching supervisor 2');
    const data = await response.json();   
    supervisor.set(data);
}
fetchSupervisor();