# stable-diffusion-gui
A python GUI to interact with a self-hosted instance of the Stable Diffusion Text-to-Image AI. Essentially just a program to accept input, send a POST request to the local server, and convert the response from base64 to an image on the screen. 

### To run the Stable Diffusion AI
```docker run -d -p 5000:5000 --gpus=all r8.im/stability-ai/stable-diffusion@sha256:a9758cbfbd5f3c2094457d996681af52552901775aa2d6dd0b17fd15df959bef```

### To run the Python GUI
```py stable_diffusion_gui.py```

![image](https://user-images.githubusercontent.com/14037175/187816332-ae1d407e-6953-4a01-a7d1-aed94c2112ec.png)
