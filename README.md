# Nuclei

# todays goals

- [x] impliment the front end
  - [x] create application flow
  - [x] create clean index page
  - [x] create good compression flow for images
  - [x] create easy indexer for images
  - [x] figure out if we can use a single image for all pages

# File Structure
```py

H:.
|   Compressed_2295819.jpg
|   image.jpg
|   main.py
|   poetry.lock
|   pyproject.toml
|   README.md
|   session_goals.md
|   tree_file.txt
|   tree_structure.py
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
    |   |       index.html
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