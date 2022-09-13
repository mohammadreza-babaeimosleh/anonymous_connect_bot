# anonymous_bot
telegram bot template

## how to use

to run the bot, at first, add PYTHONPATH to /src working directory s=using command below:
```bash
export PYTHONPATH=${PWD}
```
then add your bots' token to your local enviroment variables using command below:
```bash
export anonymous_bot_token=<your token>
```
now you can run the code by command
```bash
python ./src/run.py
```
## requirements
after installing requirement.txt file using command
```bash
pip install -r requirements.txt
```
you need to install `MongoDB` on your system or terminal
you can do it via this [Link](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)  
*note* : if you are using wsl it can be a little tricky to insall MongoDB  
after installing MongoDB you can use `MongoDBCompass` app to have a visual look in your database
