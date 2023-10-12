<script lang="ts">
	import { onMount } from 'svelte';
	import { getAllSupervisors } from '../../store/action';
	import LoadingScreen from '../../components/LoadingScreen.svelte';
	import LoginModal from '../../components/LoginModal.svelte';
	interface Supervisor {
		host: string;
		name: string;
		processes: {};
		running: boolean;
		url: string;
	}

	let supervisors: Supervisor[] = [];
	let loginModal = false;
	let selectedSupervisor: string = '';

	onMount(async () => {
		supervisors = await getAllSupervisors();
	});

	function handleSupervisorClick(supervisor: Supervisor) {
		if (!supervisor.running) {
			alert('Supervisor is not running, please enable this supervisor instance!');
			return;
		}
		selectedSupervisor = supervisor.name;
		loginModal = true;
	}
</script>

<div class="bg-[#06113C] w-screen h-screen flex justify-center flex-col items-center relative">
	<LoadingScreen>
		<h1 class="text-white top-24 text-xl md:text-3xl font-bold absolute">Select a Supervisor</h1>
		{#if supervisors.length == 0}
			<h1 class="text-white text-xl md:text-3xl font-bold">No supervisor found</h1>
		{/if}
		<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-10 w-3/4">
			{#each Object.entries(supervisors) as [id, supervisor]}
				<button
					on:click={() => handleSupervisorClick(supervisor)}
					class="bg-[#FF8C32] hover:bg-[#FF8C32]/80 p-4 md:p-6 rounded-2xl w-full flex flex-row items-center gap-3"
				>
					<span class="text-base md:text-xl font-semibold">Polyvisor {supervisor?.name}</span>
					<div
						class="h-3 w-3 min-w-[12px] min-h-[12px] {supervisor?.running
							? 'bg-lime-400'
							: 'bg-gray-400'} rounded-full"
					/>
				</button>
			{/each}
		</div>
		{#if loginModal}
			<LoginModal
				supervisorName={selectedSupervisor}
				on:close={() => {
					loginModal = !loginModal;
				}}
			/>
		{/if}
	</LoadingScreen>
</div>
