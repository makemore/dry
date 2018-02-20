from spots.models import SpotPage

def spots(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    spots = SpotPage.objects.all()
    return {'spots': spots}