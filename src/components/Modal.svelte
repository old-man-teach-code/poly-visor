<script lang="ts">
	import { createEventDispatcher, onDestroy, onMount, afterUpdate } from 'svelte';
	import { writable } from 'svelte/store';
	import ClearLogButton from './Buttons/ClearLogButton.svelte';
	import CloseButton from './Buttons/CloseButton.svelte';
	import PlayPauseButton from './Buttons/PlayPauseButton.svelte';
	import StartButton from './Buttons/StartButton.svelte';
	import StopButton from './Buttons/StopButton.svelte';
	import ToolTip from './ToolTip.svelte';
	import Input from './TextInput.svelte';
	import AddButton from './Buttons/AddButton.svelte';
	import { addNewProcessConf } from '../store/action';

	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');
	export let content: String;
	export let modalType: String;
	export let stream: String;
	export let name: String;
	let modal: HTMLElement;
	let scroll = true;
	let logState: Boolean = true;
	let logStore: string;
	let command: string;
	let processName: string;
	const processLog = writable('');

	if (modalType === 'log') {
		onMount(() => {
			let eventSource = new EventSource(`http://127.0.0.1:5000/process/${stream}/${name}`);
			eventSource.onmessage = (event) => {
				let dataProcesses = JSON.parse(event.data);
				logStore += dataProcesses.message;
				if (logState) {
					processLog.update((n) => logStore);
				}
			};
		});
	}
	const scrollToBottom = async (node) => {
		node.scroll({ top: node.scrollHeight });
	};
	afterUpdate(() => {
		if (scroll) {
			scrollToBottom(modal);
		}
	});

	const handle_keydown = (e) => {
		if (e.key === 'Escape') {
			close();
			return;
		}

		if (e.key === 'Tab') {
			// trap focus
			const nodes = modal.querySelectorAll('*');
			const tabbable = Array.from(nodes).filter((n) => n.tabIndex >= 0);

			let index = tabbable.indexOf(document.activeElement);
			if (index === -1 && e.shiftKey) index = 0;

			index += tabbable.length + (e.shiftKey ? -1 : 1);
			index %= tabbable.length;

			tabbable[index].focus();
			e.preventDefault();
		}
	};

	const previously_focused = typeof document !== 'undefined' && document.activeElement;

	if (previously_focused) {
		onDestroy(() => {
			previously_focused.focus();
		});
	}
</script>

<svelte:window on:keydown={handle_keydown} />
{#if modalType === 'log'}
	<div class="modal-background" on:click={close} />
	<div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
		<div class="sticky top-0 bg-orange-200 py-5 flex items-center justify-between">
			<div class="pl-8">
				<ToolTip title={scroll ? 'Stop auto scroll' : 'Auto scroll'}>
					<PlayPauseButton
						on:event={() => {
							scroll = !scroll;
						}}
					/>
				</ToolTip>
			</div>
			<ToolTip title={logState ? 'Pause' : 'Continue'}>
				{#if logState}
					<StopButton
						spin={false}
						on:event={() => {
							logState = !logState;
						}}
					/>
				{:else}
					<StartButton
						spin={false}
						on:event={() => {
							logState = !logState;
						}}
					/>
				{/if}
			</ToolTip>
			<ToolTip title="Clear process log">
				<ClearLogButton
					on:event={() => {
						logStore = '';
					}}
				/>
			</ToolTip>
			<div class="pr-5">
				<ToolTip title="Close log">
					<CloseButton on:event={close} />
				</ToolTip>
			</div>
		</div>
		<div class="p-10">
			<pre>
			{$processLog}
			</pre>
		</div>
		<hr />
		<!-- svelte-ignore a11y-autofocus -->
	</div>
{:else if modalType === 'detail'}
	<div class="modal-background" on:click={close} />
	<div class="modal px-10 py-6	" role="dialog" aria-modal="true" bind:this={modal}>
		<div class=" pb-5 flex justify-end">
			<CloseButton on:event={close} />
		</div>
		<hr class="pb-5" />
		Description: {content.description}
		<br />
		Exit status: {content.exitstatus}
		<br />
		Group: {content.group}
		<br />
		Log file: {content.logfile}
		<br />
		Name: {content.name}
		<br />
		Pid: {content.pid}
		<br />
		Spawnerr: {content.spawnerr}
		<br />
		Start: {content.start}
		<br />
		State: {content.state}
		<br />
		State name: {content.statename}
		<br />
		Error log file: {content.stderr_logfile}
		<br />
		Out log file: {content.stdout_logfile}
		<br />
		Stop: {content.stop}
		<br />
		<hr class="mt-5" />
		<!-- svelte-ignore a11y-autofocus -->
	</div>
{:else if modalType === 'addProcess'}
	<div class="modal-background" on:click={close} />
	<div class="modal px-10 py-8" role="dialog" aria-modal="true" bind:this={modal}>
		<div class="pb-5 flex justify-between">
			<h1>Add new process</h1>
			<CloseButton on:event={close} />
		</div>
		<hr />
		<div class=" pt-5 flex flex-col space-y-5">
			<Input
				bind:inputValue={processName}
				inputLabel="Process Name"
				inputPlaceholder="Name of the process"
			/>
			<Input
				bind:inputValue={command}
				inputLabel="Command"
				inputPlaceholder="full/path/to/process"
			/>
			<div class="pt-5 place-self-center">
				<ToolTip title="Add process config">
					<AddButton
						on:event={() => {
							addNewProcessConf(processName, command);
						}}
					/>
				</ToolTip>
			</div>
		</div>
		<!-- svelte-ignore a11y-autofocus -->
	</div>
{/if}

<style>
	.modal-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.621);
	}

	.modal {
		position: absolute;
		left: 50%;
		top: 50%;
		width: calc(100vw - 4em);
		max-width: 32em;
		max-height: calc(100vh - 4em);
		overflow: auto;
		transform: translate(-50%, -50%);
		border-radius: 0.2em;
		background: white;
	}
</style>
