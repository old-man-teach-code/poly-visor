<script>
	import Sidebar from '../components/SiderBar/index.svelte';
	import { page } from '$app/stores';
	import { beforeUpdate, onMount } from 'svelte';
	import {
		dashboardEnabled,
		isAuthenticated,
		toggleProcessesInterval,
		toggleSystemInterval
	} from '../store/supstore.js';

	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	onMount(() => {
		if ($isAuthenticated == 'false' && pathname != '/login') {
			window.location.href = '/login';
		}
		if ($isAuthenticated == 'true' && pathname != '/login') {
			dashboardEnabled.set('true');
			toggleProcessesInterval();
			toggleSystemInterval();
		}
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
