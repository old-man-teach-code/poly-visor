<script lang="ts">
	import Sidebar from '../components/SiderBar/index.svelte';
	import { page } from '$app/stores';
	import { onDestroy, onMount } from 'svelte';
	import {
		fetchProcesses,
		isAuthenticated,
		dashboardEnabled,
		fetchSystem
	} from '../store/supstore.js';
	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	let eventSource: EventSource;

	let systemInterval: NodeJS.Timeout;
	let processInterval: NodeJS.Timeout;

	$: if ($dashboardEnabled == 'true') {
		systemInterval = setInterval(fetchSystem, 2000);
	} else {
		clearInterval(systemInterval);
	}

	$: if ($isAuthenticated == 'true') {
		processInterval = setInterval(fetchProcesses, 2000);
	} else {
		clearInterval(processInterval);
	}

	$: if ($isAuthenticated == 'false' && pathname != '/login') {
		window.location.href = '/login';
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
