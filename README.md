# Nuclei

# todays goals

- [ ] impliment the front end
  - [ ] create application flow
  - [ ] create clean index page
  - [ ] create good compression flow for images
  - [ ] create easy indexer for images
  - [ ] figure out if we can use a single image for all pages

# File Structure
```bat
H:.
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
    |   |       indexed_view.html
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
