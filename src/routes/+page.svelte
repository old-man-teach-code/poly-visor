<script>
	import { system } from '../store/supstore';
	import { processes } from '../store/supstore';
	import { count } from '../store/supstore';
	import { chartJS } from '../store/action.js';
	import { disableScrollHandling } from '$app/navigation';

	let data = {
		type: 'line',
		data: {
			labels: [
				'60s',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'',
				'0s'
			],
			datasets: [
				{
					label: 'CPU %',
					backgroundColor: '#FF8C32',
					borderColor: 'rgb(255, 99, 132)',
					data: Array(31)
				}
			]
		},
		options: {
			fill: true,
			responsive: true,
			maintainAspectRatio: true,
			plugins: {
				legend: {
					position: 'top'
				},
				title: {
					display: true,
					text: 'Overall CPU usage'
				}
			},
			scales: {
				y: {
					suggestedMin: 0,
					suggestedMax: 50
				}
			}
		}
	};

	$: chartData = $system.cpu;
	let chart;
	let textCpu = 'text-[#FF8C32]';
	let textRam;
	$: if (chart == 'CPU %') {
		chartData = $system.cpu;
		data.options.plugins.title.text = 'Overall CPU usage';
		textCpu = 'text-[#FF8C32]';
		textRam = 'text-black';
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
		});
	} else if (chart == 'RAM %') {
		chartData = $system.memory;
		data.options.plugins.title.text = 'Overall RAM usage';
		textCpu = 'text-black';
		textRam = 'text-[#FF8C32]';
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
		});
	}

	function chartCpu() {
		chart = 'CPU %';
		data.data.datasets.forEach((ds) => {
			ds.data = Array(31);
		});
	}

	function chartRam() {
		chart = 'RAM %';
		data.data.datasets.forEach((ds) => {
			ds.data = Array(31);
		});
	}

	setInterval(() => {
		data.data.datasets.forEach((ds) => {
			ds.data.shift();
			ds.data.push(chartData);
		});
		data = data;
	}, 2000);
</script>

<div class="w-full h-screen px-10">
	<h1 class=" pt-5 text-2xl font-semibold">Overview</h1>
	<div class="grid text-center justify-items-center items-end gap-5 grid-cols-4 grid-rows-4">
		<button class="border-2 bg-white w-full h-32 rounded-xl {textCpu}" on:click={chartCpu}>
			<h1 class="text-xl">CPU Usage</h1>
			<h4>{$system.cpu}%</h4>
		</button>
		<button class="border-2 bg-white w-full h-32 rounded-xl {textRam}" on:click={chartRam}>
			<h1 class="text-xl">Ram Usage</h1>
			<h4>{$system.memory}%</h4>
		</button>
		<div class="border-2 bg-white w-full h-32 rounded-xl">
			<h1 class="text-xl pt-9">Running process</h1>
			<h4>{$count}</h4>
		</div>
		<div class="border-2 bg-white w-full h-32 rounded-xl">
			<h1 class="text-xl pt-9">Total process</h1>
			<h4>{Object.keys($processes).length}</h4>
		</div>
		<div class="border-2 bg-white w-3/4 rounded-xl row-span-3 col-span-4">
			<canvas class="p-2" use:chartJS={data} id="myChart" />
		</div>
	</div>
</div>
