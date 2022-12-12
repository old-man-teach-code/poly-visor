<script>
	import { system } from '../store/supstore';
	import { processes } from '../store/supstore';
	import { count } from '../store/supstore';
	import { chartJS } from '../store/action.js';
	import { cpuCount } from '../store/supstore';
	import { cpuChart } from '../store/supstore';
	import { ramChart } from '../store/supstore.js';
	import Card from '../components/Card.svelte';
	import CpuCore from '../components/cpuCore.svelte';

	let chart;
	let textCpu = 'text-[#FF8C32]'; //initial text color for CPU as orange
	let textRam;
	let textCores;
	let chartState = true;

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
					data: $cpuChart
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
			ds.data = $cpuChart;
		});
		data.options.plugins.title.text = 'Overall CPU usage';
		textCpu = 'text-[#FF8C32]';
		textRam = 'text-black';
		textCores = 'text-black';
	} else if (chart == 'RAM %') {
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
			ds.data = $ramChart;
		});
		data.options.plugins.title.text = 'Overall RAM usage';
		textCpu = 'text-black';
		textRam = 'text-[#FF8C32]';
		textCores = 'text-black';
	} else if (chart == 'Cores') {
		textCpu = 'text-black';
		textRam = 'text-black';
		textCores = 'text-[#FF8C32]';
	}
	//function for handling CPU's chart
	function chartCpu() {
		chartState = true;
		chart = 'CPU %';
	}
	//Function for handling RAM's chart
	function chartRam() {
		chartState = true;
		chart = 'RAM %';
	}
	function chartCores() {
		chartState = false;
		chart = 'Cores';
	}

	//Chart data get updated whenever the writable change
	$: if ($cpuChart) {
		data = data;
	}
</script>

<div class="w-full h-screen px-10">
	<h1 class=" pt-5 text-2xl font-semibold">Overview</h1>
	<div class="grid text-center justify-items-center gap-4 grid-cols-4 grid-rows-4">
		<Card color={textCpu} content="{$system.cpu}%" title="Cpu Usage" on:event={chartCpu} />
		<Card color={textRam} content="{$system.memory}%" title="Ram Usage" on:event={chartRam} />
		<Card color={textCores} content={$cpuCount} title="Number of cores" on:event={chartCores} />
		<Card
			content="{$count}/{Object.keys($processes).length}"
			color="null"
			title="Running processes"
			on:event={() => {
				window.location.replace('/processes');
			}}
		/>
		{#if chartState}
			<div class="border-2 bg-white w-3/4 rounded-md row-span-3 col-span-4">
				<canvas class="p-2" use:chartJS={data} id="myChart" />
			</div>
		{:else}
			{#each Object.entries($system.cores) as [key, value]}
				<CpuCore coreName={key} coreValue={value} />
			{/each}
		{/if}
	</div>
</div>
