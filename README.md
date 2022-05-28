# Nuclei

## todays goals

- [ ] compression implimentation
  - [x] need to figure out video static 
  - [ ] test different compression commands on videos to test quality against bytes compressed
- [ ] <https://pythonhosted.org/python-gnupg/>
- [ ] UI revamp
  - [x] add individual media view
  - [ ] add individual media edit
  - [ ] implement tiled dashboard view

- [ ] implement the video media player
  - [x] create a video player
  - [ ] create a video player controls
  - [ ] create a video player controls container
  - [x] implement video compression flow
  - [x] design video media models
  - [x] index video media

# File Structure
## *1377* lines of code  
```bat

|   .gitattributes
|   .gitignore
|   main.py
|   Nuclei.code-workspace
|   poetry.lock
|   pyproject.toml
|   README.md
|   tree_file.txt
|   
+---misc
|       build_md.py
|       project_line_counter.py
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
    |   +---static
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
    |   +---static
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
    |   |   |       20220214_151843.jpg
    |   |   |       download.jpg
    |   |   |       
    |   |   \---imgs
    |   |           20220214_151843.jpg
    |   |           Annotation_2022-04-14_110949.png
    |   |           download.jpg
    |   |           example.mp4
    |   |           
    |   +---templates
    |   |       grouped_rendering.html
    |   |       individual_display.html
    |   |       loading.html
    |   |       upload_template.html
    |   |       video_player.html
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
    +---index_mvc
    |   |   index_view.py
    |   |   
    |   +---templates
    |   |       dashboard.html
    |   |       
    |           
    +---video_compression
    |   |   assemble_records.py
    |   |   compression_preset.py
    |   |   example.mp4
    |   |   input.mp4
    |   |   models.py
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---static
    |   |   \---videos
    |   +---templates
    |   |       grouped_rendering.html
    |   |       individual_display.html
    |   |       loading.html
    |   |       upload_template.html
    |   |       video_player.html
    |   |       
    |           

```
