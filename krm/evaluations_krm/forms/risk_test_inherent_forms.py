from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from krm.evaluations_krm.models import RiskTestInherent


class RiskTestInherentUreateForm(ModelForm):

    class Meta:
        model = RiskTestInherent
        fields = [
            'impact_level_expert',
            'probability_level_expert',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["impact_level_expert"].widget.attrs["class"] = "form-select"
        self.fields["probability_level_expert"].widget.attrs["class"] = "form-select"
