from nuclei import app, import_tables

import_tables(app)

if __name__ == "__main__":
    
    app.run(debug=True)

