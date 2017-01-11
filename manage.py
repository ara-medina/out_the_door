import os
from flask.ext.script import Manager

from out_the_door import app
from out_the_door.database import session
from out_the_door.models import Account, Profile

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()
    
@manager.command
def seed():
    caption = """Lorem ipsum dolor sit amet, consectetur adipisicing elit"""
    age = 25
    gender = "Female"
    city = "Philadelphia"
    occupation = "Web Developer"
    income = "1,000,000"
    ethnicity = "White"

    for i in range(5):
        profile = Profile(
            title="Test Profile #{}".format(i),
            caption=caption,
            age=age,
            gender=gender,
            city=city,
            occupation=occupation,
            income=income,
            ethnicity=ethnicity
        )
        session.add(profile)
    session.commit()