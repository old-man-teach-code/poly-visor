<script lang="ts">
	import { dashboardEnabled, chartInstances, cpuChart, ramChart } from '../../store/supstore';
	let chartCount = Number(localStorage.chartInstances);

	function handleDasboardToggle() {
		dashboardEnabled.set($dashboardEnabled == 'true' ? 'false' : 'true');
	}

	function handleChartInterval() {
		if (chartCount < 3) alert('Chart instances too low!');
		if (typeof chartCount !== 'number') alert('Chart instances must be number!');
		chartInstances.set(chartCount);
		cpuChart.set(Array(Number(localStorage.chartInstances)));
		ramChart.set(Array(Number(localStorage.chartInstances)));
	}
</script>

<div class="flex flex-col items-start justify-center gap-12 mx-auto">
	<div class="flex gap-3">
		<span>Dashboard API</span>
		<button
			on:click={handleDasboardToggle}
			type="button"
			class="{$dashboardEnabled == 'true' ? 'bg-green-200' : 'bg-red-200'}
inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out "
			role="switch"
			aria-checked="false"
		>
			<!-- Enabled: "translate-x-5", Not Enabled: "translate-x-0" -->
			<span
				aria-hidden="true"
				class="
  {$dashboardEnabled == 'true' ? 'translate-x-5' : 'translate-x-0'}
  pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
			/>
		</button>
	</div>
	<div>
		<div class="flex flex-col gap-3">
			<span>Chart instances</span>
			<div class="flex items-center gap-3">
				<input
					type="number"
					bind:value={chartCount}
					min="3"
					class="rounded-md border-none shadow-md focus:ring-orange-300"
				/>
				<button
					on:click={handleChartInterval}
					class="rounded-lg bg-green-300 px-3 py-1.5 hover:bg-green-500">Save</button
				>
			</div>
		</div>
	</div>
</div>
