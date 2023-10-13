<script lang="ts">
	import { onMount } from 'svelte';
	import { getAllSupervisors } from '../../store/action';
	import LoadingScreen from '../../components/LoadingScreen.svelte';
	import LoginModal from '../../components/LoginModal.svelte';
	import { isAuthenticated } from '../../store/supstore';
	interface Supervisor {
		host: string;
		name: string;
		processes: {};
		running: boolean;
		url: string;
		authentication: boolean;
	}

	let supervisors: Supervisor[] = [];
	let loginModal = false;
	let selectedSupervisor: string = '';

	onMount(async () => {
		if ($isAuthenticated == 'true') window.location.href = '/';
		supervisors = await getAllSupervisors();
	});

	function handleSupervisorClick(supervisor: Supervisor) {
		if (!supervisor.authentication) {
			window.location.href = `/login/${supervisor.name}`;
			return;
		}
		if (!supervisor.running) {
			alert('Supervisor is not running, please enable this supervisor instance!');
			return;
		}
		selectedSupervisor = supervisor.name;
		loginModal = true;
	}
</script>

<div
	class="bg-[#06113C] w-screen !min-w-fit h-screen flex justify-center flex-col items-center relative"
>
	<LoadingScreen>
		<h1 class="text-white top-24 text-xl md:text-3xl font-bold absolute">Select a Supervisor</h1>
		{#if supervisors.length == 0}
			<h1 class="text-white text-xl md:text-3xl font-bold">No supervisor found</h1>
		{/if}
		<div class="grid  sm:grid-cols-2 lg:grid-cols-3  gap-10 mx-10 lg:mx-20">
			{#each supervisors as supervisor}
				<button
					on:click={() => handleSupervisorClick(supervisor)}
					class="bg-[#FF8C32] hover:bg-[#FF8C32]/80 p-4 md:p-6  rounded-2xl w-full flex flex-row justify-between items-center gap-3 truncate"
				>
					<div class=" flex flex-row items-center gap-3 truncate">
						<span class="text-base md:text-lg font-semibold truncate"
							>Polyvisor {supervisor?.name}aaaaaaaaaaaaaaaaaaaaaaaaa</span
						>
						<div
							class="h-3 w-3 min-w-[12px] min-h-[12px] {supervisor?.running
								? 'bg-lime-400'
								: 'bg-gray-400'} rounded-full"
						/>
					</div>
					{#if supervisor?.authentication}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
							class="w-5 h-5 text-rose-500 min-w-[20px] min-h-[20px]"
						>
							<path
								fill-rule="evenodd"
								d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z"
								clip-rule="evenodd"
							/>
						</svg>
					{:else if !supervisor?.authentication}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
							class="w-5 h-5 text-lime-400 min-w-[20px] min-h-[20px]"
						>
							<path
								fill-rule="evenodd"
								d="M14.5 1A4.5 4.5 0 0010 5.5V9H3a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-1.5V5.5a3 3 0 116 0v2.75a.75.75 0 001.5 0V5.5A4.5 4.5 0 0014.5 1z"
								clip-rule="evenodd"
							/>
						</svg>
					{/if}
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
