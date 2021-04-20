from graphene_django import DjangoObjectType
import graphene

from .models import Card



class CardType(DjangoObjectType):
	class Meta:
		model =Card




class CardMutation(graphene.Mutation):
    class Arguments:
        question = graphene.String(required=True)
       	answer = graphene.String(required=True)
        deck_id = graphene.Int()

    card = graphene.Field(CardType)

    def mutate(root, info, question, answer, deck_id):
    	c = Card(question=question, answer=answer)
    	d = Deck.objects.get(id=deck_id)
    	c.deck=d
    	c.save()
    
    	return CardMutation(card=c)