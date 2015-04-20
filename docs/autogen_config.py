#!/usr/bin/env python

from IPython.utils.text import indent, dedent

from IPython.terminal.ipapp import TerminalIPythonApp
from IPython.kernel.zmq.kernelapp import IPKernelApp

def document_config_options(classes):
    lines = []
    for cls in classes:
        classname = cls.__name__
        for k, trait in sorted(cls.class_traits(config=True).items()):
            ttype = trait.__class__.__name__

            termline = classname + '.' + trait.name

            # Choices or type
            if 'Enum' in ttype:
                # include Enum choices
                termline += ' : ' + '|'.join(repr(x) for x in trait.values)
            else:
                termline += ' : ' + ttype
            lines.append(termline)

            # Default value
            try:
                dv = trait.get_default_value()
                dvr = repr(dv)
            except Exception:
                dvr = dv = None # ignore defaults we can't construct
            if (dv is not None) and (dvr is not None):
                if len(dvr) > 64:
                    dvr = dvr[:61]+'...'
                # Double up backslashes, so they get to the rendered docs
                dvr = dvr.replace('\\n', '\\\\n')
                lines.append('    Default: `%s`' % dvr)
                lines.append('')

            help = trait.get_metadata('help')
            if help is not None:
                lines.append(indent(dedent(help), 4))
            else:
                lines.append('    No description')

            lines.append('')
    return '\n'.join(lines)

kernel_classes = IPKernelApp().classes

def write_doc(name, title, classes, preamble=None):
    configdoc = document_config_options(classes)
    filename = '%s.rst' % name
    with open('source/config/options/%s' % filename, 'w') as f:
        f.write(title + '\n')
        f.write(('=' * len(title)) + '\n')
        f.write('\n')
        if preamble is not None:
            f.write(preamble + '\n\n')
        f.write(configdoc)
    with open('source/config/options/generated', 'a') as f:
        f.write(filename + '\n')


if __name__ == '__main__':
    # create empty file
    with open('source/config/options/generated', 'w'):
        pass

    write_doc('terminal', 'Terminal IPython options', TerminalIPythonApp().classes)
    write_doc('kernel', 'IPython kernel options', kernel_classes,
        preamble="These options can be used in :file:`ipython_kernel_config.py`",
    )

