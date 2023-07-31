<script>
import AudioPlayer from './AudioPlayer.svelte';
import Spinner from './Spinner.svelte';
import Debate from './Debate.svelte';
import Answer from './Answer.svelte';
// import Counter from './Counter.svelte';
import Speakers from './Speakers.svelte';
import thinker from '$lib/images/2-thinkers.png';
import { onMount } from 'svelte';

import '$lib/recorder.js';




  // Function to set a cookie
  function setCookie(name, value, days) {
    const expires = days ? new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString() : '';
    document.cookie = `${name}=${value || ''}; expires=${expires}; path=/`;
  }



function checkAccessCodeCookie() {
  // Split the cookie string into individual cookies
  const cookiesArray = document.cookie.split(';');

  // Loop through the cookies to find the 'access_code' cookie
  for (const cookie of cookiesArray) {
    const [name, value] = cookie.trim().split('=');

    // Check if the cookie name is 'access_code'
    if (name === 'access_code') {
      // The 'access_code' cookie is present
      return true;
    }
  }

  // The 'access_code' cookie is not present
  return false;
}

let	access_code_present = 1;

onMount(() => {
	// Get the access_code from the URL query parameter
	const urlParams = new URLSearchParams(window.location.search);
	const accessCode = urlParams.get('access_code');

	// Save the access_code value as a cookie
	if (accessCode) {
		setCookie('access_code', accessCode, 7); // Cookie will expire in 7 days
	}

	access_code_present = checkAccessCodeCookie();
});






function randomString(length, chars) {
    var result = '';
    for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}

let user_id   = randomString(30, '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ');
// let debate_id = randomString(20, '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ');



let host = 'https://debate.lol'; // window.location.protocol + "//" + window.location.hostname
let addr_backend  = host + '/backend'
let addr_frontend = host
console.log(addr_backend)


let username = 'Visitor'

const SPEAKERS = [
    ["Barack Obama", "", ["Universal basic income a good idea", "US foreign policy during Obama's presidency was bad", "Basketball is better than golf"]],
    ["Donald Trump", "", ["Nothing", "US should build a wall at the southern border", "US is the best country in the world", "Golf is better than basketball"]],
    ["Elon Musk", "", ["Humanity needs a colony on Mars", "Humanity needs to switch to electric cars ASAP", "DogeCoin is an ultrasound investment"]],
    ["Taylor Swift", "", ["Music industry is not fair to artists", "Heavy metal is better than pop", "Kanye West is a bad person"]],
    ["Bill Gates", "", ["It is better to use tabs than spaces for indentation.", "Windows is the best OS", "Steve Ballmer was a better CEO than Satya Nadella", "Microsoft should acquire ElevenLabs"]],
    ["Emma Watson", "", ["Trump is a Voldemort", "Europe should accept more refugees", "Hermione should have ended up with Harry instead of Ron"]],
    ["Steve Jobs", "", ["Android copies iOS all the time", "Stanford is better than Berkeley", "You should always follow your passion", "Drugs are actually great"]],
]


let all_speakers=[
		username
	// ,	'Emma'
	// ,	'Trump'
	// ,	'Zuck'
	// ,	'Elon'
	// ,	'Gates'	
	]

$:	{
	if (all_speakers[0] != username)
		username = all_speakers[0]
	}

SPEAKERS.forEach(e=>all_speakers.push(e[0]))


//   let randomValue = Math.random(); // Initialized once, but will change on each re-render

//   // Function to prevent reactivity from changing the randomValue
//   function initializeOnce() {
//     // Check if the randomValue has already been initialized
//     if (typeof randomValue !== 'number') {
//       randomValue = Math.random();
//     }
//   }

//   // Call the 'initializeOnce' function when the component is mounted
//   onMount(initializeOnce);

const random_1 = Math.random()
const random_2 = Math.random()
const random_i_default_ai = Math.floor(random_1 * SPEAKERS.length)
const speaker_default_ai = SPEAKERS[random_i_default_ai][0];
const random_argument_default_ai = Math.floor(random_2 * SPEAKERS[random_i_default_ai][2].length)
const random_argument = SPEAKERS[random_i_default_ai][2][random_argument_default_ai]

