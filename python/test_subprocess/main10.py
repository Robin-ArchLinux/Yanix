from invoke import task

@task
def hello(c):
    print("Hello, world!")

@task
def build(c):
    c.run("ls -al")

@task
def install(c):
    c.run("sudo pacman -S code")
