import re
from os.path import dirname, realpath, join

import inflect


class EntityCommand:
    def __init__(self, cli):
        self.dbase = cli.script_path

    def run(self, name: str, entraw: list=None):
        ents = self.parse_entlist(entraw)

        self.write_entity(name, ents)

        # todo: cli CRUD commands
        #self.write_command(name, ents)

        # todo: fixture & factory & default values
        #self.write_factory(name, ents)

        # todo: Ctrl CRUD commands + use fixtures
        #self.write_controller(name, ents)

        print("Entity {} added!".format(name))

    def write_entity(self, name, ents):
        p = inflect.engine()
        name_plural = p.plural_noun(name).lower()
        file_entitytpl = join(self.dbase, 'content', 'entity.tpl')

        with open(file_entitytpl) as fh:
            entity_tpl = fh.read()

        attr_def_content = ""
        attr_init_content = ""
        attr_view_content = ""

        for (ename, etype, edef, eopt) in ents:
            # view declaration
            attr_view_content += '\n            "{0}": self.{0},'.format(ename)
            # init declaration
            attr_init_content += '\n        self.{0} = kwargs.get("{0}")'.format(ename)

            modi = ''

            if etype == 'str': etype = 'String'
            elif etype == 'int': etype = 'Integer'
            elif etype == 'uuid':
                etype = 'uuid'
                modi = ', default=uuid.uuid4'
            elif etype == 'guid':
                etype = 'GUID'
                modi = ', default=uuid.uuid4'
            elif etype == 'timestamp' or etype == 'unix':
                etype = 'TIMESTAMP'
                modi += ', server_default=func.now(), onupdate=func.current_timestamp()'
            elif etype.lower() == etype:
                etype = etype.title()

            if '*' in eopt: modi += ', nullable=True'
            if '!' in eopt: modi += ', primary_key=True'
            if edef:
                if etype == 'string':
                    edef = '"{}"'.format(edef)
                modi += ', default={}'.format(edef)

            attr_def_content += '\n    {0} = Column({1}{2})'.format(ename, etype, modi)

        file_content = entity_tpl.format(**{
            "class_name": name.title(),
            "table_name": name_plural,
            "eprefx": name[0].lower(),
            "attr_def": attr_def_content,
            "attr_init": attr_init_content,
            "attr_view": attr_view_content,
        })

        # Write Entity class & Repository
        with open('core/dal/{}.py'.format(name_plural), 'w') as fh:
            fh.write(file_content)

    def parse_entlist(self, entraw):
        if entraw is None:
            return []

        # iterate through each property
        prop_pat = re.compile(r"(?P<name>\w+)\:*(?P<type>\w*)\=*(?P<default>\w*)(?P<opt>\**)")
        ents = []

        for _ent in entraw:
            (ename, etype, edef, eopt) = prop_pat.findall(_ent)[0]
            ents.append((ename, etype.lower(), edef, eopt))

        return ents
