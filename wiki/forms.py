from django import forms

from .models import Revision


class RevisionForm(forms.ModelForm):

    revision_pk = forms.IntegerField(required=False, widget=forms.HiddenInput())
    message = forms.CharField(required=False, help_text="Leave a helpful message about your change")

    def __init__(self, *args, **kwargs):
        self.revision = kwargs.pop("revision")
        super(RevisionForm, self).__init__(*args, **kwargs)
        if self.revision:
            self.fields["content"].initial = self.revision.content
            self.fields["revision_pk"].initial = self.revision.pk
        else:
            self.fields["content"].initial = "add content and create a new page"
            self.fields["message"].initial = "initial revision"

    def clean_content(self):
        if self.revision and self.cleaned_data["content"] == self.revision.content:
            raise forms.ValidationError("You made no stinking changes")
        return self.cleaned_data["content"]

    def clean(self):
        if self.revision and self.cleaned_data.get("revision_pk") != self.revision.pk:
            raise forms.ValidationError("Someone edited this before you")
        return self.cleaned_data

    class Meta:
        model = Revision
        fields = [
            "revision_pk",
            "content",
            "message"
        ]
