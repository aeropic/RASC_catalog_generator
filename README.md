# RASC_catalog_generator

This is a python script to build a catalog of your RASC_finest_NGC_objects  astrophotographies (see https://www.rasc.ca/finest-ngc-objects)

The Finest NGC list, compiled by Alan Dyer and published in the annual RASC Observer's Handbook, complements the Messier Catalogue, as there is no overlap. The list of 110 deep-sky objects includes many fine deep-sky treasures as well as a few some mildly challenging objects.

I already developped a Messier and a Caldwell catalog here is the RASC! 

As the RASC catalog is an extract of the NCG one, simply organize your image files in a folder and add the string "NGC1,  ... NGCxyz" to the image names.
Place the "RASC_generator.py" script and the "RASC.bat" file in the same folder. Double-click on RASC.bat, accept the Windows prompts, then at first run it will import automatically the require libraries and it generates an interactive HTML contact sheet.

<img width="1661" height="760" alt="RASC_cata" src="https://github.com/user-attachments/assets/6abbb0a9-4382-49db-955f-f130fff1c2ab" />

- thumbnails are created and stored into a "thumbnails" folder
- The thumbnails are clickable to access the zoomable image.
- empty thumbnails show the best season to take the picture and gives the type of object (Nebula, Galaxy...)
- reference of each NCG object (eg NGC4048) is clickable and points to telescopius page for the clicked object.
- when placing the mouse over the thumbnail area of an object, main characteristics are displayed into a floating window. When the object is already catalogued you get as well the image name and the date of acquisition
- The "marathon" score is displayed at the top .

At the top of the page, you'll find some buttons to filter the accessible objects by season.
<img width="1331" height="598" alt="RASC_automn" src="https://github.com/user-attachments/assets/89b3f8cb-76ae-4830-baaa-cbb549568b23" />


  
If there are multiple objects in the same image, name the file with both objects.

The .bat file, of course, only runs on PC...

Let me know if it works for you too and if you see any improvements we could make! 

Note: Open and edit the .bat file to specify the path to your Python installation. I pointed to SIRIL's path:
- :: Launch Python on the script located in the same folder:
- "C:\Program Files\Siril\python\python.exe" "RASC_generator.py"

You can easily translate the script in any langage as all strings are gathered at the top of the script... Meanwhile in french except the object description in english!
