# 1063487350460910/feed?fields=story,updated_time,id,message,place,picture,attachments
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os, requests, json
import pprint, django, sys, tempfile
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dry.settings")

if not hasattr(django, 'apps'):
    django.setup()

from django.core.files.images import ImageFile
from wagtail.wagtailimages.models import Image
from django.utils.text import slugify

from django.core import files
from spots.models import SpotPage
from wagtail.wagtailcore.models import Page
import dateutil.parser

pp = pprint.PrettyPrinter(indent=4)

SpotPage.objects.all().delete()

get_images = True

"""
GET /oauth/access_token?  
    grant_type=fb_exchange_token&           
    client_id={app-id}&
    client_secret={app-secret}&
    fb_exchange_token={short-lived-token} 
    """


def get_long_access_token(short_token):
    payload = requests.get(
        "https://graph.facebook.com/v2.12/oauth/access_token?grant_type=fb_exchange_token&" +
        "client_id=" + os.environ.get("FB_APP_ID") + "&client_secret=" + os.environ.get(
            "FB_APP_SECRET") + "&fb_exchange_token=" + short_token,
        headers=headers)
    print(payload.text)


def process_page_of_data(data):
    spot_index_page = Page.objects.get(id=4)
    for post in data:
        first_time_create = False
        post_has_changed = True

        try:
            spot_page = SpotPage.objects.get(facebook_id=post["id"])
            if spot_page.facebook_updated == dateutil.parser.parse(post["updated_time"]):
                post_has_changed = False
        except SpotPage.DoesNotExist:
            spot_page = SpotPage()
            first_time_create = True

        if post_has_changed:
            spot_page.facebook_id = post["id"]
            spot_page.facebook_updated = dateutil.parser.parse(post["updated_time"])
            spot_page.facebook_created = dateutil.parser.parse(post["created_time"])

            if "message" in post:
                spot_page.title = post["message"][:70]
                spot_page.body = post["message"].replace('\n', '<br />')
            else:
                spot_page.title = "None"

            # pp.pprint(post)

            if get_images and spot_page.image is None and "full_picture" in post:

                request = requests.get(post["full_picture"], stream=True)
                print("doing image")
                # Was the request OK?
                if request.status_code != requests.codes.ok:
                    # Nope, error handling, skip file etc etc etc
                    continue

                # Get the filename from the url, used for saving later
                file_name = slugify(spot_page.title) + ".jpg"

                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in request.iter_content(1024 * 8):
                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)

                # Create the model you want to save the image to
                # image = Image()
                image = Image(
                    title=file_name,
                    # image_file is your StringIO/BytesIO object
                    file=ImageFile(files.File(lf), name=file_name),
                )
                # Save the temporary image to the model#
                # This saves the model so be sure that is it valid
                # image.image.save(file_name, files.File(lf))
                image.save()
                spot_page.image = image
            else:
                print("not doing image")

            # later when a cms user updates the page manually
            # there will be no first revision to compare against unless
            # you add a page revision also programmatically.
            # print(post["place"])
            if "place" in post:
                print("doing place")
                spot_page.address = post["place"]["name"]
                spot_page.location = str(post["place"]["location"]["latitude"]) + "," + str(
                    post["place"]["location"]["longitude"])
            else:
                print("not doing place")
            if first_time_create:
                spot_index_page.add_child(instance=spot_page)

            print(spot_page.facebook_created)
            spot_page.save_revision().publish()
        else:
            print("post is not new or changed, doing nothing")

    # pp.pprint(post)


# print(post["message"])


headers = {
    'authorization': "Bearer " + os.environ.get("FB_USER_TOKEN"),
    'content-type': "application/json",
}

# get_long_access_token(os.environ.get("FB_USER_TOKEN"))


payload = requests.get(
    "https://graph.facebook.com/v2.12/1063487350460910/feed?fields=story,updated_time,created_time,id,message,place,full_picture,attachments",
    headers=headers)

result = json.loads(payload.text)

# print(result)

process_page_of_data(result["data"])

while "paging" in result:
    payload = requests.get(result["paging"]["next"], headers=headers)
    result = json.loads(payload.text)
    process_page_of_data(result["data"])
