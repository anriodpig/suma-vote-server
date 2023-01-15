# SUMA Vote Server

Suma Group Internal Tool   
Written by ahuitec/Cubic

# How to Use
Windows : Double Click "start_server.bat" . The server would be accessiable on port 7000(runtime) or 8080(debug)   
if you a using a server, make sure you have those port open through your firewall    
otherwise, start your frp to those ports     
Linux : python(3) webio_release.py or run "bash start_server" in your terminal instead    

# Maintenance
## Static Resource
All static resource is stored in folder "static", during your edit, make sure no songs in same name but from different bands.   
This could cause issue and already happend once. Though rare, make sure no such issue happen again.   
## Dynamic Resource
The dynamic folder contains all server data;   
database.txt  ->   All vote data isolated with '|', readable in csv mode    
log.txt       ->   All error data
qq.txt        ->   QQ numbers used (blacklist)   
songs.txt     ->   Songs used (blacklist)    
## Editing Voting Information
It requires a server restart to reload stored data in dynamic folder aka the server data.   
So just close server, edit the qq.txt and songs.txt and the database.txt and restart server.    
This is predicted to be simplified with future updates. With no need to restart server.   
## Mapping Variables
Variables are mapped to physical files in function "file_path(param)" 
edit lines inside can remap the files.   
## Time
You can edit the server_xxx_time var at the end of main .py file. to set an scheduled open/close server operation.    
Server will automatically shutdown or stay closed till the time you set.   


