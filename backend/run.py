from app import create_app

# Puedes configurar el entorno aquí, como 'dev', 'test', o 'prod'
app = create_app()

if __name__ == "__main__":
    app.run()
