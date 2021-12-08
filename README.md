# Game Server

## Requirements
This server runs on python. I used version 3.10 (latest version).   
You must also have the twisted package installed. You can do this using <code>pip install twisted</code> or <code>pip3 install twisted</code>

## Starting the server
To start the server run <code>python server.py</code> or <code>python3 server.py</code>. This will start the server on port 8000.

## In-game commands
<code>login (name)</code> - Logs you into the game. You must provide a name, which will be shared with other players. When you connect you will be given the location, name and points of each player.  
<code>move (north/south/east/west)</code> - Moves you in the given direction by one unit.  
<code>quit</code> - Disconnects you from the server and takes you out of the game.   
<code>map</code> Sends you the map.

## Auto-updates
You will automaticly be notified when ever a player move and/or finds a treasure.

## Other
If you quit the game and then join, your location and points will be renembered.   
If sombody finds a treasure, then the point value is awarded to them, and the treasure is removed from the map.   
When the server is started a list of treasures is automaticly populated with each being at a random location with a random point value.   
There is currently no command to get the status of the players. Player status is automaticly posted whenever a player moves.   
This map has no obstacles or hidden areas.   
Because of the lack of obstacles, the players aren't given the locations of the treasures.

## Console/debug
The script will print a message whenever a new connection is made.   
For now, the locations of the treasures are printed at startup. This is for testing/debuging purposes.

# Client

## Requirements
This client runs on python. I used version 3.10 (latest version). 
You must also have the tkinter package installed. You can do this using <code>pip install tk</code> or <code>pip3 install tk</code>

## Starting the client
To start the client run <code>python client.py</code> or <code>python3 client.py</code>. This will start the client.  
By default this will connect to the server localhost on port 8000. To change this update the relevent lines at the beginning of client.py.

## Using the client
This is a GUI application. First you will be prompted to enter your name. Then, you can click the button, or press the enter key on your keyboard to proceed. If you accidently entered an invalid name and submited it, you will need to close the client and re-launch it. On the next screen, you can type out the commands in the box, and either click the button or press the enter key on your keyboard to send it. Optionally you can use the arrow keys to move rapidly. Pressing the up arrow key will cause you to move north, the down arrow key will move you south, the left arrow key will move you west and the right arrow key will move you east.
