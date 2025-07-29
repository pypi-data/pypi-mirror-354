from . import RunnerWrapper, locate_command


BaseCommand = locate_command("runserver")


class Command(RunnerWrapper, BaseCommand):
    pass
