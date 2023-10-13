<script lang="ts">
	import { createEventDispatcher, onDestroy } from 'svelte';
	import { login } from '../store/action.js';
	import { goto } from '$app/navigation';
	import { startFetching } from '../store/supstore.js';

	const dispatch = createEventDispatcher();
	const close = () => dispatch('close');
	let modal: HTMLElement;

	export let supervisorName: string;

	const previously_focused = typeof document !== 'undefined' && document.activeElement;

	if (previously_focused) {
		onDestroy(() => {
			// @ts-ignore
			previously_focused.focus();
		});
	}

	const handle_keydown = (e: any) => {
		if (e.key === 'Escape') {
			close();
			return;
		}

		if (e.key === 'Tab') {
			// trap focus
			const nodes = modal.querySelectorAll('*');
			const tabbable = Array.from(nodes).filter((n: any) => n.tabIndex >= 0);

			// @ts-ignore
			let index = tabbable.indexOf(document.activeElement);
			if (index === -1 && e.shiftKey) index = 0;

			index += tabbable.length + (e.shiftKey ? -1 : 1);
			index %= tabbable.length;
			// @ts-ignore
			tabbable[index].focus();
			e.preventDefault();
		}
	};

	async function handleLogin(e) {
		//create formdata
		const formData = new FormData(e.target);
		formData.append('supervisor', supervisorName);
		const accessToken = await login(formData);
		if (accessToken !== 'Invalid username or password') {
			document.cookie = `accessToken=${accessToken}`;
			//redirect to '/'
			startFetching(supervisorName);
			goto('/');
		}
	}
</script>

<svelte:window on:keydown={handle_keydown} />
<!-- svelte-ignore a11y-click-events-have-key-events -->

<div class="modal-background" on:click={close} />
<div class="modal w-full sm:w-fit" role="dialog" aria-modal="true" bind:this={modal}>
	<div class="bg-white rounded-2xl">
		<div class="bg-[#FF8C32] rounded-tl-2xl rounded-tr-2xl flex items-center justify-center py-6">
			<span class="text-[#06113C] text-lg sm:text-2xl font-bold"
				>Login into Polyvisor {supervisorName}</span
			>
		</div>
		<form
			class="px-20 py-10 flex items-center justify-center flex-col gap-10"
			method="POST"
			on:submit|preventDefault={handleLogin}
		>
			<div class=" flex flex-col gap-6 items-end justify-end">
				<div class="flex flex-col sm:flex-row items-start sm:items-center gap-1 sm:gap-5">
					<label for="username">Username</label>
					<input
						class="rounded-lg bg-[#DDDDDD] border-none focus:ring-[#FF8C32] focus:ring-2"
						type="text"
						name="username"
						id="username"
					/>
				</div>
				<div class="flex flex-col sm:flex-row items-start sm:items-center gap-1 sm:gap-5">
					<label for="password">Password</label>
					<input
						class="rounded-lg bg-[#DDDDDD] border-none focus:ring-[#FF8C32] focus:ring-2"
						type="password"
						name="password"
						id="password"
					/>
				</div>
			</div>
			<div class="flex flex-row gap-5">
				<button
					on:click={close}
					class="bg-[#FF8C32] rounded-lg px-6 py-2 sm:px-8 sm:py-3 text-white font-bold hover:text-rose-400 hover:bg-[#FF8C32]/80"
					>Cancel</button
				>
				<button
					class="bg-[#FF8C32] rounded-lg px-6 py-2 sm:px-8 sm:py-3 text-white font-bold hover:text-lime-400 hover:bg-[#FF8C32]/80"
					>Login</button
				>
			</div>
		</form>
	</div>
</div>

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
		position: fixed;
		left: 50%;
		top: 50%;
		max-height: calc(100vh - 4em);
		overflow: auto;
		transform: translate(-50%, -50%);
		border-radius: 0.2em;
	}
</style>
