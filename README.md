# TikTok Algorithms (X-Gorgon, X-Khronos, XLOG 02, TTEncrypt 05, X-Argus, X-Ladon)

[![IPRoyal](assets/proxy.jpg)](https://iproyal.com/?r=ttproxy)

These are just few of TikTok algorithms that is used by the mobile application. It might be useful for your next TikTok project.

## Contains?
- X-Gorgon and X-Khronos v0404
- XLOG 02 encrypt/decrypt
- TTEncrypt (also often called Device Register/Applog) encrypt/decrypt
- Captcha Solver
- X-Argus
- X-Ladon

## Requirements
- Check `requirements.txt`
- Some dependencies might be missing, 

## How to use?
- `pip install -r requirements.txt`
- `uvicorn main:app --reload --host 0.0.0.0 --port 8100`
- You now have FastAPI rest client on port 8100 (http://127.0.0.1:8100)

See `main.py` file and see usage example of each algorithm implementations.

## Want to contribute?

Sure, make a pull request.

[![IPRoyal](assets/proxy.jpg)](https://iproyal.com/?r=ttproxy)

## Disclaimer

Won't be responsible if used this for other purposes than educational. 

Again, **USE THIS FOR EDUCATIONAL PURPOSES ONLY**
