#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """
    for ticket in tickets:
        # print(ticket.source, ticket.destination)
        hash_table_insert(hashtable, ticket.source, ticket.destination)
    
    location = hash_table_retrieve(hashtable, "NONE") #PDX

    for i in range(length):
        route[i] = location #[PDX]
        # new location looks for key "PDX", returns the destination of "PDX"
        location = hash_table_retrieve(hashtable, location) 
    

    return route
