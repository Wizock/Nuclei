# Nuclei

# todays goals

- [ ] impliment the front end
  - [ ] create application flow
  - [x] create clean index page
  - [x] create good compression flow for images
  - [x] create easy indexer for images
  - [ ] figure out if we can use a single image for all pages

# File Structure

```bat
H:.
|   main.py
|   poetry.lock
|   pyproject.toml
|   README.md
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
    |           
    +---authentication
    |   |   config.py
    |   |   models.py
    |   |   tests.py
    |   |   views.py
    |   |   __init__.py
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
    |   |   |       2295819.jpg
    |   |   |       
    |   |   \---imgs
    |   |           2295819.jpg
    |   |           
    |   +---templates
    |   |       dashboard.html
    |   |       indexed_view.html
    |   |       individual_display.html
    |   |       
    |           
    +---database
    |       nuclei.db
    |       
    +---extension_globals
    |   |   database.py
    |   |   praetorian.py
    |   |   __init__.py
    |   |   
    |           
```
