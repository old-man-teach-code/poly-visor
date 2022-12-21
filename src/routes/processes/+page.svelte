<script lang="ts">
	import { processes } from '../../store/supstore';
	import Pagination from '../../components/Pagination.svelte';
	import StartButton from '../../components/Buttons/StartButton.svelte';
	import StopButton from '../../components/Buttons/StopButton.svelte';
	import ViewButton from '../../components/Buttons/ViewButton.svelte';
	import LogButton from '../../components/Buttons/LogButton.svelte';
	import { startProcess } from '../../store/action.js';
	import { startAllProcess } from '../../store/action.js';
	import { stopProcess } from '../../store/action.js';
	import { stopAllProcess } from '../../store/action.js';
	import ToolTip from '../../components/ToolTip.svelte';
	import Modal from '../../components/Modal.svelte';
	import AddButton from '../../components/Buttons/AddButton.svelte';
	import Selector from '../../components/Selector.svelte';
	import TextInput from '../../components/TextInput.svelte';

	let values: Object;
	let showModal = 'close';
	let modalContent: String;
	let logName: String;
	let logStream: String;
	let filter = new Array();
	let search: string;
	let tableRows;

	$: if (search) {
		tableRows = $processes.filter(
			(process) =>
				filter.includes(process.statename) &&
				process.name.toLowerCase().includes(search.toLocaleLowerCase())
		);
	} else {
		tableRows = $processes.filter((process) => filter.includes(process.statename));
	}
</script>

<div class="w-full h-screen px-10">
	<h1 class="pt-5 text-2xl font-semibold">Processes</h1>
	<div class="border-2 bg-white w-full min-h-fit rounded-md mt-10">
		<div class="flex justify-between">
			<h3 class="py-10 pl-10 font-bold">All Processes</h3>
			<div class="flex items-center">
				<ToolTip title="Add new process">
					<AddButton
						on:event={() => {
							showModal = 'addProcess';
						}}
					/>
				</ToolTip>
			</div>
			<div class="flex items-center pr-24">
				<ToolTip title="Start all processes">
					<StartButton spin={false} on:event={() => startAllProcess()} />
				</ToolTip>
				<ToolTip title="Stop all processes">
					<StopButton spin={false} on:event={() => stopAllProcess()} />
				</ToolTip>
			</div>
		</div>
		<!-- options={['RUNNING', 'STOPPED', 'STARTING', 'BACKOFF', 'FATAL']} -->
		<!-- on:event={handleFilter} -->
		<div class="flex justify-between">
			<div class="pl-5 pb-5">
				<TextInput inputPlaceholder="Search" bind:inputValue={search} />
			</div>
			<Selector
				bind:result={filter}
				title="Status"
				options={['RUNNING', 'STARTING', 'BACKOFF', 'STOPPED', 'FATAL']}
			/>
		</div>
		<!-- <hr class="mb-10 mx-5" /> -->
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
												error={false}
												on:event={() => {
													showModal = 'Log';
													logName = process.name;
													logStream = 'out';
												}}
											/></ToolTip
										>
										<ToolTip title="View error log"
											><LogButton
												error
												on:event={() => {
													showModal = 'Log';
													logName = process.name;
													logStream = 'err';
												}}
											/></ToolTip
										>
										<ToolTip title="View process detail">
											<ViewButton
												spin={false}
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
						<td class="py-3 px-6 text-center" />
					{/if}
				</tbody>
			</table>
			<Pagination rows={tableRows} perPage={5} bind:trimmedRows={values} />
			{#if showModal != 'close'}
				{#if showModal == 'Log'}
					<Modal
						content=""
						modalType="log"
						on:close={() => (showModal = 'close')}
						name={logName}
						stream={logStream}
					/>
				{:else if showModal == 'Detail'}
					<Modal
						content={modalContent}
						modalType="detail"
						stream=""
						name=""
						on:close={() => (showModal = 'close')}
					/>
				{:else if showModal == 'addProcess'}
					<Modal
						content=""
						modalType="addProcess"
						stream=""
						name=""
						on:close={() => (showModal = 'close')}
					/>
				{/if}
			{/if}
		</div>
	</div>
</div>
