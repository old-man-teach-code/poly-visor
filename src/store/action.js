//ChartJS import
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
    Tooltip,
} from 'chart.js';

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
export function chartJS(node, config) {
    const ctx = node.getContext('2d');
    chart = new Chart(ctx, config)
    return {
        update(newConfig) {
            chart.data = newConfig.data;
            Object.assign(chart.options, newConfig.options);
            chart.update();
        },
        destroy() {
            chart.destroy();
        }
    }
}

export function destroyChart() {
    chart.destroy();
}

