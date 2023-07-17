//ChartJS import
// import chartjs from 'chart.js';
import { Chart, LineElement, PointElement, LineController, CategoryScale, LinearScale, Filler, Legend, Title, Tooltip } from 'chart.js';
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
    Tooltip,
);

let chart;
//ChartJS function for creating, updating. Delete chart when there's no param
export function chartJS(node, config)
{
    const ctx = node.getContext('2d');
    chart = new Chart(ctx, config)
    return {
        update(newConfig)
        {
            chart.data = newConfig.data;
            Object.assign(chart.options, newConfig.options);
            chart.update();
        },
        destroy()
        {
            chart.destroy();
        }
    }
}

export function destroyChart()
{
    chart.destroy();
}


//call start process api
export async function startProcess(name)
{
    const res = await fetch(`/process/start/${name}`);
    const message = await res.json();
    return message;
}
export async function stopProcess(name)
{
    const res = await fetch(`/process/stop/${name}`);
    const message = await res.json();
    return message;
}
export async function startAllProcess()
{
    const res = await fetch('/processes/start');
    const message = await res.json();
    return message;
}
export async function stopAllProcess()
{
    const res = await fetch('/processes/stop');
    const message = await res.json();
    return message;
}

export async function addNewProcessConf(conf)
{
    console.log(conf)
    const res = await fetch('/config/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(conf)
    });
    const message = await res.json();
    alert(message.message)
    return message;
}


export async function renderProcessConf(name)
{
    const res = await fetch(`/config/render/${name}`);
    const data = await res.json();
    return data;
}

