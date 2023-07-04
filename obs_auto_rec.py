import obspython as obs
import datetime
import subprocess
import os


# Set start time and recording duration
start_time = datetime.time(hour=5, minute=30, second=0)
recording_duration = datetime.timedelta(minutes=2)

# Set output name and format
output_format = "mkv"
output_directory = "/path/to/recording/directory"
output_filename = f"News - {datetime.date.today()}.{output_format}"


# Callback function for the "Start Rec" button
def start_recording_callback(props, prop):
    # Get current time
    current_time = datetime.datetime.now().time()

    # Check if current time is after the start time
    if current_time > start_time:
        # Calculate the time remaining until the end of the recording
        time_remaining = datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(days=1) - datetime.datetime.now()

        # Check if the time remaining is less than the recording duration
        if time_remaining < recording_duration:
            # Adjust the recording duration
            recording_duration = time_remaining

            # Start recording
            obs.obs_frontend_recording_start()

            # Schedule to stop the recording after the recording duration
            obs.timer_add(stop_recording_callback, int(recording_duration.total_seconds() * 1000))

            # Set output file path
            output_file = os.path.join(output_directory, output_filename)
            obs.obs_output_set_recording_output(obs.obs_frontend_get_recording_output(), output_file)

            # Log recording start
            obs.script_log(obs.LOG_INFO, "Recording started!")


# Callback function to stop the recording
def stop_recording_callback():
    # Stop recording
    obs.obs_frontend_recording_stop()

    # Convert recorded file
    input_file = os.path.join(output_directory, output_filename)
    output_file = os.path.join(output_directory, f"News - {datetime.date.today()}.mp4")
    subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-c:a", "copy", output_file], check=True)

    # Log recording end
    obs.script_log(obs.LOG_INFO, "Recording stopped!")

# Register the start_recording_callback function as a button script property
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "start_recording", "Start Recording", start_recording_callback)
    return props

# Set script description and properties
def script_description():
    return "Starts and stops the recording of MKV file at a given time. Then converts it to MP4."

obs.script_properties = script_properties
obs.script_description = script_description