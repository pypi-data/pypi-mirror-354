import __init__

pf = __init__.profanityfilter(['word'])

print(pf.fillerscan('Oh oh! Hey! Can I tell about the wordof the day? It"s a really cool word!', '[_]'))
