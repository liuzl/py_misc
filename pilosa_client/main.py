from __future__ import print_function
from pilosa import Index, Client, PilosaError, TimeQuantum

# We will just use the default client which assumes the server is at http://localhost:10101
client = Client()

# Let's load the schema from the server.
# Note that, for this example the schema should be created beforehand
# and the stargazer data should be imported.
# See the Getting Started repository: https://github.com/pilosa/getting-started/

# Let's create Index and Field objects, which will contain the settings
# for the corresponding indexes and fields.
try:
    schema = client.schema()
except PilosaError as e:
    # Most calls will raise an exception on errors.
    # You should handle them appropriately.
    # We will just terminate the program in this case.
    raise SystemExit(e)

# We need to refer to indexes and fields before we can use them in a query.
repository = schema.index("repository")
stargazer = repository.field("stargazer")
language = repository.field("language")

# Which repositories did user 8 star:
repository_ids = client.query(stargazer.row(14)).result.row.columns
print("User 8 starred: ", repository_ids)

# What are the top 5 languages in the sample data:
top_languages = client.query(language.topn(5)).result.count_items
print("Top 5 languages: ", [item.id for item in top_languages])

# Which repositories were starred by both user 14 and 19:
query = repository.intersect(
    stargazer.row(14),
    stargazer.row(19)
)
mutually_starred = client.query(query).result.row.columns
print("Both user 14 and 19 starred:", mutually_starred)

# Which repositories were starred by user 14 or 19:
query = repository.union(
    stargazer.row(14),
    stargazer.row(19)
)
either_starred = client.query(query).result.row.columns
print("User 14 or 19 starred:", either_starred)

# Which repositories were starred by user 14 or 19 and were written in language 1:
query = repository.intersect(
    repository.union(
        stargazer.row(14),
        stargazer.row(19)
    ),
    language.row(1)
)
mutually_starred = client.query(query).result.row.columns
print("User 14 or 19 starred, written in language 1:", mutually_starred)

# Set user 99999 as a stargazer for repository 77777
client.query(stargazer.set(99999, 77777))
