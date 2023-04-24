from typing import TypeVar

from django.db.models import Count, Exists, OuterRef
from django.forms import CheckboxInput, Select
from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):

    CHOICES = (
        ('created_at', 'Oldest first'),
        ('-created_at', 'Newest first'),
    )

    is_interesting = filters.BooleanFilter(
        method='filter_interesting',
        distinct=True,
        widget=CheckboxInput(
            attrs={'class': 'filter', 'id': 'radio1', 'checked': False}
        ),
        label='Interesting',
    )

    is_popular = filters.BooleanFilter(
        method='filter_popular',
        distinct=True,
        widget=CheckboxInput(
            attrs={'class': 'filter', 'id': 'radio2', 'checked': False}
        ),
        label='Popular',
    )

    ordering = filters.ChoiceFilter(
        choices=CHOICES,
        method='ordering_filter',
        widget=Select(attrs={'class': 'filter', 'id': 'ordering'}),
        label='By date',
    )

    class Meta:
        model = Post
        fields = ['category']

    T = TypeVar('T')

    def annotate_by_interesting(self, queryset: T) -> T:
        """Will return a QuerySet annotated with is_interesting"""

        following = self.request.user.profile.following
        return queryset.annotate(
            is_interesting=Exists(following.filter(id=OuterRef('author__profile__id')))
        )

    def annotate_by_liked_cnt(self, queryset: T) -> T:
        """Annotate QuerySet with liked_cnt."""

        return queryset.annotate(liked_cnt=Count('liked'))

    def ordering_filter(self, queryset: T, name: str, value: str) -> T:
        """Order QuerySet by created_at."""

        if self.data.get('is_interesting'):
            return self.annotate_by_interesting(queryset).order_by(
                '-is_interesting', value
            )

        if self.data.get('is_popular'):
            return self.annotate_by_liked_cnt(queryset).order_by('-liked_cnt', value)

        return queryset.order_by(value)

    def filter_interesting(self, queryset: T, name: str, value: bool) -> T:
        """Filter QuerySet by user.profile.following posts."""

        if not value:
            return queryset

        return self.annotate_by_interesting(queryset).order_by(
            '-is_interesting', '-created_at'
        )

    def filter_popular(self, queryset, name: str, value: bool):
        """Order QuerySet by likes count."""

        if not value:
            return queryset

        return self.annotate_by_liked_cnt(queryset).order_by(
            '-liked_cnt', '-created_at'
        )
