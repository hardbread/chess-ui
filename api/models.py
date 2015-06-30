import datetime
from django.db import models
from elo import Elo
from decimal import Decimal


class ModelMixin(models.Model):
    def to_dict(self, custom_model=None, _recursion=None):
        ret = {}
        if _recursion is None:
            _recursion = set()
        _recursion.add(self)
        obj_model = custom_model or self
        for k, v in obj_model.__dict__.items():
            try:
                if k.endswith('_cache') and v not in _recursion:
                    if hasattr(v, 'to_dict'):
                        ret.setdefault(k[1:].replace('_cache', ''), v.to_dict(_recursion=_recursion))
                    elif isinstance(v, models.Model):
                        ret.setdefault(k[1:].replace('_cache', ''), self.to_dict(v, _recursion=_recursion))
                elif not k.startswith('_'):
                    if isinstance(v, (dict, list, int, basestring, set, float, long) or v is None):
                        ret.setdefault(k, v)
                    elif isinstance(v, Decimal):
                        ret.setdefault(k, str(v))
                    elif isinstance(v, datetime.datetime):
                        ret.setdefault(k, v.strftime("%Y-%m-%d %H:%M:%S"))
                    elif isinstance(v, datetime.time):
                        ret.setdefault(k, v.strftime("%H:%M:%S"))
                    elif isinstance(v, datetime.date):
                        ret.setdefault(k, datetime.datetime.combine(
                            v, datetime.datetime.min.time()
                        ).strftime("%Y-%m-%d"))
            except:
                pass
        return ret

    class Meta:
        abstract = True


class Player(ModelMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=7, decimal_places=3, db_index=True)
    birthday = models.DateField()

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def decade_born_in(self):
        return self.birthday.strftime('%Y')[:3] + "0's"
    decade_born_in.short_description = 'Birth decade'

    def get_elo(self, value):
        return Elo(initial=value)

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    class Meta:
        unique_together = ('first_name', 'last_name', 'birthday')
        index_together = ('first_name', 'last_name', 'rating')


class Tournament(ModelMixin):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.ForeignKey(Player, blank=True, null=True, related_name='tournament_winner')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.title)

    class Meta:
        index_together = ('start_date', 'end_date')


class Match(ModelMixin):
    game_time_st = models.TimeField('Start time')
    game_time_end = models.TimeField('End time')
    winner = models.ForeignKey(Player, blank=True, null=True, related_name='match_winner')
    tournament = models.ForeignKey(Tournament, related_name='match_tournament')

    def __unicode__(self):
        return u'Match in {}-{}'.format(self.game_time_st, self.game_time_end)

    class Meta:
        index_together = ('game_time_st', 'game_time_end')


class Team(ModelMixin):
    player_1 = models.ForeignKey(Player, related_name='team_player_1')
    player_2 = models.ForeignKey(Player, related_name='team_player_2')
    match = models.ForeignKey(Match, related_name='team_match')

    def __unicode__(self):
        return u'{} & {}'.format(self.player_1, self.player_2)

    class Meta:
        unique_together = ('player_1', 'player_2', 'match')


class Score(ModelMixin):
    WIN = '1'
    DRAW = '0.5'
    LOSS = '0'
    CHOICES = (
        (WIN, 'Win'),
        (DRAW, 'Draw'),
        (LOSS, 'Loss'),
    )
    CHOICE = [1, 0.5, 0]
    player = models.ForeignKey(Player, related_name='score_player')
    match = models.ForeignKey(Match, related_name='score_match')
    score = models.IntegerField(editable=False, choices=CHOICES, default=LOSS)