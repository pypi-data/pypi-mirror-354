cleanlang let's you filter out profane and/or offensive language with customizable options! This includes things like threshold, a line between whether something is close to profane or not profane!
___

**DISCLAIMER**

Our module's results vary depending on your settings. This module is also in beta as of 6/10/25. We are also not responsible for any harm according to the MIT license.
___

profanityfilter: (Creates a profanity filter class)
```python
import cleanlang

profanebot = cleanlang.profanityfilter(['bad', 'word'], 80) # (bad word list) (threshold)
```
Output:
```
No output
```
___

scan: (Determines whether or not a string contains profane language or not)
```python
import cleanlang

pb = cleanlang.profanityfilter(['bad', 'word'], 80)

print(pb.scan('this Woard is b@d'))
```
Output:
```
True
```
___

dependencies:
- fuzzywuzzy[speedup]
___

Thanks for reading, and enjoy cleanlang! :)
