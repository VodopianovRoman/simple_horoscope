                                          # Simple horoscope

  What is it?
  -----------
  
  A simple application written in python using Django. 
  Shows information about the desired zodiac sign and horoscope for the current date.
  
  Installation
  ------------
  
  Runs like all Django applications with the command:
  python manage.py runserver
  
  How it works?
  ------------
  
  With the help of the reguests library, a get request is sent to the site. 
  The received information is transferred to bs4, after which the forecast is transferred from the view to the url.
