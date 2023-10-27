<script lang="ts">
	import { dashboardEnabled } from '../../store/supstore';

	function handleDasboardToggle() {
		dashboardEnabled.set($dashboardEnabled == 'true' ? 'false' : 'true');
	}
</script>

<div class="grid items-center mx-auto">
	<div class="flex flex-row gap-3">
		<h1>Dashboard API</h1>
		<button
			on:click={handleDasboardToggle}
			type="button"
			class="{$dashboardEnabled == 'true' ? 'bg-green-200' : 'bg-red-200'}
inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out "
			role="switch"
			aria-checked="false"
		>
			<!-- Enabled: "translate-x-5", Not Enabled: "translate-x-0" -->
			<span
				aria-hidden="true"
				class="
  {$dashboardEnabled == 'true' ? 'translate-x-5' : 'translate-x-0'}
  pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
			/>
		</button>
	</div>
</div>
