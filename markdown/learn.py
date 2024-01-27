import markdown2
html = markdown2.markdown("*boo!*", extras=["footnotes"])
print(html)