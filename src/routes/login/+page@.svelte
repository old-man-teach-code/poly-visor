<script lang="ts">
</script>

<div class="bg-[#06113C] w-screen h-screen flex flex-col">
	<h1 class="text-[32px] text-[#EEEEEE] font-bold mb-10 text-center bottom-0 mt-24">Login</h1>
	<div class="bg-white mx-auto mt-14 rounded-2xl">
		<div class="bg-[#FF8C32] rounded-tl-2xl rounded-tr-2xl flex justify-center py-6">
			<span class="text-[#06113C] text-2xl font-bold">Polyvisor lid001</span>
		</div>
		<div class="px-20 py-10 flex items-center justify-center flex-col gap-6">
			<div class="flex flex-row items-center gap-5">
				<label for="username">Username</label>
				<input
					class="rounded-lg bg-[#DDDDDD] border-none focus:ring-[#FF8C32] focus:ring-2"
					type="text"
					name="username"
					id="username"
				/>
			</div>
			<div class="flex flex-row items-center gap-5">
				<label for="password">Password</label>
				<input
					class="rounded-lg bg-[#DDDDDD] border-none focus:ring-[#FF8C32] focus:ring-2"
					type="password"
					name="password"
					id="password"
				/>
			</div>
			<button
				class="bg-[#FF8C32] rounded-lg px-8 py-3 text-[#EEEEEE] font-bold hover:bg-[#FF8C32]/80"
				>Login</button
			>
		</div>
	</div>
</div>
