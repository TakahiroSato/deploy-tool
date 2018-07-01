const _connectionsFilePath =
  require('electron').remote.app.getAppPath() + '\\data\\connections.json'

export default {
  connectionsFilePath: _connectionsFilePath,
  getHostList: () => {
    const fs = require('fs')
    const json = fs.readFileSync(_connectionsFilePath, 'utf-8')
    if (json.length > 0) {
      return JSON.parse(json)
    } else {
      return []
    }
  }
}
