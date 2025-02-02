from main import app, db, Cafe


# I use this module to edit my database in Testing

with app.app_context():
    cafe = Cafe.query.filter_by(name="Emmerys Nørrebro").first()  # Fetch cafe
    
    new_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2249.0183339109362!2d12.559268554986224!3d55.68866900553238!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46525306df2bfdcb%3A0xeddd222779e262ea!2sEmmerys!5e0!3m2!1sen!2sde!4v1738497906298!5m2!1sen!2sde"
    cafe.map_url = new_url  # Update the field
    
    db.session.commit()  # Save changes
    print("Database updated with embed URLs!")