

class ExampleGroup:

    def __init__(self, app):
        self.app = app

    async def echo(self, request, client):
        print(request.data['message'])

        return {
            "message": request.data['message'] + ' ' + str(id(client))
        }

        # or:
        # await self.app.send({
        #     "message": request.data['message']
        # }, client, route='Example:echo')
