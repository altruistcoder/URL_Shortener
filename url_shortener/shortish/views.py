from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from analytics.models import ClickEvent

from .forms import SubmitUrlForm
from .models import ShortishURL


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "Shortish.in",
            "form": the_form
        }
        return render(request, "shortish/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Shortish.co",
            "form": form
        }
        template = "shortish/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            new_shortcode = form.cleaned_data.get("shortcode")
            if new_shortcode == "" or new_shortcode is None:
                q_set = ShortishURL.objects.filter(url__iexact=new_url)
                if q_set.count() != 0:
                    obj = q_set.first()
                    created = False
                else:
                    obj = ShortishURL.objects.create(url=new_url)
                    created = True
            else:
                q_s = ShortishURL.objects.filter(shortcode__iexact=new_shortcode).exists()
                if q_s:
                    obj = ShortishURL.objects.get(shortcode=new_shortcode)
                    created = False
                    print(obj.url)
                    if obj.url != new_url:
                        return render(request, "shortish/shortcode-invalid.html")
                else:
                    obj = ShortishURL.objects.create(url=new_url, shortcode=new_shortcode)
                    created = True
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortish/success.html"
            else:
                template = "shortish/already-exists.html"

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = ShortishURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
