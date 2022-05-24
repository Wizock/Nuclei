# Nuclei

## todays goals

- [ ] compression implimentation
  - [ ] need to figure out video static 
  - [ ] test different compression commands on videos to test quality against bytes compressed
- [ ] <https://pythonhosted.org/python-gnupg/>
- [ ] UI revamp
  - [ ] add individual media view
  - [ ] add individual media edit
  - [ ] implement tiled dashboard view

- [ ] implement the video media player
  - [ ] create a video player
  - [ ] create a video player controls
  - [ ] create a video player controls container
  - [ ] implement video compression flow
  - [ ] design video media models
  - [ ] index video media

# File Structure
## *1275* lines of code  
```bat
C:.
|   .gitattributes
|   .gitignore
|   build_md.py
|   lines_file.md
|   main.py
|   poetry.lock
|   project_lines.txt
|   project_line_counter.py
|   pyproject.toml
|   README.md
|   tree_file.txt
|   
\---nuclei
    |   config.py
    |   __init__.py
    |   
    +---admin_interface
    |   |   config.py
    |   |   models.py
    |   |   tests.py
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---templates
    |   |       index.html
    |   |       
    |           
    +---authentication
    |   |   config.py
    |   |   models.py
    |   |   tests.py
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---templates
    |   |       landing_page.html
    |   |       login.html
    |   |       register.html
    |   |       
    |           
    +---compression_service
    |   |   config.py
    |   |   models.py
    |   |   tests.py
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---static
    |   |   +---compressed
    |   |   |       Capture.PNG
    |   |   |       cody-fitzgerald-s5A30N0oBEw-unsplash.jpg
    |   |   |       Screenshot_2.png
    |   |   |       
    |   |   \---imgs
    |   |           Capture.PNG
    |   |           cody-fitzgerald-s5A30N0oBEw-unsplash.jpg
    |   |           Screenshot_2.png
    |   |           
    |   +---templates
    |   |       dashboard.html
    |   |       grouped_rendering.html
    |   |       individual_display.html
    |   |       upload_template.html
    |   |       
    |   +---video_compression
    |   |   |   compression_preset.py
    |   |   |   input.mp4
    |   |   |   test_compression.py
    |   |   |   video_parse.py
    |   |   |   views.py
    |   |   |   __init__.py
    |   |   |   
    |   |           
    |           
    +---database
    |       nuclei.db
    |       
    +---extension_globals
    |   |   admin.py
    |   |   celery.py
    |   |   cookies.py
    |   |   database.py
    |   |   kafka.py
    |   |   mail.py
    |   |   praetorian.py
    |   |   redis.py
    |   |   security.py
    |   |   __init__.py
    |   |   
    |           
            


```
