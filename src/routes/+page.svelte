<script>
    import {system} from "../store/supstore";
    import {processes} from "../store/supstore";
    import {count} from "../store/supstore";

    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';


    console.log(JSON.stringify($system.cpulist));
	let chartValues = [20.9, 10.1, 5.6, 2.1, 20.5, 30.4, 45.5];
	let chartLabels = [60,50,40,30,20,10,0];

	let chartCanvas;

	onMount(async (promise) => {
		  let ctx = chartCanvas.getContext('2d');
			var chart = new Chart(ctx, {
				type: 'line',
				data: {
						labels: chartLabels,
						datasets: [{
								label: 'CPU %',
								backgroundColor: 'rgb(255, 99, 132)',
								borderColor: 'rgb(255, 99, 132)',
								data: chartValues
						}]
				}
		});
	});

</script>
<div class="w-full px-10">
    <h1 class=" pt-5 text-2xl font-semibold">Overview</h1>
        <div class="grid text-center justify-items-center items-end gap-5 grid-cols-4 grid-rows-4">
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">CPU Usage</h1><h4>{$system.cpu}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Ram Usage</h1><h4>{$system.memory}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Running process</h1><h4>{$count}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Total process</h1><h4>{Object.keys($processes).length}</h4></div>
            <div class="border-2 bg-white w-full h-full rounded-xl row-span-3 col-span-4" >
                <canvas class="p-5" bind:this={chartCanvas} id="myChart"></canvas>
            </div>
        </div>
</div>

    
