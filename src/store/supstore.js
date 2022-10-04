import { writable} from "svelte/store";

export const state = writable([]);
export const allProcessInfo = writable([]);

export const fetchAll = async() =>{
    // fetch state
    const resState = await fetch('http://127.0.0.1:5000/api/state');
    const dataState = await resState.json();
    state.set(dataState);
    // fetch all process info
    const resAllProcessInfo = await fetch('http://127.0.0.1:5000/api/allProcessInfo');
    const dataAllProcessInfo = await resAllProcessInfo.json();
    allProcessInfo.set(dataAllProcessInfo);
}
setInterval(fetchAll, 1000);
