from pydactyl import PterodactylClient

class Connect:
    def __init__(self, api_key: str, base_url: str = 'https://panel.optimihost.com'):
        self._api = PterodactylClient(base_url, api_key)

        # Client API
        self.Account = self._api.client.account
        self.servers = self._api.client.servers
        self.Backups = self._api.client.servers.backups
        self.Databases = self._api.client.servers.databases
        self.Files = self._api.client.servers.files
        self.Network = self._api.client.servers.network
        self.Schedules = self._api.client.servers.schedules
        self.Settings = self._api.client.servers.settings
        self.Startup = self._api.client.servers.startup
        self.Users = self._api.client.servers.users

        # Application API
        self.Locations = self._api.locations
        self.Nests = self._api.nests
        self.Nodes = self._api.nodes
        self.AppServers = self._api.servers
        self.AppUsers = self._api.user

    def ListServers(self):
        return self.servers.list_servers()

    def GetServerInfo(self, server_id: str, detail: bool = False, includes=None, params=None):
        return self.servers.get_server(server_id, detail=detail, includes=includes, params=params)

    def SendPower(self, server_id: str, signal: str):
        return self.servers.send_power_action(server_id, signal)
