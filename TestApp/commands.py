from cligo import CliApp


app = CliApp("testapp")


@app.register('login')
def login(request):
    print("logging in...")
    return True


print(app.commands)
