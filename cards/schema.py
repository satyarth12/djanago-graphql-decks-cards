from graphene_django import DjangoObjectType
import graphene

from graphql import GraphQLError

from .models import Card
from decks.models import Deck

from decks.schema import (
    DeckMutation,
    DeckType
)

from django.utils import timezone


buckets = (
        (1, 1),
        (2, 3),
        (3, 7),
        (4, 16),
        (5, 30)
        )

#for calculating the next_review_at
def return_date_time(days):
    now = timezone.now()
    return now + timezone.timedelta(days=days)
    
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


class UpdateCardMutation(graphene.Mutation):
    class Arguments:
        question = graphene.String(required=True)
        answer = graphene.String(required=True)
        status = graphene.Int(description='easy, average, or difficult -> 1, 2, 3')
        card_id = graphene.ID()

    card = graphene.Field(CardType)

    def mutate(root, info, card_id, question, answer, status):
        if status not in [1,2,3]:
            raise GraphQLError('Status out of bounds. Must be 1, 2, or 3.')

        c = Card.objects.get(pk=card_id)

        #updating bucket's day according to the status
        bucket = c.bucket
        if status == 1 and bucket > 1:
            bucket -= 1
        elif status == 3 and bucket <=4:
            bucket += 1


        days = buckets[bucket-1][1] #[1] will return the number of days in the buckets tuple, 2,7,16....
        next_review_at = return_date_time(days)
        print(bucket)
        c.question=question
        c.answer=answer
        c.bucket=bucket
        c.next_review_at=next_review_at
        c.last_reviewed_at=timezone.now()
        c.save()

        return UpdateCardMutation(card = c)

