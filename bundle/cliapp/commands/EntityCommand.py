import re
import inflect


class EntityCommand:
    def __init__(self, cli):
        pass

    def run(self, name: str, entraw: list):
        ents = self.parse_entlist(entraw)
        self.write_entity(name, ents)

        # todo: write defaults
        # todo: cli CRUD commands
        # todo: Ctrl CRUD commands
        # todo: fixture & factory & default values

    def write_entity(self, name, ents):
        p = inflect.engine()
        name_plural = p.plural_noun(name).lower()
        special_types = ['uuid', 'guid', 'timestamp']

        with open('cliapp/content/entity.tpl') as fh:
            entity_tpl = fh.read()

        attr_def_content = ""
        attr_init_content = ""
        attr_view_content = ""

        for (ename, etype, edef, eopt) in ents:
            # view declaration
            attr_view_content += '\n            "{0}": self.{0},'.format(ename)
            # init declaration
            attr_init_content += '\n        self.{0} = kwargs.get("{0}")'.format(ename)

            if etype in special_types:
                # todo: find definition from templates
                pass
            else:
                if etype == 'str': etype = 'string'
                if etype == 'int': etype = 'integer'
                modi = ''
                if '*' in eopt: modi += ', nullable=True'
                if '!' in eopt: modi += ', primary_key=True'
                if edef:
                    if etype == 'string':
                        edef = '"{}"'.format(edef)
                    modi += ', default={}'.format(edef)

                attr_def_content += '\n    {0} = Column({1}{2})'.format(ename, etype.title(), modi)

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
        # iterate through each property
        prop_pat = re.compile(r"(?P<name>\w+)\:*(?P<type>\w*)\=*(?P<default>\w*)(?P<opt>\**)")
        ents = []

        for _ent in entraw:
            (ename, etype, edef, eopt) = prop_pat.findall(_ent)[0]
            ents.append((ename, etype.lower(), edef, eopt))

        return ents
