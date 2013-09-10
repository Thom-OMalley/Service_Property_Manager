Service Property Manager by Thomas O'Malley at the Illinois State Geological Survey

1. Run the Service_Property_Manager.exe
2. Click "Setup" the first time
3. Fill in your contact info
4. Navigate to the folder containing your CFG files
	Default folder location = DRIVE:\Program Files (x86)\ArcGIS\Server10.0\server\user\cfg\aasggeothermal
5. Click 'Use Tags' to use the Map Document Properties tags from an MXD of the same name as the service keywords
6. Navigate to the folder containing your MXD files (this one searches several folders down for the files)
7. Type in the names of the services you wish to edit (exclude file extensions)
8. All the WFS and WMS service properties will be populated, including the correct Namespace
9. A box will appear at the end and display any errors that occurred during the process

After the first time setup, at the first window you can choose "Run" and it will jump straight to where you type in the services to edit.  Your choices are not only saved, but they will populate the empty fields if you click Setup again.  So if you want to change just one thing, you don't have to re-enter everything.


Notes:

You may need to install Microsoft Visual C++ 2008 redistributable.

Service name and MXD file name must match (case sensitive) in order to Use Tags.

The information you enter is saved in a folder named "CFG_Editor" in your My Documents folder.

This program will restart the ArcGIS SOM (Service Object Manager), which will take the services down for a brief few seconds.

You should NOT have to Clear the Cache after running this program, the automatic SOM restart should be enough.

If the program cannot match a schema to the service, it will still run and edit the other properties, but the WFS namespace will be populated with "null."  An error message will inform you of this so you do not have to check the namespace every time.