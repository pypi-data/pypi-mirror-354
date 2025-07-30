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

from django.contrib import admin
from django.contrib.admin import register, SimpleListFilter
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import gettext as _
from nobinobi_staff.models import Staff

from nobinobi_child.models import Period, Allergy, FoodRestriction, Language, Classroom, AgeGroup, Absence, AbsenceType, \
    AbsenceGroup, ClassroomDayOff, InformationOfTheDay, Contact, Address, ChildSpecificNeed, LogChangeClassroom, Child, \
    ChildToPeriod, ChildToContact, ReplacementClassroom, ChildTrackingLog, NobinobiChildSettings


class DefaultListFilter(SimpleListFilter):
    all_value = '_all'

    def default_value(self):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        if self.parameter_name in request.GET and request.GET[self.parameter_name] == self.all_value:
            return queryset

        if self.parameter_name in request.GET:
            return queryset.filter(**{self.parameter_name: request.GET[self.parameter_name]})

        return queryset.filter(**{self.parameter_name: self.default_value()})

    def choices(self, cl):
        yield {
            'selected': self.value() == self.all_value,
            'query_string': cl.get_query_string({self.parameter_name: self.all_value}, []),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (
                    self.value() == None and force_text(self.default_value()) == force_text(lookup)),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


@register(Period)
class PeriodAdmin(admin.ModelAdmin):
    """
        Admin View for Period
    """
    list_display = ('name', 'weekday', 'order')
    list_filter = ('weekday',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name',)
    sortable_by = ("weekday", "order",)


@register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """
        Admin View for Classroom
    """
    list_display = ('name', 'capacity', 'order', 'mode')
    list_filter = ('mode',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('allowed_login',)
    filter_horizontal = ('allowed_login', 'allowed_group_login')
    readonly_fields = ('slug',)
    search_fields = ('name', 'slug', 'capacity', 'mode')


@register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    """
        Admin View for AgeGroup
    """
    list_display = ('name',)
    readonly_fields = ('slug',)
    search_fields = ('name', 'slug')


@register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    """
        Admin View for Allergy
    """
    list_display = ('name',)
    search_fields = ('name',)


@register(FoodRestriction)
class FoodRestrictionAdmin(admin.ModelAdmin):
    """
        Admin View for FoodRestriction
    """
    list_display = ('name',)
    search_fields = ('name',)


@register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
        Admin View for Language
    """
    list_display = ('name',)
    search_fields = ('name',)


@register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    """
        Admin View for Absence
    """
    list_display = ('child', 'start_date', 'end_date', 'type')
    list_filter = ('start_date', 'end_date', 'type')
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('child__first_name', 'child__last_name')

    def get_ordering(self, request):
        """
        Hook for specifying field ordering.
        """
        settings = NobinobiChildSettings.get_settings()
        if settings.admin_child_absence_ordering == NobinobiChildSettings.OrderAbsenceChildListDisplayInAdmin.STD:
            self.ordering = ('start_date', 'end_date', 'child')
        elif settings.admin_child_absence_ordering == NobinobiChildSettings.OrderAbsenceChildListDisplayInAdmin.CHI:
            self.ordering = ('child__last_name', 'start_date', 'end_date')
        return self.ordering or ()  # otherwise we might try to *None, which is bad ;)


@register(AbsenceType)
class AbsenceTypeAdmin(admin.ModelAdmin):
    """
        Admin View for AbsenceType
    """
    list_display = ('name', 'group', 'order')
    list_filter = ('group',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name', 'group')


@register(AbsenceGroup)
class AbsenceGroupAdmin(admin.ModelAdmin):
    """
        Admin View for AbsenceGroup
    """
    list_display = ('name',)
    list_filter = ()
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name',)


class ClassroomInline(admin.TabularInline):
    model = Classroom


@register(ClassroomDayOff)
class ClassroomDayOffAdmin(admin.ModelAdmin):
    """
        Admin View for ClassroomDayOff
    """
    list_display = ('weekday',)
    list_filter = ('weekday',)
    # inlines = [
    #     ClassroomInline,
    # ]
    search_fields = ('weekday',)


@register(InformationOfTheDay)
class InformationOfTheDayAdmin(admin.ModelAdmin):
    """
        Admin View for InformationOfTheDay
    """
    list_display = ('title', 'start_date', 'end_date',)
    list_filter = ('start_date', 'end_date',)
    # /    inlines = [
    #         ClassroomInline,
    #     ]
    search_fields = ('content',)


@register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
        Admin View for InformationOfTheDay
    """
    list_display = ('full_name', 'email', 'phone', 'organisation', 'function')
    list_filter = ('organisation', 'function')
    # /    inlines = [
    #         ClassroomInline,
    #     ]
    search_fields = (
        'first_name', 'last_name', 'phone', 'mobile_phone', 'professional_phone', 'organisation', 'function')


@register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
        Admin View for Address
    """
    list_display = ('street', 'zip', 'city', 'country')
    list_filter = ('zip', 'city', 'country',)
    search_fields = ('street', 'zip', 'city', 'country')


@register(ChildSpecificNeed)
class ChildSpecificNeedAdmin(admin.ModelAdmin):
    """
        Admin View for ChildSpecificNeed
    """
    list_display = ('child', 'ihp', 'attachment')
    list_filter = ('ihp', 'attachment',)
    search_fields = ('problem', 'measure_take', 'child')


@register(LogChangeClassroom)
class LogChangeClassroomAdmin(admin.ModelAdmin):
    """
        Admin View for LogChangeClassroom
    """
    list_display = ('child', 'classroom', 'next_classroom', 'date')
    list_filter = ('classroom', 'next_classroom', 'date')
    search_fields = ('child', 'classroom', 'next_classroom', 'date',)


@register(ReplacementClassroom)
class ReplacementClassroomAdmin(admin.ModelAdmin):
    """
        Admin View for RemplacementClassroom
    """
    list_display = ('from_date', 'end_date', 'child', 'classroom', 'archived')
    list_filter = ('from_date', 'end_date', 'classroom', 'archived')
    search_fields = ('from_date', 'end_date', 'classroom', 'child',)


class ChildToPeriodInline(admin.TabularInline):
    model = ChildToPeriod
    min_num = 0
    extra = 1
    sortable_by = "period__order"
    show_change_link = False
    can_delete = True
    classes = ('collapse',)
    verbose_name = _("Subscription")
    verbose_name_plural = _("Subscriptions")


class ChildToContactInline(admin.TabularInline):
    model = ChildToContact
    min_num = 0
    extra = 1
    show_change_link = True
    can_delete = True
    classes = ('collapse',)
    verbose_name = _("Contact")
    verbose_name_plural = _("Contacts")

class ReplacementClassroomInline(admin.TabularInline):
    model = ReplacementClassroom
    min_num = 0
    extra = 1
    show_change_link = True
    can_delete = True
    classes = ('collapse',)


class ChildSpecificNeedInline(admin.TabularInline):
    model = ChildSpecificNeed
    min_num = 0
    max_num = 1
    extra = 0
    show_change_link = True
    can_delete = True
    classes = ('collapse',)


class ChildTrackingLogInline(admin.TabularInline):
    model = ChildTrackingLog
    min_num = 0
    extra = 1
    # show_change_link = True
    can_delete = True
    ordering = ("-date",)
    classes = ('collapse',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = kwargs['request'].user
        return super(ChildTrackingLogInline, self).formfield_for_dbfield(db_field, **kwargs)


class StatusFilter(DefaultListFilter):
    title = _('Status')
    parameter_name = 'status__exact'

    def lookups(self, request, model_admin):
        return Child.STATUS

    def default_value(self):
        return "in_progress"


@register(Child)
class ChildAdmin(admin.ModelAdmin):
    """
        Admin View for Child
    """

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        settings = NobinobiChildSettings.get_settings()
        if settings.admin_child_list_display_order == NobinobiChildSettings.OrderChildListDisplayInAdmin.STD:
            self.list_display = ('first_name', 'last_name', 'usual_name', 'gender', 'birth_date', 'classroom', 'age_group', 'staff')
        elif settings.admin_child_list_display_order == NobinobiChildSettings.OrderChildListDisplayInAdmin.INV:
            self.list_display = ('last_name', 'first_name', 'usual_name', 'gender', 'birth_date', 'classroom', 'age_group', 'staff')
        return self.list_display

    def get_ordering(self, request):
        """
        Hook for specifying field ordering.
        """
        settings = NobinobiChildSettings.get_settings()
        if settings.admin_child_ordering == NobinobiChildSettings.OrderChildListDisplayInAdmin.STD:
            self.ordering = ('first_name', 'last_name', 'created')
        elif settings.admin_child_ordering == NobinobiChildSettings.OrderChildListDisplayInAdmin.INV:
            self.ordering = ('last_name', 'first_name', 'created')
        return self.ordering or ()  # otherwise we might try to *None, which is bad ;)
    list_filter = (StatusFilter, 'gender', 'classroom', 'age_group', 'staff')

    fieldsets = [
        (_("Personal information"), {
            'fields': ['first_name', 'last_name', 'usual_name', 'gender', 'picture', 'birth_date', 'languages',
                       'nationality',
                       'red_list',
                       'food_restrictions',
                       'sibling_name', 'sibling_birth_date', 'sibling_institution',
                       'comment', "autorisations", 'renewal_date', ],
            # 'classes': ('collapse',),
        }),
        (_('Health info'), {
            'fields': (
                "allergies", "pediatrician", "pediatrician_contact", "usage_paracetamol", "healthy_child",
                "good_development",
                "specific_problem",
                "vaccination",
                "health_insurance"
            ),
            'classes': ('collapse',),
        }),
        (_('Classroom'), {
            'fields': ('classroom', 'next_classroom', 'date_next_classroom', 'age_group'),
            # 'classes': ('collapse',),
        }),
        (_('Staff'), {
            'fields': ['staff'],
        }),
        (_('File status'), {
            'fields': ['status', 'slug', 'date_end_child', 'created', 'modified'],
            'classes': ('collapse',),

        })]

    inlines = [
        ReplacementClassroomInline,
        ChildToPeriodInline,
        ChildToContactInline,
        ChildSpecificNeedInline,
        ChildTrackingLogInline,
    ]
    # raw_id_fields = ('',)
    readonly_fields = ('slug', "folder", "created", "modified")
    search_fields = (
        'first_name', 'last_name', 'usual_name', 'birth_date', 'classroom__name', 'next_classroom__name',
        'date_next_classroom',
        'age_group__name', 'staff__first_name', 'staff__last_name')
    actions = ["child_archived", "remove_information_after_archived"]
    save_as = True
    save_as_continue = True
    save_on_top = True

    def folder(self, x):
        try:
            from nobinobi_sape_contract.models import Folder
        except ModuleNotFoundError as err:
            # Error handling
            pass
        else:
            return Folder.objects.get(child=x)

    folder.short_description = _('Folder')

    def child_archived(self, request, queryset):
        rows_updated = queryset.update(status=Child.STATUS.archived)
        if rows_updated == 1:
            message_bit = _("1 child was")
        else:
            message_bit = _("{} children were").format(rows_updated)
        self.message_user(request, "%s successfully marked as archived." % message_bit)

    child_archived.short_description = _('Put child in archive')

    def remove_information_after_archived(self, request, queryset):
        for qs in queryset.filter(status=Child.STATUS.archived):
            child = qs
            child.pediatrician = None
            child.classroom = None
            child.next_classroom = None
            child.age_group = None
            child.picture = None
            child.red_list = ""
            child.comment = ""
            child.nationality = ""
            child.sibling_name = ""
            child.sibling_birth_date = None
            child.sibling_institution = ""
            child.renewal_date = None
            child.usage_paracetamol = None
            child.usage_homeopathy = None
            child.healthy_child = None
            child.good_development = None
            child.specific_problem = None
            child.vaccination = None
            child.pediatrician_contact = None
            child.health_insurance = ""
            child.autorisations = ""
            child.staff = None

            # food rest
            if hasattr(child, "food_restrictions"):
                for fr in child.food_restrictions.all():
                    child.food_restrictions.remove(fr)
        #     allergies
            if hasattr(child, "allergies"):
                for a in child.allergies.all():
                    child.allergies.remove(a)
        #     periods
            if hasattr(child, "periods"):
                for p in child.periods.all():
                    child.periods.remove(p)
        #     periods
            if hasattr(child, "contacts"):
                for c in child.contacts.all():
                    child.contacts.remove(c)
        #     languages
            if hasattr(child, "languages"):
                for l in child.languages.all():
                    child.languages.remove(l)
        #     languages
            if hasattr(child, "childspecificneed"):
                for l in child.childspecificneed.all():
                    child.childspecificneed.remove(l)

            # contacts
            if hasattr(child, "childtocontact_set"):
                for l in child.childtocontact_set.all():
                    la = l.contact.id
                    l.delete()
                    if not ChildToContact.objects.filter(contact_id=la).exists() and not Child.objects.filter(pediatrician__contacts__id=la).exists():
                        Contact.objects.get(id=la).delete()

        #     periodes
            if hasattr(child, "childtoperiod_set"):
                for l in child.childtoperiod_set.all():
                    l.delete()

        #     childtrackinglog
            if hasattr(child, "childtrackinglog_set"):
                for l in child.childtrackinglog_set.all():
                    l.delete()

        #     replacementclassroom_set
            if hasattr(child, "replacementclassroom_set"):
                for l in child.replacementclassroom_set.all():
                    l.delete()


        #     logchangeclassroom_set
            if hasattr(child, "logchangeclassroom_set"):
                for l in child.logchangeclassroom_set.all():
                    l.delete()


            # OBSERVATIONS
            try:
                from nobinobi_observation.models import Observation
            except ModuleNotFoundError as err:
                # Error handling
                pass
            else:
                obs = Observation.objects.filter(child=child)
                for ob in obs:
                    ob.delete()

            #   DAILY FOLLOW UP
            try:
                from nobinobi_daily_follow_up.models import DailyFollowUp
            except ModuleNotFoundError as err:
                # Error handling
                pass
            else:
                dfus = DailyFollowUp.objects.filter(presence__child=child)
                for dfu in dfus:
                    # ACTIVITY
                    from nobinobi_daily_follow_up.models import Activity
                    acts = Activity.objects.filter(daily_follow_up=dfu)
                    for act in acts:
                        act.delete()
                    # Nap
                    from nobinobi_daily_follow_up.models import Nap
                    naps = Nap.objects.filter(daily_follow_up=dfu)
                    for nap in naps:
                        nap.delete()
                    # LotionDailyFollowUp
                    from nobinobi_daily_follow_up.models import LotionDailyFollowUp
                    ldfus = LotionDailyFollowUp.objects.filter(daily_follow_up=dfu)
                    for ldu in ldfus:
                        ldu.delete()
                    # DiaperChange
                    from nobinobi_daily_follow_up.models import DiaperChange
                    dpcs = DiaperChange.objects.filter(daily_follow_up=dfu)
                    for dpc in dpcs:
                        dpc.delete()
                    # DailyFollowUpToMedication
                    from nobinobi_daily_follow_up.models import DailyFollowUpToMedication
                    xs = LotionDailyFollowUp.objects.filter(daily_follow_up=dfu)
                    for x in xs:
                        x.delete()
                    # Medication
                    from nobinobi_daily_follow_up.models import Medication
                    xs = Medication.objects.filter(child=child)
                    for x in xs:
                        x.delete()

            child.save()
            self.message_user(request, "%s successfully removed infos." % child)

    remove_information_after_archived.short_description = _('Remove informations after archived')

    def response_change(self, request, obj):
        if "_printhealcard" in request.POST:
            return HttpResponseRedirect(reverse("nobinobi_child:print_heal_card", kwargs={"pk": obj.pk}))
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChildAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['staff'].queryset = Staff.objects.filter(status__exact='active')
        return form


@register(ChildTrackingLog)
class ChildTrackingLogAdmin(admin.ModelAdmin):
    """
        Admin View for ChildTrackingLog
    """
    list_display = ('date', 'user', 'child',)
    list_filter = ('date',)
    search_fields = ('date', "body")


@register(NobinobiChildSettings)
class NobinobiChildSettingsAdmin(admin.ModelAdmin):
    pass
