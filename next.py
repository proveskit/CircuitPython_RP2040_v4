import supervisor


def set_next_code_file(file):
    supervisor.set_next_code_file(file, reload_on_success=True)
    supervisor.reload()
