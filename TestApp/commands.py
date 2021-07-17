from cligo import CliApp
app = CliApp("trellect")


@app.register('login')
def login():
    print("logging in...")
    return True

print(app.commands)
