import cgi
form = cgi.FieldStorage()


print ('bienvenue')

if form.has_key("search"):
    text = form["search"].value
    print ("Content-Type: text/html\n")
    print ("""
    <H3>Merci, %s !</H3>
    <H4>La phrase que vous m'avez fournie était : </H4>
    <H3><FONT Color="red"> %s </FONT></H3>""") % (text)
else:
    text = "C'etait vide"