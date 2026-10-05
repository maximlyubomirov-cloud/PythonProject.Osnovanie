























s = 'ЗдрАвстВуйте, гости!'

print(n := s.lower())
print(s.upper())
print(s.title()) # Capital
print(s.capitalize()) # Variable
print(s.rjust(40)) # Var writes in 40 znakomestax


print(s.strip()) # removes spaces po krayam
print(s.strip('!'))
print(s.strip('З '))
print(s.strip('Зд '))


# print(s.find(sub:'Т', start 8, end:11))
# print(s.replace())
ls = s.split() # создает список разделяя
ls = s.split(' , ')
# с пробелом
print(ls)
print(", ".join(ls))
