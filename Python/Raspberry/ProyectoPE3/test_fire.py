import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/Desktop/ProyectoPE3/proyecto-practicas-e3-firebase-adminsdk-jj1tc-6e66acd5ce.json')


# Initialize the app with a service account, granting admin privileges

firebase_admin.initialize_app(cred, {

    'databaseURL': 'https://proyecto-practicas-e3-default-rtdb.firebaseio.com/'

})


ref = db.reference('message')

print(ref.get())

print ('Ok !')