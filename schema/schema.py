from graphene_django import DjangoObjectType
import graphene

from django.contrib.auth import get_user_model
from decks.models import Deck
from cards.models import Card


from decks.schema import (
    DeckType,
    DeckMutation
)
from cards.schema import (
    CardType,
    CardMutation
)



class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Mutation(graphene.ObjectType):
    card_mutation = CardMutation.Field()
    deck_mutation = DeckMutation.Field()


class Query(graphene.ObjectType):
	users = graphene.List(UserType)

	decks = graphene.Field(DeckType, title=graphene.String(required=True))
	decks_by_id = graphene.Field(DeckType, id=graphene.Int())

	cards = graphene.List(CardType)
	cards_by_id = graphene.Field(CardType, id=graphene.Int())

	def resolve_users(info, root):
		return get_user_model().objects.all()

	def resolve_decks(root, info, title):
		try:
			return Deck.objects.get(title=title)
		except Deck.DoesNotExist:
			return None

	def resolve_decks_by_id(info, root, id):
		return Deck.objects.get(pk=id)

	def resolve_cards(info, root):
		return Card.objects.select_related("deck").all()

	def resolve_cards_by_id(info, root, id):
		return Card.objects.get(pk=id)



schema = graphene.Schema(query=Query, mutation=Mutation)