// let random_i_default_ai;
// let speaker_default_ai = '';
// let random_argument_default_ai = '';
// let random_argument = 'asd';
// let did_we_already_generate_defaults = false


let debate =
	{
		topic    : ''
	,	tracks   : []
	,	started  : 0
	,	speaker1    : speaker_default_ai
	,	speaker2    : username
	,	placeholder : random_argument
	,	debate_id	: randomString(20, '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	}

$:	{
	if (! all_speakers.includes(debate.speaker1))
		debate.speaker1 = all_speakers[0]
	if (! all_speakers.includes(debate.speaker2))
		debate.speaker2 = all_speakers[0]
	}


let waiting_for_server = 0;
// onMount(() => {
// 	// if (did_we_already_generate_defaults == false)
// 		{
// 		did_we_already_generate_defaults = true
// 		random_i_default_ai = Math.floor(Math.random() * SPEAKERS.length)
// 		speaker_default_ai  = SPEAKERS[random_i_default_ai][0];
// 		random_argument_default_ai = Math.floor(Math.random() * SPEAKERS[random_i_default_ai][2].length)
// 		random_argument     = SPEAKERS[random_i_default_ai][2][random_argument_default_ai]
// 		debate = debate
// 		}
//   });


let presenter_said = []




function progress_the_conversation()
	{
	console.log("progress_the_conversation()")
	if	(
			debate.tracks.length == 1
		&&	debate.speaker1 != username
		)
		ask_bot({...debate, speaker:debate.speaker1, player:1})
	else
	if	(
			debate.tracks.length == 3
		&&	debate.speaker2 != username
		)
		{
		ask_bot({...debate, speaker:debate.speaker2, rebuttal:true, player:2})
		}
	else

	if	(debate.tracks.length == 2)
		{
		debate.tracks.push(
			{
				src: addr_backend+'/static/speeches/'+debate.debate_id+'_after1.wav',
				transcription: presenter_said[1],
				artist: 'Presenter',
				player:0
			})
		debate = debate
		progress_the_conversation()
		return 0
		}
	else
	if	(debate.tracks.length == 4)
		{
		debate.tracks.push(
			{
				src: addr_backend+'/static/speeches/'+debate.debate_id+'_after2.wav',
				transcription: presenter_said[2],
				artist: 'Presenter',
				player:0
			})
		debate = debate
		progress_the_conversation()
		return 0
		}

	else
	if	(debate.tracks.length == 5)
		{
		judge()
		// progress_the_conversation()
		return 0
		}
	}


async function judge()
	{
	let	responseData = ''
	async function backend_judge_speech() 
		{
		const url = addr_backend+'/judge_speech/'+debate.debate_id;
		const data = debate;

		const requestOptions = 
			{
			method: 'GET',
			headers: 
				{
				'Content-Type': 'application/json'
				},
			// body: JSON.stringify(send)
			};

		try {
			const response = await fetch(url, requestOptions);

			let response_result = await response.json();
			let score1    = response_result["score1"];
			let score2    = response_result["score2"];
			let judgement = response_result["judgement"];

			debate.tracks.push(
				{
					src: addr_backend+'/static/speeches/'+debate.debate_id+'_judgement.wav',
					// src: addr_backend+'/'+audio_file,
					transcription: judgement,
					artist: "Presenting jury response",
					player: score1>score2? 11:22
				})
			debate = debate
			waiting_for_server = 0

			// progress_the_conversation()



			}
		catch (error) 
			{
			console.error('Error fetching data:', error);
			waiting_for_server = 0
			}
		}
	waiting_for_server = 1
	backend_judge_speech()

	}




async function ask_bot(send)
	{
	let	responseData = ''
	async function backend_generate_speech() 
		{
		const url = addr_backend+'/generate_speech';
		const data = debate;

		const requestOptions = 
			{
			method: 'POST',
			headers: 
				{
				'Content-Type': 'application/json'
				},
			body: JSON.stringify(send)
			};

		try {
			const response = await fetch(url, requestOptions);

			let response_result = await response.json();
			// let text_said  = response_result["transcription"];
			// let audio_file = response_result["audio"];
			// let text_said = await response.json();
			let text_said  = response_result["speech"];
			let audio_file = response_result["audio"];
			console.log(text_said)

			debate.tracks.push(
				{
					// src: addr_backend+'/static/speeches/'+debate.debate_id+'_intro.wav',
					src: addr_backend+'/'+audio_file,
					transcription: text_said,
					artist: send.speaker,
					player: send.player
				})
			debate = debate
			waiting_for_server = 0

			progress_the_conversation()
			}
		catch (error) 
			{
			console.error('Error fetching data:', error);
			waiting_for_server = 0
			}
		}
	waiting_for_server = 1
	backend_generate_speech()
	}




async function start_debate()
	{
	debate.started = 1
	if (debate.topic == '')
		debate.topic = debate.placeholder
	// console.log('debate.topic',debate.topic)

	let	responseData = ''
	async function postData() 
		{
		const url = addr_backend+'/initialize_debate';
		const data = debate;

		const requestOptions = 
			{
			method: 'POST',
			headers: 
				{
				'Content-Type': 'application/json'
				},
			body: JSON.stringify(data)
			};

		try {
			// Make the POST request
			const response = await fetch(url, requestOptions);

			// Parse the response as JSON
			presenter_said = await response.json();
			console.log(presenter_said)

			debate.tracks.push(
				{
					src: addr_backend+'/static/speeches/'+debate.debate_id+'_intro.wav',
					transcription: presenter_said[0],
					artist: 'Presenter',
					player:0
				})
			debate = debate
			progress_the_conversation()
			}
		catch (error) 
			{
			console.error('Error fetching data:', error);
			}
		}


	postData()
	}


// function transcriptionReceived(transcribed)
// 	{
// 	// transcription = transcribed
// 	debate.tracks = [...debate.tracks, 
// 		{
// 		src: addr_backend+'/static/user.mp3',
// 		transcription: transcribed,
// 		artist: 'Me',
// 		player:debate.tracks.length+1
// 		}]


// // Temporary simulation
// 	if (debate.tracks.length > 1)
// 	debate.tracks = [...debate.tracks, 
// 		{
// 		src: 'https://learn.svelte.dev/assets/media/music/satie.mp3',
// 		transcription: 'Second won!',
// 		artist: 'Referee',
// 		player:22
// 		}]




// 	debate = debate
// 	// console.log("Server returned: ", transcription);
// 	}

// function sendWAV(blob)
// 	{
// 	// setTimeout(()=>
// 		// {
// 		var xhr=new XMLHttpRequest();
// 		xhr.onload=function(e) 
// 			{
// 			if(this.readyState === 4) 
// 				{
// 				// transcription = e.target.responseText
// 				transcriptionReceived(e.target.responseText)
// 				if (debate.tracks.length > 1)
// 					record_btn_text = 'hide'
// 				else
// 					{
// 					record_btn_text = text_for_when_not_recording_against
// 					is_rec_disabled = 0
// 					}
// 				}
// 			// }, 50);
// 	};
// 	var fd=new FormData();
//     // var filename = new Date().toISOString();
// 	fd.append("audio_data",blob, debate_id);
// 	// fd.append("audio_data",blob, filename);
// 	xhr.open("POST",addr_backend + "/transcribe_speech",true);
// 	xhr.send(fd);
// 	}

// function recording() {
// 	//	Pressed Record
// 	if (
// 			record_btn_text==text_for_when_not_recording_pro
// 		||	record_btn_text==text_for_when_not_recording_against
// 		)
// 		{
// 		console.log("Recording..");

// 		/*
// 			Simple constraints object, for more advanced audio features see
// 			https://addpipe.com/blog/audio-constraints-getusermedia/
// 		*/

// 		var constraints = { audio: true, video:false }

// 		/*
// 			Disable the record button until we get a success or fail from getUserMedia() 
// 		*/

// 		// recordButton.disabled = true;
// 		// stopButton.disabled = false;
// 		// pauseButton.disabled = false
// 		record_btn_text = text_to_end_recording

// 		/*
// 			We're using the standard promise based getUserMedia() 
// 			https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
// 		*/

// 		navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
// 			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

// 			/*
// 				create an audio context after getUserMedia is called
// 				sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
// 				the sampleRate defaults to the one set in your OS for your playback device

// 			*/
// 			audioContext = new AudioContext();

// 			//update the format 
// 			// document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

// 			/*  assign to gumStream for later use  */
// 			gumStream = stream;

// 			/* use the stream */
// 			input = audioContext.createMediaStreamSource(stream);

// 			/* 
// 				Create the Recorder object and configure to record mono sound (1 channel)
// 				Recording 2 channels  will double the file size
// 			*/
// 			rec = new Recorder(input,{numChannels:1})

// 			//start the recording process
// 			rec.record()

// 			console.log("Recording started");

// 			}).catch(function(err) {
// 				//enable the record button if getUserMedia() fails
// 				// recordButton.disabled = false;
// 				// stopButton.disabled = true;
// 				// pauseButton.disabled = true
// 			});
// 		}
// 	else
// 	//	Pressed done. Sending:
// 	if(record_btn_text==text_to_end_recording)
// 		{
// 		record_btn_text = text_after_ending_rec
// 		is_rec_disabled = 1
// 		console.log("Recorded.");
// 		rec.stop();

// 		//stop microphone access
// 		gumStream.getAudioTracks()[0].stop();

// 		//create the wav blob and pass it on to createDownloadLink
// 		rec.exportWAV(sendWAV);
// 		}	
// }



let answer_pro_or_vs = 'pro';
$:	{
	if (debate.tracks == 1)
		answer_pro_or_vs = 'pro';
	else
		answer_pro_or_vs = 'vs';
	}
</script>





<svelte:head>
	<title>Debate.LOL - debate with AI</title>
	<meta name="description" content="Debate the best public speakers in the world on any topic you like!" />
</svelte:head>

<section>
	<!-- <h1> -->
		<div class="welcome">
			<picture>
				<source srcset={thinker} type="image/webp" />
				<img src={thinker} alt="Debate" />
			</picture>
		</div>

	<!-- </h1> -->












{#if access_code_present == 1}
	{#if (debate.started != 0)}
		<Debate {...debate} />

		<br/>

		<!-- {#if (record_btn_text != 'hide')} -->
		{#if debate.tracks.length == 0}
			<div id="starting_conversaion">Starting the debate...</div>
			<br/>
			<br/>
			<Spinner />
		{:else if waiting_for_server}
			<div id="starting_conversaion">The speaker is preparing...</div>
			<br/>
			<br/>
			<Spinner />
		{/if}
		{#if (
				debate.tracks.length == 1  &&  debate.speaker1 == username
			||	debate.tracks.length == 3  &&  debate.speaker2 == username
			)}
		<!-- <button id="recordButton" on:click|preventDefault|stopPropagation|capture|nonpassive={recording} disabled={is_rec_disabled} class="button-53 {debate.tracks.length?'going-second':'going-first'}">{record_btn_text}</button> -->
			<Answer {answer_pro_or_vs} {username} bind:debate={debate} {addr_backend} on:progress_the_conversation={progress_the_conversation} />
		{/if}
	{:else}
		<div id="prepare-choices">
			<div id="topic-choice">
				<div id="topic-will-be">
				💡 Let's argue about:
				</div>
				<textarea id="topic-input" type="text" placeholder={debate.placeholder} bind:value={debate.topic}/>
			</div>
			<div id="speaker-choice">
				<div id="speaker-A-choice">
					<div class="speakers-will-be">
					🗣 Proponent
					</div>
					<Speakers bind:chosen={debate.speaker1} bind:speakers={all_speakers} />
				</div>
				<div id="speaker-B-choice">
					<div class="speakers-will-be">
					🔥 Opponent
					</div>
					<Speakers bind:chosen={debate.speaker2} bind:speakers={all_speakers} side="B" />
				</div>
			</div>	
			<button id="start_debate" on:click|preventDefault|stopPropagation|capture|nonpassive={start_debate} class="button-53 pro">Start</button>
		</div>	
	{/if}
	{#if debate.tracks.length == 6}
		<div id="next">
		The debate concluded.<br/>
		Recording is now available in the <a href="/explore">🏆 Hall of Fame</a>.<br/>
		You can <a href="/">🗣 start a new debate</a> if you want.
		</div>
	{/if}
{:else}
<br/>
<br/>
<br/>
<div id="next">
Ask vlyubin@gmail.com for an exclusive access token.
</div>
{/if}









</section>

<style>
	#prepare-choices
		{
		width: 100%;
		}
	#start_debate
		{
		margin:	3em auto 1em;
		}
	#speaker-choice
		{
		width: 100%;
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 1em;
		align-items: flex-end;
		}
	#speaker-A-choice, #speaker-B-choice
		{
		flex: 1 1 calc(50% - 15px);
		}
	.speakers-will-be
		{
		font-size: 2em;
		line-height:1.4;
		padding:1em 0;
		}

	@media (max-width: 600px) 
		{ /* adjust this value according to your needs */
		#A, #B 
			{
			flex: 1 1 100%; /* in smaller screens, each div takes full width */
			justify-content: flex-end; 
			}
		}



	#topic-choice
		{
		width: 100%;
		}
	#topic-will-be
		{
		font-size: 2em;
		line-height:1.4;
		padding:1em 0;
		}
	#topic-choice textarea
		{
		line-height:1.4;
		font-size: 2em;
		background: #333;
		width:100%;
		padding:0.5em;
		box-sizing:border-box;
		border-radius:10px;
		color: hsla(1,0%,100%, 0.8);
		/* border-radius:10% 10% / 5% 20%; */
		border: 2px solid #444;
		}


	section {
		/* display: flex; */
		flex-direction: column;
		justify-content: center;
		align-items: center;
		/* flex: 0.1; */
	}

	h1 {
		width: 100%;
		padding: 0;
		margin: 0;
	}

	.welcome {
		display: block;
		/* position: relative; */
		width: 100%;
	}

	.welcome img {
	  	object-fit: contain;
		max-height:40vh;
		max-width:100%;

		height:auto;
		width:auto;

		top: 0;
		display: block;
		border-radius:30% 30% / 20% 100%;
		border: solid 1px #000;
		box-shadow:
		0.2em 0.1em 0.3em #111,
		-0.4em -0.1em 0.3em #111;

	}









/* CSS */
.pro	
	{
	background-color: #539dcb;
	}
/* .going-second	
	{
	background-color: #cb7d53;
	} */
.button-53 {
	/* background-color: #cb7d53; */
	border: 0 solid #E5E7EB;
	border-radius:3% 3% / 2% 10%;

	box-sizing: border-box;
	color: #fff;
	display: flex;
	font-family: ui-sans-serif,system-ui,-apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
	font-size: 1rem;
	font-weight: 700;
	justify-content: center;
	line-height: 1.75rem;
	padding: .75rem 1.65rem;
	position: relative;
	text-align: center;
	text-decoration: none #000000 solid;
	text-decoration-thickness: auto;
	width: 100%;
	max-width: 460px;
	position: relative;
	cursor: pointer;
	transform: rotate(-2deg);
	user-select: none;
	-webkit-user-select: none;
	touch-action: manipulation;
}

.button-53:disabled {
	background-color: #616161;
	}
.button-53:focus {
	outline: 0;
}

.button-53:after {
	content: '';
	position: absolute;
	border: 1px solid #fff;
	bottom: 4px;
	left: 4px;
	width: calc(100% - 1px);
	height: calc(100% - 1px);
	border-radius:3% 3% / 2% 10%;

}

.button-53:hover:after {
	bottom: 2px;
	left: 2px;
}

@media (min-width: 768px) {
	.button-53 {
		padding: .75rem 3rem;
		font-size: 1.25rem;
	}
}


#starting_conversaion
	{
	text-align:center;
	width:100%;
	display:block;
	}


#next
	{
	font-size: 2em;
	line-height:1.5;
	text-align:center;
	width:100%;
	display:block;
	}

</style>
