from django import forms

from .validators import validate_url, validate_dot_com


class SubmitUrlForm(forms.Form):
    url = forms.CharField(
        label='',
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your URL",
                "class": "form-control"
            }
        )
    )
    shortcode = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': "Enter your Shortcode (Optional)",
                'class': "form-control"
            }
        ),
        required=False
    )

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'https' in url:
            if url[8:12] == 'www.':
                return url
            else:
                return url[0:8] + "www." + url[8:]
        elif 'http' in url:
            if url[7:11] == 'www.':
                return url
            else:
                return url[0:7] + "www." + url[7:]
        else:
            if url[0:4] == 'www.':
                return "http://" + url
            else:
                return "http://www." + url
