<script lang="ts">
	import { system } from '../store/supstore';
	import { processes } from '../store/supstore';
	import { count } from '../store/supstore';
	import { chartJS } from '../store/action.js';
	import { cpuCount } from '../store/supstore';
	import { cpuChart } from '../store/supstore';
	import { ramChart } from '../store/supstore.js';
	import Card from '../components/Card.svelte';
	import CpuCore from '../components/CpuCore.svelte';
	import { page } from '$app/stores';

	let chart: any;
	let textCpu: Boolean = true; //initial text color for CPU as orange
	let textRam: Boolean;
	let textCores: Boolean;
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
			resizeDelay: 0,
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
		textCpu = true;
		textRam = false;
		textCores = false;
	} else if (chart == 'RAM %') {
		data.data.datasets.forEach((ds) => {
			ds.label = chart;
			ds.data = $ramChart;
		});
		data.options.plugins.title.text = 'Overall RAM usage';
		textCpu = false;
		textRam = true;
		textCores = false;
	} else if (chart == 'Cores') {
		textCpu = false;
		textRam = false;
		textCores = true;
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

<div class="px-10 space-y-5 mb-5 flex flex-col w-full">
	<h1 class="text-2xl font-semibold mt-5">Overview</h1>
	<div class="flex flex-col gap-5">
		<div class="grid xl:grid-cols-4 grid-cols-2 gap-7">
			<Card enabled={textCpu} content="{$system.cpu}%" title="Cpu Usage" on:event={chartCpu} />
			<Card enabled={textRam} content="{$system.memory}%" title="Ram Usage" on:event={chartRam} />
			<Card enabled={textCores} content={$cpuCount} title="Number of cores" on:event={chartCores} />
			<a class="" href="/processes">
				<Card
					content="{$count}/{Object.keys($processes).length}"
					enabled={false}
					title="Running processes"
				/>
			</a>
		</div>
	</div>
	{#if chartState}
		<div class="flex flex-1 justify-center">
			<div class="relative bg-white border-2 rounded-md h-4/5 w-11/12 lg:w-3/4 min-h-[300px]">
				<canvas class="p-2" use:chartJS={data} id="myChart" />
			</div>
		</div>
	{:else}
		<div class="grid lg:grid-cols-4 grid-cols-2 justify-items-center place-content-center gap-10">
			{#each Object.entries($system.cores) as [key, value]}
				<CpuCore coreName={key} coreValue={value} />
			{/each}
		</div>
	{/if}
</div>
