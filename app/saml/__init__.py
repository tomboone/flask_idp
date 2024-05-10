from app.saml.models.flaskloginidentityprovider import FlaskLoginIdentityProvider

samlidp = FlaskLoginIdentityProvider()  # Create the FlaskLoginIdentityProvider
samlbp = samlidp.create_blueprint()  # Create the blueprint for the FlaskLoginIdentityProvider
