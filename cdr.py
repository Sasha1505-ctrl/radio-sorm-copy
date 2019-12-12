class Cdr:
    """General call data record presentation"""

    def add_toc(self, toc, group=False, termination='ok'):
        # Init head rec
        self.seq_num = toc.seq_num
        print("add_toc() - calling")
        if termination != 'ok':
            print("add_toc() - rejected call")
    def add_tcc(self, tcc):
        # Append data to rec
        print("add_tcc() - calling")
