from graphene_django import DjangoObjectType
import graphene

from .models import Deck


class DeckType(DjangoObjectType):
	class Meta:
		model =Deck



class DeckMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
       	description = graphene.String(required=True)

    deck = graphene.Field(DeckType)

    def mutate(root, info, title, description):
    	d = Deck(title=title, description=description)
    	d.save()
    	return DeckMutation(deck=d)