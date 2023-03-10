from import_export import resources
from tickets.models import Tickets

class TicketsResource(resources.ModelResource):
    class Meta:
        model=Tickets

#class UserResource(resources.ModelResource):
 #   class Meta:
  #      model=User