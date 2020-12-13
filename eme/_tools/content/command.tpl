from core.dal.{entities} import {entity}
from eme.data_access import get_repo


class {entities_t}Command:
    def __init__(self, cli):
        self.repo = get_repo({entity})

    def run_create(self, {params}):
        {evar} = {entity}()
        {setters}

        self.repo.create({evar})

    def run_edit(self, uid, {params}):
        {evar} = self.repo.get(uid)
        {setters}

        self.repo.save()

    def run_delete(self, uid):
        {evar} = self.repo.get(uid)

        if {evar}:
            self.repo.delete({evar})
