<script lang="ts">
	import { createEventDispatcher, onDestroy, onMount, afterUpdate } from 'svelte';
	import { writable } from 'svelte/store';
	import ClearLogButton from './Buttons/ClearLogButton.svelte';
	import CloseButton from './Buttons/CloseButton.svelte';
	import PlayPauseButton from './Buttons/PlayPauseButton.svelte';
	import StartButton from './Buttons/StartButton.svelte';
	import StopButton from './Buttons/StopButton.svelte';
	import ToolTip from './ToolTip.svelte';

	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');
	export let content: String;
	export let log: Boolean;
	export let stream: String;
	export let name: String;
	let modal: HTMLElement;
	let scroll = true;
	let logState: Boolean = true;
	let logStore: string;
	const processLog = writable('');

	if (log) {
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
{#if log}
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
						processLog.set('');
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
{:else}
	<div class="modal-background" on:click={close} />
	<div class="modal p-10" role="dialog" aria-modal="true" bind:this={modal}>
		<div class="flex justify-end">
			<CloseButton on:event={close} />
		</div>
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
		<hr />
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
		max-height: 42rem;
		overflow: auto;
		transform: translate(-50%, -50%);
		border-radius: 0.2em;
		background: white;
	}
</style>
