<script>
	import { processes } from '../../store/supstore';
	import Pagination from '../../components/Pagination.svelte';
	import StartButton from '../../components/StartButton.svelte';
	import StopButton from '../../components/StopButton.svelte';
	import ViewButton from '../../components/ViewButton.svelte';
	import LogButton from '../../components/LogButton.svelte';
	import { startProcess } from '../../store/action.js';
	import { startAllProcess } from '../../store/action.js';
	import { stopProcess } from '../../store/action.js';
	import { stopAllProcess } from '../../store/action.js';
	import ToolTip from '../../components/toolTip.svelte';
	import Modal from '../../components/Modal.svelte';
	import { viewProcessLog } from '../../store/action.js';

	let values;
	let showModal = 'close';
	let modalContent;

	function getProcess(name) {}
</script>

<div class="w-full h-screen px-10">
	<h1 class=" pt-5 text-2xl font-semibold">Processes</h1>
	<div class="border-2 bg-white w-full h-5/6 rounded-md mt-10">
		<div class="flex justify-between">
			<h3 class="p-10 font-bold">All Processes</h3>
			<div class="flex items-center pr-16">
				<ToolTip title="Start all processes">
					<StartButton on:event={() => startAllProcess()} />
				</ToolTip>
				<ToolTip title="Stop all processes">
					<StopButton on:event={() => stopAllProcess()} />
				</ToolTip>
			</div>
		</div>
		<div class="overflow-auto flex flex-col items-center">
			<table class="min-w-full w-full table-auto">
				<thead>
					<tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
						<th class="py-3 px-6 text-left">Process name</th>
						<th class="py-3 px-6 text-left">Description</th>
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
										<span>{process.description}</span>
									</div>
								</td>
								<td class="py-3 px-6 text-center">
									<span class="{process.stateColor} py-1 px-3 rounded-full text-xs"
										>{process.statename}</span
									>
								</td>
								<td class="py-3 px-6 text-center">
									<div class="flex item-center justify-center">
										{#if process.statename != 'STOPPED'}
											<ToolTip title="Stop this process">
												<StopButton spin on:event={() => stopProcess(process.name)} />
											</ToolTip>
										{:else}
											<ToolTip title="Start this process">
												<StartButton spin on:event={() => startProcess(process.name)} />
											</ToolTip>
										{/if}
										<ToolTip title="View process log"
											><LogButton
												on:event={() => {
													showModal = 'Log';
													modalContent = viewProcessLog(process.name);
												}}
											/></ToolTip
										>
										<ToolTip title="View process detail">
											<ViewButton
												on:event={() => {
													showModal = 'Detail';
													modalContent = process;
												}}
											/>
										</ToolTip>
									</div>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
			<Pagination rows={$processes} perPage={5} bind:trimmedRows={values} />
			{#if showModal != 'close'}
				<Modal on:close={() => (showModal = 'close')}>
					{#if showModal == 'Log'}
						{modalContent}
					{:else if showModal == 'Detail'}
						Description: {modalContent.description}
						<br />
						Exit status: {modalContent.exitstatus}
						<br />
						Group: {modalContent.group}
						<br />
						Log file: {modalContent.logfile}
						<br />
						Name: {modalContent.name}
						<br />
						Pid: {modalContent.pid}
						<br />
						Spawnerr: {modalContent.spawnerr}
						<br />
						Start: {modalContent.start}
						<br />
						State: {modalContent.state}
						<br />
						State name: {modalContent.statename}
						<br />
						Error log file: {modalContent.stderr_logfile}
						<br />
						Out log file: {modalContent.stdout_logfile}
						<br />
						Stop: {modalContent.stop}
						<br />
					{/if}
				</Modal>
			{/if}
		</div>
	</div>
</div>