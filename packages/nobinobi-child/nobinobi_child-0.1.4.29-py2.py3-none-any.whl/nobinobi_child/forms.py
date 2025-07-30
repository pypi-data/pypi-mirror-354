#  Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Hidden, Field
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from nobinobi_child.models import Absence, Child


class LoginAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/accounts/login/'
        self.helper.form_show_labels = False
        self.helper.form_tag = True
        self.helper.layout = Layout(
            AppendedText('username', mark_safe('<i class="fas fa-user"></i>'), placeholder=_("Username")),
            AppendedText('password', mark_safe('<i class="fas fa-key"></i>'), placeholder=_("Password")),
            Hidden('next', '/'),
            Submit("login", _("Sign In"), css_class='btn btn-primary btn-block btn-flat'),
        )


class AbsenceCreateForm(BSModalModelForm):
    """
        A form to create an absence record.

        This form initializes with default values for the start date and filters
        the child queryset based on the classroom or classrooms provided in the request.
    """
    child = forms.ModelChoiceField(label=_("Child"),
                                   queryset=Child.objects.filter(status=Child.STATUS.in_progress),
                                   )

    class Meta:
        model = Absence
        fields = ["child", "start_date", "end_date", "type"]
        widgets = {
            "start_date": DateTimePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY HH:mm"}),
            "end_date": DateTimePickerInput(range_from="start_date", options={"locale": "fr", "format": "DD/MM/YYYY HH:mm"}),
        }

    def __init__(self, *args, **kwargs):
        """
            Initialize the AbsenceCreateForm.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Keyword Args:
                initial (dict): Initial data for the form fields.
                request (HttpRequest): The request object containing GET parameters.

            The form initializes the 'start_date' field with the current date and time
            set to 6:00 AM if no initial data is provided. It also filters the 'child'
            field queryset based on the 'classroom' or 'classrooms' GET parameters.
        """
        super(AbsenceCreateForm, self).__init__(*args, **kwargs)

        # Remove required fields for autofill if empty
        self.fields['end_date'].required = False

        # Set default start_date if not provided in initial data
        if not kwargs.get('initial', None):
            if not self.initial.get('start_date', None):
                self.initial['start_date'] = timezone.localtime().replace(hour=6, minute=0, second=0)

        now = timezone.localdate()

        # Filter child queryset based on 'classroom' GET parameter
        if kwargs["request"].GET.get("classroom"):
            filter_child = Child.objects.filter(status=Child.STATUS.in_progress)
            classroom = int(kwargs["request"].GET.get("classroom", 0))
            self.fields['child'].queryset = filter_child.filter(
                Q(classroom__id=classroom) |
                Q(replacementclassroom__classroom_id=classroom) &
                Q(replacementclassroom__from_date__lte=now) &
                Q(replacementclassroom__end_date__gte=now) &
                Q(replacementclassroom__archived=False)
            ).distinct()

        # Filter child queryset based on 'classrooms' GET parameter
        if kwargs["request"].GET.get("classrooms"):
            filter_child = Child.objects.filter(status=Child.STATUS.in_progress)
            classroom_list = [int(x) for x in str(kwargs["request"].GET.get("classrooms")).split(",")]
            self.fields['child'].queryset = filter_child.filter(
                Q(classroom__in=classroom_list) |
                Q(replacementclassroom__classroom_id__in=classroom_list) & Q(replacementclassroom__from_date__lte=now) &
                Q(replacementclassroom__end_date__gte=now) &
                Q(replacementclassroom__archived=False)
            ).distinct()

    def clean(self):
        cleaned_data = super().clean()
        # autofill end_date if empty with same date but at night for 1 day
        end_date = cleaned_data.get('end_date')
        if not end_date:
            cleaned_data['end_date'] = timezone.localtime().replace(hour=22, minute=0, second=0)
        return cleaned_data


class ChildPictureSelectForm(forms.ModelForm):
    child = forms.ModelChoiceField(
        label=_("Child"),
        queryset=Child.objects.filter(status=Child.STATUS.in_progress),
    )

    class Meta:
        model = Child
        fields = ("child",)

    def __init__(self, *args, **kwargs):
        super(ChildPictureSelectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-child-picture-select'
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"

        self.helper.add_input(Submit('submit', _("Submit")))


class ChildPictureForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ("picture",)

    def __init__(self, *args, **kwargs):
        super(ChildPictureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-child-picture-select'
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.attrs['enctype'] = "multipart/form-data"
        self.helper.layout = Layout(
            Field("picture"),
            Submit('submit', _("Submit"))
        )


class ChildPictureUpdateForm(BSModalModelForm):
    class Meta:
        model = Child
        fields = ("picture",)
