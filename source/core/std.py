class IO:

    @staticmethod
    def up(string, **var):
        format_specifier=["$w", "$d"]
        if any(fs in string for fs in format_specifier):
            pass
