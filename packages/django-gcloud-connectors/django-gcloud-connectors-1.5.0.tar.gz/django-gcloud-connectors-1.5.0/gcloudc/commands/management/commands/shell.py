from . import RunnerWrapper, locate_command


BaseCommand = locate_command("shell")


class Command(RunnerWrapper, BaseCommand):
    pass
