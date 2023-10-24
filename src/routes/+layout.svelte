<script lang="ts">
	import Sidebar from '../components/SiderBar/index.svelte';
	import { page } from '$app/stores';
	import { onDestroy, onMount } from 'svelte';
	import {
		isAuthenticated,
		toggleProcessesInterval,
		toggleSystemInterval
	} from '../store/supstore.js';
	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	let eventSource: EventSource;

	onMount(() => {
		eventSource = new EventSource('/api/stream');
		eventSource.onmessage = (event) => {
			let data = JSON.parse(event.data);
			console.log(data);
		};
	});

	$: if ($isAuthenticated == 'false' && pathname != '/login') {
		window.location.href = '/login';
	}
	$: if ($isAuthenticated == 'true' && pathname != '/login') {
		toggleProcessesInterval();
		toggleSystemInterval();
	}

	onDestroy(() => {
		eventSource.close();
	});
</script>

<!-- Import sidebar -->
{#if pathname == '/login'}
	<slot />
{:else}
	<div class="flex flex-row w-full min-h-screen ">
		<Sidebar />
		<LoadingScreen />
		<slot />
	</div>
{/if}
