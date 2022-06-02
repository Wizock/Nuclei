# Nuclei
## quickstart
```bat
pip install poetry
poetry install

poetry run ./main.py
```

## todays goals
 - impliment this: https://platform.uno/
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
## *1673* lines of code  

```bat
Nuclei:
|   main.py
|   poetry.lock
|   pyproject.toml
|   README.md
|   requirements.txt
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
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---static
    |   +---templates
    |   |       landing_page.html
    |   |       login.html
    |   |       register.html
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
    |   |   |       
    |   |   \---imgs
    |   |           
    |   +---templates
    |   |       grouped_rendering.html
    |   |       individual_display.html
    |   |       upload_template.html
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
    |           
    +---index_mvc
    |   |   index_view.py
    |   |   
    |   +---templates
    |   |       dashboard.html
    |           
    +---tests
    |   |   authentication_test.py
    |   |   conftest.py
    |   |   image_test.py
    |   |   main_tests.py
    |   |   video_test.py
    |   |   __init__.py
    |           
    +---video_compression
    |   |   assemble_records.py
    |   |   compression_preset.py
    |   |   models.py
    |   |   views.py
    |   |   __init__.py
    |   |   
    |   +---static
    |   |   +---compressed
    |   |   |       
    |   |   \---videos
    |   |           
    |   +---templates
    |   |       grouped_rendering.html
    |   |       individual_display.html
    |   |       upload_template.html
    |   |       video_player.html
    |   |       
    |           
            
```
