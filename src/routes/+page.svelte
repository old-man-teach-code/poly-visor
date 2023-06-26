<script>
	import { system } from '../store/supstore';
	import { processes } from '../store/supstore';
	import { count } from '../store/supstore';
	import { chartJS } from '../store/action.js';
	import { cpuCount } from '../store/supstore';
	import { cpuChart } from '../store/supstore';
	import { ramChart } from '../store/supstore.js';
	import Card from '../components/Card.svelte';
	import CpuCore from '../components/CpuCore.svelte';

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
			maintainAspectRatio: false,
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

	let open = true;
	let innerWidth;
	$: if (innerWidth > 768) {
		open = true;
	}
</script>

<svelte:window bind:innerWidth />
<div class="w-full h-screen px-10 space-y-5">
	<h1 class="text-2xl font-semibold pt-5">Overview</h1>
	<div class="space-y-5 h-3/4">
		<div class="bg-[#FF8C32] flex justify-between px-3 rounded-md py-1 sm:hidden">
			<p class="text-lg text-white">Detail</p>
			<button
				class="text-white"
				on:click={() => {
					open = !open;
				}}
				><svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-6 h-6 transition-all duration-300 {open ? '' : 'rotate-180'}"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
				</svg>
			</button>
		</div>
		<div
			class="grid {open
				? '[grid-template-rows:1fr] max-sm:border-gray-300 max-sm:bg-white max-sm:border-2 max-sm:rounded-md'
				: '[grid-template-rows:0fr] opacity-0'} transition-all duration-300 p-4"
		>
			<div class="grid grid-cols-4 max-sm:grid-cols-1 max-md:grid-cols-2 gap-5 min-h-0">
				<Card color={textCpu} content="{$system.cpu}%" title="Cpu Usage" on:event={chartCpu} />
				<Card color={textRam} content="{$system.memory}%" title="Ram Usage" on:event={chartRam} />
				<Card color={textCores} content={$cpuCount} title="Number of cores" on:event={chartCores} />
				<a class="w-full" href="/processes">
					<Card
						content="{$count}/{Object.keys($processes).length}"
						color="null"
						title="Running processes"
					/>
				</a>
			</div>
		</div>
		{#if chartState}
			<div class="h-full flex justify-center">
				<div
					class="sm:w-3/4 w-full h-3/4 relative border-2 bg-white rounded-md flex justify-center"
				>
					<canvas class="p-2" use:chartJS={data} id="myChart" />
				</div>
			</div>
		{:else}
			<div
				class="grid grid-cols-4 max-md:grid-cols-2 justify-items-center place-content-center gap-10"
			>
				{#each Object.entries($system.cores) as [key, value]}
					<CpuCore coreName={key} coreValue={value} />
				{/each}
			</div>
		{/if}
	</div>
</div>
