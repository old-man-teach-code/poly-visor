<script>
	import { system } from '../store/supstore';
	import { processes } from '../store/supstore';
	import { count } from '../store/supstore';
	import { chartJS } from '../store/action.js';
	import { cpuCount } from '../store/supstore';

	//Variables for storing data as an array for chartJS
	let chartCpuData = Array(31);
	let chartRamData = Array(31);
	let chart;
	let textCpu = 'text-[#FF8C32]'; //initial text color fo0r CPU as orange
	let textRam;

	//Initial data for ChartJS
	let data = {
		type: 'line',
		data: {
			//X axis data label
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
			//set default dataset as CPU
			datasets: [
				{
					label: 'CPU %',
					backgroundColor: '#FF8C32',
					borderColor: 'rgb(255, 99, 132)',
					data: chartCpuData
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
				//Y axis min max data value
				y: {
					suggestedMin: 0,
					suggestedMax: 50
				}
			}
		}
	};

	//Reactive function, changing datasets when swapping between CPU and Ram
	$: if (chart == 'CPU %') {
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
			ds.data = chartCpuData;
		});
		data.options.plugins.title.text = 'Overall CPU usage';
		textCpu = 'text-[#FF8C32]';
		textRam = 'text-black';
	} else if (chart == 'RAM %') {
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
			ds.data = chartRamData;
		});
		data.options.plugins.title.text = 'Overall RAM usage';
		textCpu = 'text-black';
		textRam = 'text-[#FF8C32]';
	}

	//function for handling CPU's chart
	function chartCpu() {
		chart = 'CPU %';
	}
	//Function for handling RAM's chart
	function chartRam() {
		chart = 'RAM %';
	}

	//Push new data from the API every 2 seconds
	setInterval(() => {
		chartCpuData.shift();
		chartCpuData.push($system.cpu);
		chartRamData.shift();
		chartRamData.push($system.memory);
		data = data;
	}, 2000);
</script>

<div class="w-full h-full px-10">
	<h1 class=" pt-5 text-2xl font-semibold">Overview</h1>
	<div class="grid text-center justify-items-center items-end gap-4 grid-cols-4 grid-rows-4">
		<button
			class="hover:text-2xl border-2 bg-white w-full h-32 rounded-md {textCpu}"
			on:click={chartCpu}
		>
			<h1 class="text-xl">CPU Usage</h1>
			<h4>{$system.cpu}%</h4>
		</button>
		<button
			class="hover:text-2xl border-2 bg-white w-full h-32 rounded-md {textRam}"
			on:click={chartRam}
		>
			<h1 class="text-xl">Ram Usage</h1>
			<h4>{$system.memory}%</h4>
		</button>
		<div class="border-2 bg-white w-full h-32 rounded-md">
			<h1 class="text-xl pt-9">Number of cores</h1>
			<h4>{$cpuCount}</h4>
		</div>
		<div class="border-2 bg-white w-full h-32 rounded-md">
			<h1 class="text-xl pt-9">Running process</h1>
			<h4>{$count}/{Object.keys($processes).length}</h4>
		</div>
		<div class="border-2 bg-white w-3/4 rounded-md row-span-3 col-span-4">
			<canvas class="p-2" use:chartJS={data} id="myChart" />
		</div>
	</div>
</div>
7
