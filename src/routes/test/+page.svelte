<script>
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

	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	let values;
	let showModal = 'close';
	let modalContent;

	const messages = writable([]);
	const processes = writable('');
	onMount(async () => {
		let eventSource = new EventSource('http://127.0.0.1:5000/process/out/demo');
		eventSource.onmessage = (event) => {
			let dataProcesses = JSON.parse(event.data);
			processes.update((items) => {
				items += dataProcesses.message;
				return items;
			});
		};
	});
</script>

<div class="w-64 h-52">{$processes}</div>
