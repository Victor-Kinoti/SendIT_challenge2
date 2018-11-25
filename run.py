from app import create_app
from db.create_tables import DatabaseConnection


app = create_app()

db = DatabaseConnection


@app.cli.command()
def destroy():
    db.destroy_tables()

#
# app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
