from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

def update_views(request, object):
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)#update views number
    hits = hit_count.hits#model of specific object
    hitcontext = context["hitcount"] = {"pk": hit_count.pk} #get number of hit or
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext["hitcounted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits