# micro-ds
Capture audio on your NDS and send it to the PC via WIFI

<p align=center>
[![Youtube](https://img.youtube.com/vi/GOZne7amyPI/0.jpg)](https://www.youtube.com/watch?v=GOZne7amyPI)

<h2 align="center">Dependencies</h2>
<ul>
 <li>linux</li>
<li>DevkitPro, easiest way to download it is through pacman: https://devkitpro.org/wiki/Getting_Started</li>
</ul>

<h2 align="center">Usage</h2>

<ul>
 
 <li> create hotspot on your laptop </li>
 <li> run .nds file on your NDS </li>
 <li> connect to your hotspot on your NDS via the .nds file </li>
 <li> run the python script: desktop_client.py </li> 
 
</ul>

<h2 align="center">How it works</h2>

<ul>
<li>NDS opens port 8080, python script connects PC to it, then:</li>
  <ul>
    <li> NDS receives ACK character from PC</li>  
    <li> NDS records 5 seconds of audio</li>  
    <li> NDS sends buffered audio </li>
    <li> python saves it in file and plays</li>
    </ul>
</ul>

<h2 align="center">How to make WIFI hotspot that NDS can connect (it's not that obvious):</h2>

<ul>
<li>in Ubuntu open "Network Connections" and click "add new"</li>
<li>go to the "Wi-Fi security" - NDS supports only WEP security (so remember, it's dangerous to beacon that poorly secured network all the time, use this hotspot only when playing with your NDS) - select "WEP 40/128 bit key (Hex or ASCII)" </li>
 <li> select some random 5 character (only digits) password </li>
 <li> in "Wi-Fi" tab select "Mode" to "Hotspot" </li>
 <li> save it </li>
 <li> open "Network" </li>
 <li> click "Connect to to a hidden network" </li>
 <li> select network that you've just created (by default its name will be "hotspot")
 <li> you're done, if you were previously connected with another network via wifi you'll be disconnected</li>
 <li> now you can connect to this network through your NDS </li>
</ul>
