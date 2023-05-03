from typing import TypeVar

from django.db.models import Count, Exists, OuterRef
from django.forms import CheckboxInput, Select
from django_filters import rest_framework as filters

from mwk.modules.main.models.post import Post


class PostFilter(filters.FilterSet):
    T = TypeVar('T')

    CHOICES = (
        ('created_at', 'Oldest first'),
        ('-created_at', 'Newest first'),
    )

    is_interesting = filters.BooleanFilter(
        method='filter_interesting',
        widget=CheckboxInput(attrs={'class': 'filter', 'id': 'radio1'}),
        label='Interesting',
    )

    is_popular = filters.BooleanFilter(
        method='filter_popular',
        widget=CheckboxInput(attrs={'class': 'filter', 'id': 'radio2'}),
        label='Popular',
    )

    date_ordering = filters.ChoiceFilter(
        choices=CHOICES,
        method='ordering_filter',
        widget=Select(attrs={'class': 'filter', 'id': 'date_ordering'}),
        label='By date',
    )

    class Meta:
        model = Post
        fields = ['category']

    def filter_interesting(self, queryset: T, name: str, value: bool) -> T:
        """Filter QuerySet by user.profile.following posts."""
        if value:
            following = self.request.user.profile.following
            queryset = (
                queryset.annotate(
                    is_interesting=Exists(following.filter(id=OuterRef('author__profile__id')))
                )
                .order_by('-is_interesting', '-created_at')
            )

        return queryset

    def filter_popular(self, queryset: T, name: str, value: bool) -> T:
        """Filter QuerySet by likes count."""

        if value:
            queryset = queryset.annotate(
                liked_cnt=Count('liked')
            ).order_by('-liked_cnt', '-created_at')

        return queryset

    def ordering_filter(self, queryset: T, name: str, value: str) -> T:
        """Order QuerySet by created_at."""

        if self.data.get('is_interesting'):
            queryset = self.filter_interesting(queryset, name, True)

        if self.data.get('is_popular'):
            queryset = self.filter_popular(queryset, name, True)

        return queryset.order_by(value)
