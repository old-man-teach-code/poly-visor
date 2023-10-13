<script>
	import Sidebar from '../components/SideBar.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { isAuthenticated } from '../store/supstore.js';
	

	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	onMount(() => {
		if (!$isAuthenticated) {
			goto('/login');
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
