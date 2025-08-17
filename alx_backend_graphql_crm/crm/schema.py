import graphene
from .models import Customer, Product, Order
from django.db import IntegrityError
import re



class CustomerType(graphene.ObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)

    def resolve_customers(self, info):
        return Customer.objects.all()

# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if phone:
            phone_pattern = r'^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
            if not re.match(phone_pattern, phone):
                return CreateCustomer(customer=None, success=False, message="Invalid phone format.")
        try:
            customer = Customer.objects.create(name=name, email=email, phone=phone)
            return CreateCustomer(customer=customer, success=True, message="Customer created successfully.")
        except IntegrityError:
            return CreateCustomer(customer=None, success=False, message="Email already exists.")

schema = graphene.Schema(query=Query, mutation=CreateCustomer)