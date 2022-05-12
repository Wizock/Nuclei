# Nuclei

## todays goals

- [ ] compression implimentation
  - [ ] test different compression commands on videos to test quality against bytes compressed

- [ ] UI revamp
  - [ ] add individual media view
  - [ ] add individual media edit
  - [ ] implement tiled dashboard view

- [ ] security measures
  - [ ] create a admin/superuser dashboard page
  - [ ] create a admin/superuser protected edit page
  - [ ] create a admin/superuser protected view page
  - [ ] create a design models for the admin/superuser dashboard
  - [ ] implement password reset functionality
  - [ ] create password reset email
  - [ ] hash uncompressed images
  
- [ ] security measures
  - [ ] create a admin/superuser password protected login 2
  - [ ] create a admin/superuser password protected logout 2
  - [ ] create a admin/superuser protected registration 2
  - [ ] create a admin/superuser dashboard page
  - [ ] create a admin/superuser protected upload page 2
  - [ ] create a admin/superuser protected delete page 2
  - [ ] create a admin/superuser protected edit page
  - [ ] create a admin/superuser protected view page
  - [ ] create a design models for the admin/superuser dashboard
  - [ ] impliment password reset functionality 2
  - [ ] hash passwords 2
  - [ ] create password reset email
  - [ ] hash uncompressed images

- [ ] implement the video media player
  - [ ] create a video player
  - [ ] create a video player controls
  - [ ] create a video player controls container
  - [ ] implement video compression flow
  - [ ] design video media models
  - [ ] index video media

# Project Size

## lines of code
Project lines: 653891
## amount of files
Project files: 235

# File Structure
```bat

Folder PATH listing for volume Windows
Volume serial number is 165C-21C8
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