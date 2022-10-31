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

export function chartJS(node, config) {
    const ctx = node.getContext('2d');
    const chart = new Chart(ctx, config)
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

['60s','58s','56s','54s','52s','50s','48s','46s','44s','42s','40s','38s','36s','34s','32s','30s','28s','26s','24s','22s','20s','18s','16s','14s','12s','10s','8s','6s','4s','2s','0s']