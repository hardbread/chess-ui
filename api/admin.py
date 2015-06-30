from django import forms
from django.contrib import admin
from models import *


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'rating', 'decade_born_in']
    fieldsets = (
        (
            None, {
                'fields': (('first_name', 'last_name',), 'rating', 'birthday')
            }
        ),
    )


class TeamAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'match']
    fieldsets = (
        (
            'Team gamers', {
                'fields': (('player_1', 'player_2',),)
            }
        ),
    )


class TeamChoice(admin.TabularInline):
    model = Team
    extra = 3


class MatchAdminForm(forms.ModelForm):
    def clean(self):
        game_time_st, game_time_end = self.cleaned_data.get('game_time_st'), self.cleaned_data.get('game_time_end')
        if game_time_st >= game_time_end:
            raise forms.ValidationError('%(ed)s should be greater %(sd)s', params={
                'sd': game_time_st,
                'ed': game_time_end
            },)
        return self.cleaned_data

    class Meta:
        exclude = []
        model = Match


class MatchAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'game_time_st', 'game_time_end', 'tournament', 'winner']
    fieldsets = (
        (
            'Time period', {
                'fields': (('game_time_st', 'game_time_end'),)
            }
        ),
        (
            None, {
                'fields': ('winner',)
            }
        )
    )

    inlines = [TeamChoice]

    form = MatchAdminForm


class MatchChoice(admin.TabularInline):
    model = Match
    form = MatchAdminForm
    extra = 3


class TournamentAdminForm(forms.ModelForm):

    def clean(self):
        start_date, end_date = self.cleaned_data.get('start_date'), self.cleaned_data.get('end_date')
        if end_date <= start_date:
            raise forms.ValidationError('%(sd)s should be greater %(ed)s', params={
                'sd': start_date,
                'ed': end_date
            },)
        return self.cleaned_data

    class Meta:
        exclude = []
        model = Tournament


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'start_date', 'end_date', 'winner']
    readonly_fields = ('winner',)
    fieldsets = (
        (
            'Tournament date', {
                'fields': (('start_date', 'end_date'),)
            }
        ),
        (
            'Tournament info', {
                'fields': ('title', 'description',)
            }
        ),
        (
            None, {
                'fields': ('winner',)
            }
        ),
    )

    inlines = [MatchChoice]

    form = TournamentAdminForm


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tournament, TournamentAdmin)
