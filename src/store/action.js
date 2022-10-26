import Chart from 'chart.js/auto';

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