<script>
	import { processes } from '../../store/supstore';
	import Pagination from '../../components/Pagination.svelte';
	import StartButton from '../../components/StartButton.svelte';
	import StopButton from '../../components/StopButton.svelte';
	import ViewButton from '../../components/ViewButton.svelte';
	let values;
	function Start() {
		console.log('stop');
	}
</script>

<div class="w-full h-screen px-10">
	<h1 class=" pt-5 text-2xl font-semibold">Processes</h1>
	<div class="border-2 bg-white w-full h-5/6 rounded-md mt-10">
		<h3 class="p-10 font-bold">All Processes</h3>
		<div class="w-full">
			<table class="min-w-max w-full table-auto">
				<thead>
					<tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
						<th class="py-3 px-6 text-left">Process name</th>
						<th class="py-3 px-6 text-left">UpTime</th>
						<th class="py-3 px-6 text-center">Status</th>
						<th class="py-3 px-6 text-center">Actions</th>
					</tr>
				</thead>
				<tbody class="text-gray-600 text-sm font-light">
					{#if values}
						{#each values as process}
							<tr class="border-b border-gray-200 hover:bg-gray-100">
								<td class="py-3 px-6 text-left whitespace-nowrap">
									<div class="flex items-center">
										<span class="font-medium">{process.name}</span>
									</div>
								</td>
								<td class="py-3 px-6 text-left">
									<div class="flex items-center">
										<div class="mr-2" />
										<span>none</span>
									</div>
								</td>
								<td class="py-3 px-6 text-center">
									<span class="{process.stateColor} py-1 px-3 rounded-full text-xs"
										>{process.statename}</span
									>
								</td>
								<td class="py-3 px-6 text-center">
									<div class="flex item-center justify-center">
										<StartButton on:start={Start} />
										<StopButton />
										<ViewButton />
									</div>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
			<Pagination rows={$processes} perPage={5} bind:trimmedRows={values} />
		</div>
	</div>
</div>
