<script>
import '$lib/recorder.js';
import { onMount } from 'svelte';
import { createEventDispatcher } from 'svelte';
const dispatch = createEventDispatcher();

export let answer_pro_or_vs = "pro";
export let debate;
export let addr_backend;
export let username;

let text_for_when_not_recording_pro     = '🎙 Let me tell you why'
let text_for_when_not_recording_against = '🎙 Let me argue against that'
let text_to_end_recording       = '🔴 Tap when nuff said'
let text_after_ending_rec       = '🤔 Considering'
let record_btn_text             = text_for_when_not_recording_pro
let is_rec_disabled             = 0


var gumStream;     //stream from getUserMedia()
var rec;           //Recorder.js object
var input;         //MediaStreamAudioSourceNode we'll be recording
var AudioContext
onMount(() => {
	AudioContext= window.AudioContext || window.webkitAudioContext;
  });
var audioContext //audio context to help us record


if( answer_pro_or_vs == 'pro')
	record_btn_text = text_for_when_not_recording_pro

$: 	{
	if (
			debate.tracks.length > 3 
		&&	record_btn_text == text_for_when_not_recording_pro
		)
		record_btn_text = text_for_when_not_recording_against
	}

function trigger_progress_the_conversation()
	{	
	console.log("trigger_progress_the_conversation()")
	dispatch('progress_the_conversation');
	}



function add_to_debate(transcribed)
	{
	console.log('transcription received:', transcribed.transcription, transcribed.audio)
	// transcription = transcribed
	debate.tracks = [...debate.tracks, 
		{
		src: addr_backend+'/' + transcribed.audio,
		transcription: transcribed.transcription,
		artist: username,
		player: debate.tracks.length==1?1:2
		}]


	debate = debate
	dispatch('message', debate);
	trigger_progress_the_conversation()
	// console.log("Server returned: ", transcription);
	}

function sendWAV(blob)
	{
	// setTimeout(()=>
		// {
		var xhr=new XMLHttpRequest();
		xhr.onload=function(e) 
			{
			if(this.readyState === 4) 
				{
				// transcription = e.target.responseText
				let resp = JSON.parse(e.target.responseText)
				record_btn_text = text_for_when_not_recording_against
				is_rec_disabled = 0
				// if (debate.tracks.length >= 3)
					// record_btn_text = 'hide'
				add_to_debate(resp)
				}
			};
	var fd=new FormData();
	// console.log(JSON.stringify(debate))
	fd.append("audio_data", blob, debate.debate_id);
	console.log("debate.debate_id",debate.debate_id)
	xhr.open("POST",addr_backend + "/transcribe_speech",true);
	xhr.send(fd);
	}

function recording() {
	//	Pressed Record
	if (
			record_btn_text==text_for_when_not_recording_pro
		||	record_btn_text==text_for_when_not_recording_against
		)
		{
		console.log("Recording..");

		/*
			Simple constraints object, for more advanced audio features see
			https://addpipe.com/blog/audio-constraints-getusermedia/
		*/

		var constraints = { audio: true, video:false }

		/*
			Disable the record button until we get a success or fail from getUserMedia() 
		*/

		// recordButton.disabled = true;
		// stopButton.disabled = false;
		// pauseButton.disabled = false
		record_btn_text = text_to_end_recording

		/*
			We're using the standard promise based getUserMedia() 
			https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
		*/

		navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

			/*
				create an audio context after getUserMedia is called
				sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
				the sampleRate defaults to the one set in your OS for your playback device

			*/
			audioContext = new AudioContext();

			//update the format 
			// document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

			/*  assign to gumStream for later use  */
			gumStream = stream;

			/* use the stream */
			input = audioContext.createMediaStreamSource(stream);

			/* 
				Create the Recorder object and configure to record mono sound (1 channel)
				Recording 2 channels  will double the file size
			*/
			rec = new Recorder(input,{numChannels:1})

			//start the recording process
			rec.record()

			console.log("Recording started");

			}).catch(function(err) {
				//enable the record button if getUserMedia() fails
				// recordButton.disabled = false;
				// stopButton.disabled = true;
				// pauseButton.disabled = true
			});
		}
	else
	//	Pressed done. Sending:
	if(record_btn_text==text_to_end_recording)
		{
		record_btn_text = text_after_ending_rec
		is_rec_disabled = 1
		console.log("Recorded.");
		rec.stop();

		//stop microphone access
		gumStream.getAudioTracks()[0].stop();

		//create the wav blob and pass it on to createDownloadLink
		rec.exportWAV(sendWAV);
		}	
}

</script>


<button id="recordButton" on:click|preventDefault|stopPropagation|capture|nonpassive={recording} disabled={is_rec_disabled} class="button-53 {answer_pro_or_vs}">{record_btn_text}</button>




<style>
.pro	
	{
	background-color: #539dcb;
	}
.vs	
	{
	background-color: #cb7d53;
	}


#recordButton
	{
	margin: 0 auto;
	}


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

</style>
