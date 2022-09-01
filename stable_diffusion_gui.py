# img_viewer.py

import PySimpleGUI as sg
import os.path
import json
import base64
import subprocess
import requests
import time

PORT_NUMBER = 5000

sg.theme('SystemDefault1')

prompt_input_column = [
    [sg.Text("Prompt")],
    [sg.Multiline(size =(50, 3), key="prompt")],
    [sg.Text("Width"), sg.InputText('512', size=(10, 1), key="width")],
    [sg.Text("Height"), sg.InputText('512', key="height")],
    [sg.Text("# Inference Steps"), sg.InputText('15', key="num_inference_steps")],
    [sg.Button('Run',), sg.Button('Exit')],
    [sg.Text("Status: Ready",key="status")],
    [sg.Text(key="error")]
]

image_viewer_column = [
    [sg.Text(key="prompt_output_time")],
    [sg.Text(size=(50, 1), key="prompt_output_text")],
    [sg.Image(key="prompt_output")],
]

layout = [
    [
        sg.Column(prompt_input_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

def sd_post(values):
    input_obj = {
        "input": {
            "prompt": values['prompt'],
            "width": values['width'],
            "height": values['height'],
            "num_outputs": "1",
            "num_inference_steps": values['num_inference_steps'],
            "guidance_scale": "5"
        }
    }

    url = 'http://localhost:{}/predictions'.format(PORT_NUMBER)
    payload = json.dumps(input_obj)
    headers = {'Content-Type': "application/json"}
    return requests.post(url, data=payload, headers=headers)

def run_sd(values):

    start_time = time.time()
    post_res = sd_post(values)
    response = post_res.content.decode("utf-8")

    end_time = time.time()
    
    # Please ignore shitty error handling
    if 'succeeded' not in response:
        window['status'].update('Status: Error')
        if 'Internal Server Error' in response:
            window['error'].update('NSFW Content Detected')
        else:
            window['error'].update(response)
    else:
        window['status'].update('Status: Running')
        # Parse the JSON response
        data = json.loads(response)

        # Get the base64 bytestring, convert to a string
        b64str = str.encode(data['output'][0].replace('data:image/png;base64,', ''))

        # Toss er into a png
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(b64str))

        # Elapsed time
        elapsed_time = end_time - start_time

        # Update GUI
        window['prompt_output_time'].update("Time elapsed: {:.2f} seconds".format(elapsed_time))
        window['prompt_output_text'].update(values['prompt'])
        window["prompt_output"].update(filename='imageToSave.png')
        window['status'].update('Status: Success')

window = sg.Window("Stable Diffusion", layout)

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == 'Run':
        window['error'].update('')
        run_sd(values)

window.close()
