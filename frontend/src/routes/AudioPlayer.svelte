<script>
	export let src;
	export let transcription;
	export let artist;
	export let player = 0;
	export let preload = "metadata";

	let time = 0;
	let duration = 0;
	let paused = true;

	function format(time) {
		if (isNaN(time)) return '...';

		const minutes = Math.floor(time / 60);
		const seconds = Math.floor(time % 60);

		return `${minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
	}
</script>

<div class="player player{player}" class:paused>


	<div>
		<button
			class="play"
			aria-label={paused ? 'play' : 'pause'}
			on:click={() => paused = !paused}
		/>
	</div>
	<div>
		<audio
			{src}
			bind:currentTime={time}
			bind:duration
			bind:paused
			preload={preload}
			on:ended={() => {
				time = 0;
			}}
		/>
		
		<div class="info">
			<div class="time">
				<span>{format(time)}</span>
				<div
					class="slider"
					on:pointerdown={e => {
						const div = e.currentTarget;
						
						function seek(e) {
							const { left, width } = div.getBoundingClientRect();

							let p = (e.clientX - left) / width;
							if (p < 0) p = 0;
							if (p > 1) p = 1;
							
							time = p * duration;
						}

						seek(e);

						window.addEventListener('pointermove', seek);

						window.addEventListener('pointerup', () => {
							window.removeEventListener('pointermove', seek);
						}, {
							once: true
						});
					}}
				>
					<div class="progress" style="--progress: {time / duration}%" />
				</div>
				<span>{duration ? format(duration) : '--:--'}</span>



			</div>

			<div class="description">
				<strong>{artist}</strong> /
				<span>{transcription}</span>

			</div>

	</div>

	</div>
</div>

<style>
	.player {
		display: grid;
		grid-template-columns: 2.5em 1fr;
		align-items: center;
		gap: 1em;
		padding: 0.6em 1em 0.6em 0.6em;
		border-radius: 2em;
		/* background: var(--bg-1); */
		/* background: #333; */
		transition: filter 0.2s;
		color: var(--fg-3);
		/* color: #000; */

		/* user-select: none; */
	}

	.player:not(.paused) {
		color: var(--fg-1);
		/* color: #000; */
		filter: drop-shadow(0.5em 0.5em 1em rgba(0,0,0,0.1));
	}
	
	button {
		width: 100%;
		cursor:pointer;
		aspect-ratio: 1;
		background-repeat: no-repeat;
		background-position: 50% 50%;
		border-radius: 50%;
	}
	
	[aria-label="pause"] {
		background-image: url(./pause.svg);
	}

	[aria-label="play"] {
		background-image: url(./play.svg);
	}

	.info {
		overflow: hidden;
	}

	.description {
		/* white-space: nowrap; */
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 1.2;
	}

	.time {
		display: flex;
		align-items: center;
		gap: 0.5em;
		line-height:1.7
	}

	.time span {
		font-size: 0.7em;
	}

	.slider {
		flex: 1;
		height: 0.5em;
		background: var(--bg-2);
		/* background: #000; */
		border-radius: 0.5em;
		overflow: hidden;
	}

	.progress {
		width: calc(100 * var(--progress));
		height: 100%;
		/* background: var(--bg-3); */
		background: #fff;
	}



.player1
		{
		background-color: #2a3a46;
		}
.player2
		{
		background-color: #3d291e;
		}
/* Player 1 or 2 won */
.player11 
		{
		background-color: #25455a;
		} 
.player22
		{
		background-color: #5a3725;
		} 


</style>