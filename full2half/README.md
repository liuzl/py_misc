The built-in `unicodedata` module can do it:

```python
import unicodedata
foo = u'１２３４５６７８９０'
ret = unicodedata.normalize('NFKC', foo)
# '1234567890'
```
