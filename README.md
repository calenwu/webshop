features:
global coupon
free gift

todo:
fix credit coupon
readme, github gitlab
image invoice url

fix:
payment method page loading time


#need to install on ubuntu:
sudo apt-get install wkhtmltopdf
sudo apt-get install gettext

#before first makemigration
comment out profile picture
remove wagtail_modeltranslation from apps
remove all apps

#prep
sudo docker-compose run --rm webshop python manage.py loaddata blog/fixtures/setting cart/fixtures/setting contact/fixtures/setting home/fixtures/title order/fixtures/country order/fixtures/setting order/fixtures/shipping_method shop/fixtures/setting winwheel/fixtures/winwheel
sudo docker-compose run --rm webshop python manage.py createsuperuser

#setup
First add categories: 

Go into every setting and set variables
make countries available

blog categories: Snippets > Blog categories
product categories: Snippets > Product categories
product size categories: Snippets > Product size categories
