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
	import ArrowButton from './Buttons/ArrowButton.svelte';
	import {renderProcessConf} from '../store/action';
	import EditButton from './Buttons/EditButton.svelte';

	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');
	export let content: String;
	export let modalType: String;
	export let stream: String;
	export let name: string;
	let modal: HTMLElement;
	let scroll = true;
	let logState: Boolean = true;
	let logStore: string;
	let eventSource: EventSource;
	let required: Boolean = false;
	const processLog = writable('');

	let conf = {
		process_full_name: '',
		command: '',
		numprocs: '1',
		umask: '022',
		numprocs_start: '0',
		priority: '999',
		autostart: 'true',
		autorestart: 'true',
		startsecs: '1',
		startretries: '3',
		exitcodes: '0',
		stopsignal: 'TERM',
		stopwaitsecs: '10',
		stopasgroup: 'false',
		killasgroup: 'false',
		redirect_stderr: 'false',
		stdout_logfile_maxbytes: '50MB',
		stdout_logfile_backups: '10',
		stdout_capture_maxbytes: '0',
		stdout_events_enabled: 'false',
		stdout_syslog: 'false',
		stderr_logfile_maxbytes: '50MB',
		stderr_logfile_backups: '10',
		stderr_capture_maxbytes: '0',
		stderr_events_enabled: 'false',
		stderr_syslog: 'false',
		environment: '',
		serverurl: 'AUTO',
		directory: '/tmp',
		stdout_logfile:'AUTO',
		stderr_logfile:'AUTO',
		edit:false
	};

	if (modalType === 'log') {
		onMount(() => {
			eventSource = new EventSource(`http://localhost:5000/process/${stream}/${name}`);
			eventSource.onmessage = (event) => {
				let dataProcesses = JSON.parse(event.data);
				if (logState) {
					processLog.update((n) => dataProcesses.message);
				}
			};
		});
		afterUpdate(() => {
			if (scroll) {
				scrollToBottom(modal);
			}
		});
	}else if(modalType === 'editProcess'){
		//map the return of renderObjectConf to conf
		renderProcessConf(name).then((data) => {
			conf = data;
			conf.process_full_name = name;
			conf.edit = true;
		});
		
	}
	const scrollToBottom = async (node) => {
		node.scroll({ top: node.scrollHeight });
	};

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
	<div class="modal-background" on:click={()=>{
		close();
		eventSource.close();
	}} />
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
					<CloseButton on:event={()=> {
							close();
							eventSource.close()
						
						}} />
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
	<div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
		<div class="sticky top-0 bg-orange-200 py-5 flex items-center justify-between px-10">
			<h1 class="font-bold text-xl">Process detail</h1>
			<CloseButton on:event={close} />
		</div>
		<hr class="pb-5" />
		<div class="p-10 flex flex-col space-y-5">
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
		</div>
		<hr class="mt-5" />
		<!-- svelte-ignore a11y-autofocus -->
	</div>
{:else if modalType === 'addProcess' || modalType === 'editProcess'}
	<div class="modal-background" on:click={close} />
	<div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
		<div class="sticky top-0 bg-orange-200 py-5 flex items-center justify-between px-10">
			{#if modalType === 'addProcess'}
				<h1 class="font-bold text-xl">Add new process</h1>
			{:else if modalType === 'editProcess'}
				<h1 class="font-bold text-xl">Edit <span class="text-orange-400">{conf.process_full_name} </span>process</h1>
			{/if}
			<CloseButton on:event={close} />
		</div>
		<div class="p-10 flex flex-col space-y-5">
			{#if modalType === 'addProcess'}
				<Input
					bind:inputValue={conf.process_full_name}
					inputLabel="Process Name"
					inputPlaceholder="Name of the process"
				/>
			{/if}
			<Input
				bind:inputValue={conf.command}
				inputLabel="Command"
				inputPlaceholder="Command to run"
			/>
			<div class="flex justify-center">
				<ToolTip title={required ? 'Hide non-required config' : 'Show non-required config'}>
					<ArrowButton
						direction={required ? 'up' : 'down'}
						on:event={() => {
							required = !required;
						}}
					/></ToolTip
				>
			</div>
			{#if required}
				<Input
					bind:inputValue={conf.numprocs}
					inputLabel="Numbprocs"
					inputPlaceholder="Instances of the process to run"
				/>
				<Input
					bind:inputValue={conf.umask}
					inputLabel="Umask"
					inputPlaceholder="Umask of the process"
				/>
				<Input
					bind:inputValue={conf.numprocs_start}
					inputLabel="Numprocs_start"
					inputPlaceholder="Offset integer used to compute the number at which process_num starts"
				/>
				<Input
					bind:inputValue={conf.priority}
					inputLabel="Priority"
					inputPlaceholder="Start and shutdown order of the process"
				/>
				<Input
					bind:inputValue={conf.autostart}
					inputLabel="Autostart"
					inputPlaceholder="Autostart the process"
				/>
				<Input
					bind:inputValue={conf.autorestart}
					inputLabel="Autorestart"
					inputPlaceholder="Autorestart the process"
				/>
				<Input
					bind:inputValue={conf.startsecs}
					inputLabel="Startsecs"
					inputPlaceholder="Number of seconds to wait before running the process"
				/>
				<Input
					bind:inputValue={conf.startretries}
					inputLabel="Startretries"
					inputPlaceholder="Number of retries to attempt to start the process"
				/>
				<Input
					bind:inputValue={conf.exitcodes}
					inputLabel="Exitcodes"
					inputPlaceholder="List of exit codes that will be use with auto restart"
				/>
				<Input
					bind:inputValue={conf.stopsignal}
					inputLabel="Stopsignal"
					inputPlaceholder="Signal used to stop the process"
				/>
				<Input
					bind:inputValue={conf.stopwaitsecs}
					inputLabel="Stopwaitsecs"
					inputPlaceholder="Number of seconds to wait before killing the process"
				/>
				<Input
					bind:inputValue={conf.stopasgroup}
					inputLabel="Stopasgroup"
					inputPlaceholder="Send stop signal to the process group"
				/>
				<Input
					bind:inputValue={conf.killasgroup}
					inputLabel="Killasgroup"
					inputPlaceholder="Send kill signal to the process group"
				/>
				<Input
					bind:inputValue={conf.redirect_stderr}
					inputLabel="Redirect_stderr"
					inputPlaceholder="Redirect stderr to stdout"
				/>
				<Input
					bind:inputValue={conf.stdout_logfile_maxbytes}
					inputLabel="Stdout_logfile_maxbytes"
					inputPlaceholder="Max size of the stdout log file"
				/>
				<Input
					bind:inputValue={conf.stdout_logfile_backups}
					inputLabel="Stdout_logfile_backups"
					inputPlaceholder="Number of stdout log files to keep"
				/>
				<Input
					bind:inputValue={conf.stdout_capture_maxbytes}
					inputLabel="Stdout_capture_maxbytes"
					inputPlaceholder="Max size of the stdout capture"
				/>
				<Input
					bind:inputValue={conf.stdout_events_enabled}
					inputLabel="Stdout_events_enabled"
					inputPlaceholder="Enable stdout events"
				/>
				<Input
					bind:inputValue={conf.stdout_syslog}
					inputLabel="Stdout_syslog"
					inputPlaceholder="Send stdout to syslog"
				/>
				<Input
					bind:inputValue={conf.stderr_logfile_maxbytes}
					inputLabel="Stderr_logfile_maxbytes"
					inputPlaceholder="Max size of the stderr log file"
				/>
				<Input
					bind:inputValue={conf.stderr_logfile_backups}
					inputLabel="Stderr_logfile_backups"
					inputPlaceholder="Number of stderr log files to keep"
				/>
				<Input
					bind:inputValue={conf.stderr_capture_maxbytes}
					inputLabel="Stderr_capture_maxbytes"
					inputPlaceholder="Max size of the stderr capture"
				/>
				<Input
					bind:inputValue={conf.stderr_events_enabled}
					inputLabel="Stderr_events_enabled"
					inputPlaceholder="Enable stderr events"
				/>
				<Input
					bind:inputValue={conf.stderr_syslog}
					inputLabel="Stderr_syslog"
					inputPlaceholder="Send stderr to syslog"
				/>
				<Input bind:inputValue={conf.environment} inputLabel="Environment" inputPlaceholder="" />
				<Input
					bind:inputValue={conf.serverurl}
					inputLabel="Serverurl"
					inputPlaceholder="Server url for the process"
				/>
				<Input
				bind:inputValue={conf.stdout_logfile}
				inputLabel="Stdout_logfile"
				inputPlaceholder="Log file location"
			/>
			<Input
				bind:inputValue={conf.stderr_logfile}
				inputLabel="Stderr_logfile"
				inputPlaceholder="Error log file location"
			/>
			{/if}
			<div class="pt-5 place-self-center">
				{#if modalType === 'addProcess'}
					<ToolTip title="Add process config">
						<AddButton
							on:event={() => {
								addNewProcessConf(conf);
							}}
						/>
					</ToolTip>
				{:else if modalType === 'editProcess'}
					<ToolTip title="Edit process config">
						<EditButton
							on:event={() => {
								addNewProcessConf(conf);
							}}
						/>
					</ToolTip>
				{/if}
			</div>
		</div>
		<!-- svelte-ignore a11y-autofocus -->
	</div>
{/if}

<style>
	.modal-background {
		z-index: 10;
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.621);
	}

	.modal {
		z-index: 10;
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
