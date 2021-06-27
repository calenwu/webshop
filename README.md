# webshop

webshop is an online shop built with the wagtail/django framework

## Installation

install the following packages (tested on Ubuntu 21.04)

```bash
apt install -y fonts-liberation \
    gettext\
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxtst6 \
    wkhtmltopdf \
    xdg-utils
```

## Before running makemigrations for the first time
1. Comment out the `profile_picture` field in `account.models.User`
1. Comment out `wagtail_modeltranslation` from `INSTALLED_APPS` in `settings`
1. Comment out all apps from this folder from `INSTALLED_APPS` in `settings`
1. Finally run manage.py makemigrations
1. Uncomment the previous comments

## Preparation
Run manage.py migrate
```bash
manage.py migrate
```
Load fixtures to load the keys needed for the settings:
``` bash
manage.py loaddata blog/fixtures/setting cart/fixtures/setting contact/fixtures/setting home/fixtures/title order/fixtures/country order/fixtures/setting order/fixtures/shipping_method shop/fixtures/setting winwheel/fixtures/winwheel
```
Create a superuser
``` bash
manage.py createsuperuser
```

## Setting up the webshop
### Adding a product for the first time
Each Product belongs to a `ProductCategory` and `ProductSizeCategory`. Therefore you need to create those first (in the Snippets panel). After creating those 2 you have to create `ProdutSize` (in the Snippets panel). Add the size to a `ProductCategory`.  
The user can select between those sizes for the product given the `ProductCategory` for the `Product` in the shop.  
Finally you can add a `ProductPage`. But first you need to create a `ProductListingPage` under the `HomePage`.  
Fill out all needed fields and then on the top bar switch from "CONTENT" to "PRODUCT VARIATIONS".  
Add as many `ProductColor` as you like, but do not click the "ADD QUANTITY" button.
Those will be created automatically after publishing the page.
So after filling out the form click on "PUBLISH" on the bottom bar. 
Now edit the `ProductPage` again. You now can see in the "PRODUCT VARIATIONS" tab that each `ProductColor` has a `ProductQuantity` subpanel. In there you can enter how much stock there is for each `ProductSize`.

### Other models
The other models are rather self explanatory. So I will not cover them.

### Settings Panel
In the wagtail admin page you can find a "Settings" tab. There you can find all model Settings. Just go through all of them and enter whatever is asked. The key name should tell you what you need to fill in. If there are no keys you didnt run `load fixtures`.  
Not that all keys asking for true/false, the value should be yes/no.

## Notes
In `settings` do not forget to change the database settings. The only 2 other important things in the settings are the `BASE_URL` setting and the `EMAIL` settings.

## To do's (important):
Fix credit coupons: if 2 people check out at the same time with the same credit coupon. The coupon will go into negative balance. Unfortunately I dont know how to solve that problem.

## Features to add:
* Global coupon: coupon which is added automatically.
* Free gift: Free item added to the cart, when a certain cart value has been reached.

## Thanks:
These projects were used in the making of this application:
* [Django](https://github.com/django/django)
* [wagtail](https://github.com/wagtail/wagtail)
* [tailwind](https://github.com/tailwindlabs/tailwindcss)
* [fontawesome](https://github.com/FortAwesome/Font-Awesome)
* [PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe)
* [splide](https://github.com/Splidejs/splide)
* [tagify](https://github.com/yairEO/tagify)
* [winwheel](https://github.com/zarocknz/javascript-winwheel)

## License
[MIT](https://choosealicense.com/licenses/mit/)