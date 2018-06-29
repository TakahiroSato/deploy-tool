<template>
  <div id="main-pane">
    <div id="left-pane">
      <ul>
        <li class="left-pane" v-for="host in hosts" @click="changeSetting(host)">{{ host }}</li>
      </ul>
    </div>
    <div id="right-pane">
      <div style="margin-left: 50px; margin-top: 20px">
          <div>
            <h3>接続先</h3>
            <input type="text" v-model="inputHost" placeholder="host or ip">
          </div>
          <div style="margin-top: 20px">
            <h3>秘密鍵</h3>
            <input type="text" v-model="inputSecretKeyPath" placeholder="secret key path">
          </div>
          <div style="margin-top: 20px">
            <h3>パスワード</h3>
            <input type="text" v-model="inputPassword" placeholder="password">
          </div>
          <div style="margin-top: 20px">
            <h3>バックアップ先</h3>
            <input type="text" v-model="inputBackUpPath" placeholder="backup path">
          </div>
          <div style="margin-top: 20px">
            <input id="save" type="submit" value="保存" @click="save()">
          </div>
      </div>
    </div>
  </div>
</template>

<script>
  var connectionsFilePath = require('electron').remote.app.getAppPath() + '\\data\\connections.json'
  export default {
    name: 'connection-setting-page',
    data: function () {
      return {
        inputHost: '',
        inputSecretKeyPath: '',
        inputPassword: '',
        inputBackUpPath: '',
        connections: [],
        hosts: []
      }
    },
    methods: {
      save: function () {
        var fs = require('fs')
        this.connections.some(function (v, i) {
          if (v.host === this.inputHost) this.connections.splice(i, 1)
        }.bind(this))
        this.connections.push({
          host: this.inputHost,
          secretKey: this.inputSecretKeyPath,
          password: this.inputPassword,
          backupPath: this.inputBackUpPath
        })
        fs.writeFile(connectionsFilePath,
          JSON.stringify(this.connections, null, ''), 'utf-8', (err) => {
            if (err) {
              console.log(err)
              throw err
            }
          })
        this.readFile()
      },
      readFile: function () {
        var fs = require('fs')
        var json = fs.readFileSync(connectionsFilePath, 'utf-8')
        if (json.length > 0) {
          this.connections = []
          this.connections = this.connections.concat(JSON.parse(json))
        }
        this.hosts = []
        this.hosts = this.connections.map(function (d) {
          return d.host
        })
      },
      changeSetting: function (host) {
        var setting = this.connections.filter(function (v, i) {
          if (v.host === host) return true
        })
        setting = setting[0]
        this.inputHost = setting.host
        this.inputSecretKeyPath = setting.secretKey
        this.inputPassword = setting.password
        this.inputBackUpPath = setting.backupPath
      }
    },
    mounted: function () {
      this.readFile()
    }
  }
</script>

<style>
    * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #main-pane {
    height: inherit;
    margin: 0px 15px 10px 0px;
    border: 2px solid #999999;
  }

  #left-pane {
    width: 150px;
    height: inherit;
    display: inline-block;
      float:left;
    text-align: center;
    border-style: solid;
    border-color: gray;
    border-width: 0 1px 0 0;
  }

  li.left-pane{
    width:100%;
    padding-top:5px;
    padding-bottom:5px;
    border-bottom: 1px solid #999999;
    color:red;
  }

  #right-pane {
    height: inherit;
    display: inline-block;
      float:left;
  }

  ul{
    text-align: center;
  }

  #save{
    padding: 0.5em 1em;
    text-decoration: none;
    background: #7FB6F5;
  }
</style>
