from spots.models import SpotPage

def spots(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    spots = SpotPage.objects.order_by("-facebook_created")
    return {'spots': spots}